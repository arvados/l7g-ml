#!/usr/bin/env Rscript
# install.packages("glmnet", repos = 'http://cran.us.r-project.org')
# install.packages("Matrix", repos = 'http://cran.us.r-project.org')
# install.packages("reticulate", repos = 'http://cran.us.r-project.org')

# Inorder to use Python
#reticulate::use_python('/usr/local/bin/python3')
#reticulate::py_discover_config()

# R libraries
library(Matrix)
library(foreach)
suppressMessages(library(glmnet))
library(reticulate)
library(methods)

# Python libraries
np <- import("numpy")

args = commandArgs(trailingOnly=TRUE)
# 11057 x 98692
Xrc <- np$load(args[1])
Xrc <- as.matrix(Xrc)
Xdim <- dim(Xrc)
print(Xdim)

Xdata <- matrix(data = 1, nrow = 1, ncol = Xdim[2])
row_ind = as.matrix(Xrc[1,])
col_ind = as.matrix(Xrc[2,])


# Make them into an integer vector
row_ind <- as.integer(row_ind) + 1
col_ind <- as.integer(col_ind) + 1


# Create a new sparse matrix

Xdata <- as.numeric(Xdata)
#row_ind <- as.numeric(row_ind)
#col_ind <- as.numeric(col_ind)

Xmatfull <- sparseMatrix(row_ind,col_ind,x = Xdata)
print(dim(Xmatfull))
rm(row_ind,col_ind,Xdata)

# Load the y array and make into vector in R
coldata <- np$load(args[2])
coldata <- as.matrix(coldata)

sampledata <- read.csv(args[3], sep="\t", stringsAsFactors=FALSE)
training_ind <- sampledata$Index[!is.na(sampledata$TrainingValidation) & sampledata$TrainingValidation == 1] + 1

y <- as.numeric(sampledata$CaseControl[!is.na(sampledata$TrainingValidation) & sampledata$TrainingValidation == 1])
y <- as.matrix(y)

# Load auxiliary matrix
auxiliaries <- names(sampledata)[-(1:4)]
Xauxiliary = as.matrix(sampledata[!is.na(sampledata$TrainingValidation) & sampledata$TrainingValidation == 1,][auxiliaries])

# Extract training set of the sparse matrix and combine with auxiliary matrix
Xmat = cbind(Xauxiliary, Xmatfull[training_ind,])
print(dim(Xmat))
rm(Xmatfull)

tags <- as.matrix(as.numeric(coldata[1,]))
varvals <- as.matrix(as.numeric(coldata[2,]))
zygosity <- as.matrix(as.numeric(coldata[3,]))

gamma <- args[4]
weighted <- args[5]
seedinput <- args[6]
forcePCA <- FALSE

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
checktype <- typeof(seedinput)
seedinput <- as.integer(seedinput)
checktype <- typeof(seedinput)

print(checktype)
print(seedinput)

set.seed(seedinput)

forcePCA <- as.logical(forcePCA)
weighted <- as.logical(weighted)
print(weighted)

gamma <- as.numeric(gamma)

print(gamma)

# Bagged Sample (for bootstrap)
bootidx = sample(seq(length(y)),length(y),replace=TRUE)
y = y[bootidx]
Xmat = Xmat[bootidx,]

Xtrain = Xmat
ytrain = y

# Weighning, if optioned
fraction_0 <- rep(1 - sum(ytrain == 0) / length(ytrain), sum(ytrain == 0))
fraction_1 <- rep(1 - sum(ytrain == 1) / length(ytrain), sum(ytrain == 1))
# assign that value to a "weights" vector

wtrain <- rep(1,length(ytrain))

if (weighted == TRUE) {
  wtrain[ytrain == 0] <- fraction_0
  wtrain[ytrain == 1] <- fraction_1
} else {
  wtrain <- rep(1, length(ytrain))
}

cv.ridge <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE,intercept = TRUE, weights=wtrain)
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^gamma ## Using gamma = 2
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999

if (forcePCA == TRUE) {
  w3[(length(w3) - 21):length(w3),1] <- 0
}

cv.lasso.adaptive <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=1, nfolds = 10, parallel=TRUE, intercept=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3, weights=wtrain)

# Plotting CV,Lambda plot
plotname_adaptive <- paste0('glmnet_lasso.png')
png(plotname_adaptive)
plot(cv.lasso.adaptive)
dev.off()

output_model_params <- function(modeltype) {
  coef <- coef(cv.lasso.adaptive, s=paste0("lambda.",modeltype))
  print(paste("lasso", modeltype, "intercept:", coef[1]))
  coefAux <- coef[2:(length(auxiliaries)+1)]
  coefTilevar <- coef[-(1:(length(auxiliaries)+1))]
  idxAux <- which(coefAux !=0)
  idxTilevar <- which(coefTilevar !=0)

  filename <- paste0("glmnet_lasso_", modeltype, ".txt")
  fileConn <- file(filename, "w")

  dfAux <- data.frame("feature" = auxiliaries[idxAux], "coef" = coefAux[idxAux])
  dfTilevar <- data.frame("feature" = paste0(tags[idxTilevar], "-", varvals[idxTilevar], "-", zygosity[idxTilevar]), "coef" = coefTilevar[idxTilevar])
  dfAll <- rbind(dfAux, dfTilevar)
  o <- order(abs(dfAll$coef), decreasing = TRUE)
  dfAll <- dfAll[o,]

  write.table(dfAll, fileConn, sep= "\t", row.names = FALSE, quote=FALSE)
  close(fileConn)
}

output_model_params("min") # minimum lambda
output_model_params("1se") # 1std lambda
