#!/usr/bin/env Rscript
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
scipy <- import("scipy")
np <- import("numpy")

args = commandArgs(trailingOnly=TRUE)

# xstr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/X.npz"
x <- as.vector(np$load(args[1]))

# Make them into an integer vector
i <- as.integer(as.vector(np$load(args[2]))) + 1
j <- as.integer(as.vector(np$load(args[3]))) + 1

# Create a new sparse matrix
Xmat <- sparseMatrix(i,j,x = x)
#Xmat <- Xmat[,-20]

rm(i,j,x)

# Load the y array and make into vector in R
ynump <- np$load(args[4]) 
y <- as.vector(ynump)

pathdataOH <- as.vector(np$load(args[5]))
oldpath <- as.vector(np$load(args[6]))
varvals <- as.vector(np$load(args[7]))
colorblood <- args[8]

PCAlabel = 1000+seq(1, 20)
varvals = c(varvals,PCAlabel,99,999)

nsample = round(.90*length(y))
train = sample(seq(length(y)),nsample,replace=FALSE)

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
set.seed(999)
#cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=TRUE,intercept = FALSE)
#w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
#                   [, 1][2:(ncol(Xmat)+1)] ))^4.5 ## Using gamma = 2 
#w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999
#w3[(length(w3) - 19):length(w3)] <- 0

# Adaptive Lasso
set.seed(999)

reg.fit <- glmnet(Xmat[train,], y[train], family='binomial', alpha=1, intercept=TRUE, standardize=FALSE, type.measure='class',penalty.factor=w3)

coef.beta = rbind(reg.fit$a0,as.matrix(reg.fit$beta))  # extract coefficients at all values of lambda,  including the intercept

n = nrow(Xmat[train,])
p = ncol(Xmat[train,])
gamma.ebic = 0.50

dev = deviance(reg.fit)
reg.df = reg.fit$df
aic_obj = dev + 2 * reg.df
bic_obj = dev + log(n) * reg.df
ebic_obj = dev + log(n) * reg.df + 4 * gamma.ebic * reg.df * log(p)

lambda.ind = which.min(bic_obj)
coef.beta = coef.beta[, lambda.ind]
lambda = reg.fit$lambda[lambda.ind]
lamb = reg.fit$lambda

plotname_fit<- paste0('aicfit_',colorblood,'.png')
png(plotname_fit)

results <- data.frame(x = lamb, y = bic_obj)

coefVec = coef.beta[-1]
#coefVec = coef.beta
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 
tile_path <- as.vector(np$trunc(coefPathsMin/(16**5)))
tile_step <- as.vector(np$trunc((coefPathsMin - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

filename <- paste0('glmnet_lasso_bic_',colorblood,'.txt' )
fileConn <- file(filename, "w")
dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

idaic = match(reg.fit$lambda[lambda.ind],reg.fit$lambda)
cm = confusion.glmnet(reg.fit, newx = Xmat[-train,], newy = y[-train], family='binomial')[[idaic]]

png('confusion_matrix.png')
ggplot(as.data.frame(cm), aes(Predicted,sort(True,decreasing = T), fill= Freq)) + geom_tile() + geom_text(aes(label=Freq)) + scale_fill_gradient(low="white", high="#009194") + labs(x = "Reference",y = "Prediction") + scale_x_discrete(labels=c("0","1")) + scale_y_discrete(labels=c("1","0"))
dev.off()

write.table(cm, file = "aic_cm.csv",sep=",")
