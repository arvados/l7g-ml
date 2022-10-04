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

Xmat <- sparseMatrix(row_ind,col_ind,x = Xdata)
print(dim(Xmat))
rm(row_ind,col_ind,Xdata)

# Load the y array and make into vector in R
coldata <- np$load(args[2])
coldata <- as.matrix(coldata)

sampledata = read.csv(args[3],header=FALSE)
sampledata = as.matrix(sampledata)

y <- as.numeric(sampledata[,3])
y <- as.matrix(y)

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

cv.lasso.adaptive <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=1, nfolds = 10, parallel=TRUE, intercept=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3,weights=wtrain)

# Plotting CV,Lambda plot
plotname_adaptive <- paste0('glmnet_lasso.png')
png(plotname_adaptive)
plot(cv.lasso.adaptive)
dev.off()

# Output model params minimum lambda
coefVec <- coef(cv.lasso.adaptive, s= "lambda.min")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]

filename <- paste0('glmnet_lasso_min.txt' )
fileConn <- file(filename, "w")

dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin,  "tag" = tags[idxnzmin], "variant" = varvals[idxnzmin],"zygosity"=zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

# Output model params for 1std lambda

coefVse <- coef(cv.lasso.adaptive, s="lambda.1se")
coefVse <- coefVse[-1]

idxnzse <- which(coefVse !=0)
nznumbse <- coefVse[idxnzse]

dataF_1se <- data.frame("nonnzerocoefs_1se" = nznumbse, "tag" = tags[idxnzse], "variant" = varvals[idxnzse],"zygosity"=zygosity[idxnzse])

o_1se <- order(abs(dataF_1se$nonnzerocoefs_1se), decreasing = TRUE)
dataF_1se <- dataF_1se[o_1se,]

filename1 <- paste0('glmnet_lasso_1se.txt')
fileConn1 <- file(filename1, "w")
write.table(dataF_1se, fileConn1, sep= "\t", row.names = FALSE)
close(fileConn1)
