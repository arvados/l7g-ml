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
scipy <- import("scipy")
np <- import("numpy")

args = commandArgs(trailingOnly=TRUE)
weighted <- TRUE
set.seed(999)

#if (length(args) <= 8) {
#  stop("8 arguments must be supplied", call.=FALSE)
#}

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
zygosity <- as.vector(np$load(args[8]))
colorblood <- args[9]
type_measure <- args[10]

PCAlabel = 1000+seq(1, 20)

varvals = c(varvals,99,999,PCAlabel)

nsample = round(.90*length(y))
train = sample(seq(length(y)),nsample,replace=FALSE)
ytrain = y[train]

fraction_0 <- rep(1 - sum(ytrain == 0) / length(ytrain), sum(ytrain == 0))
fraction_1 <- rep(1 - sum(ytrain == 1) / length(ytrain), sum(ytrain == 1))
# assign that value to a "weights" vector

weights <- rep(1,length(ytrain))

if (weighted == TRUE) {
  weights[y == 0] <- fraction_0
  weights[y == 1] <- fraction_1
} else {
  weights <- rep(1, length(ytrain))
}

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
set.seed(999)
cv.ridge <- cv.glmnet(Xmat[train,], y[train], family='binomial', alpha=0, parallel=TRUE, standardize=FALSE,intercept = TRUE,weights=weights[train])
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^2 ## Using gamma = 2 
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999
# Keep PCA components
#w3[(length(w3) - 19):length(w3),1] <- 0

# Adaptive Lasso

reg.fit <- glmnet(Xmat[train,], y[train], family='binomial', alpha=1, intercept=TRUE, standardize=FALSE, penalty.factor=w3,weights=weights[train])

coef.beta = rbind(reg.fit$a0,as.matrix(reg.fit$beta))  # extract coefficients at all values of lambda,  including the intercept

n = nrow(Xmat[train,])
p = ncol(Xmat[train,])
gamma.ebic = 0.50

dev = deviance(reg.fit)
reg.df = reg.fit$df
aic_obj = dev + 2 * reg.df
bic_obj = dev + log(n) * reg.df
ebic_obj = dev + log(n) * reg.df + 4 * gamma.ebic * reg.df * log(p)

lambda.ind = which.min(aic_obj)
coef.beta_aic = coef.beta[, lambda.ind]
lambda = reg.fit$lambda[lambda.ind]
lamb = reg.fit$lambda

results <- data.frame(x = lamb, y = ebic_obj)

coefVec = coef.beta_aic[-1]
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

filename <- paste0('glmnet_lasso_aic_',colorblood,'.txt' )

fileConn <- file(filename, "w")
dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin], "zygosity" = zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

ytest = y[-train]

fraction_0 <- rep(1 - sum(ytest == 0) / length(ytest), sum(ytest == 0))
fraction_1 <- rep(1 - sum(ytest == 1) / length(ytest), sum(ytest == 1))
# assign that value to a "weights" vector

weights <- rep(1,length(ytest))

if (weighted == TRUE) {
  weights[y == 0] <- fraction_0
  weights[y == 1] <- fraction_1
} else {
  weights <- rep(1, length(ytest))
}

idaic = match(reg.fit$lambda[lambda.ind],reg.fit$lambda)
cm = confusion.glmnet(reg.fit, newx = Xmat[-train,], newy = y[-train], family='binomial',weights=weights)[[idaic]]

print(cm)
write.table(cm, file = "aic_cm.csv",sep=",")

lambda.ind = which.min(bic_obj)
coef.beta_bic = coef.beta[, lambda.ind]
lambda = reg.fit$lambda[lambda.ind]
lamb = reg.fit$lambda

results <- data.frame(x = lamb, y = ebic_obj)

coefVec = coef.beta_bic[-1]
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
dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin], "zygosity" = zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
idaic = match(reg.fit$lambda[lambda.ind],reg.fit$lambda)
cm = confusion.glmnet(reg.fit, newx = Xmat[-train,], newy = y[-train], family='binomial',weights=weights)[[idaic]]

print(cm)

png('confusion_matrix_bic.png')
ggplot(as.data.frame(cm), aes(Predicted,sort(True,decreasing = T), fill= Freq)) + geom_tile() + geom_text(aes(label=Freq)) + scale_fill_gradient(low="white", high="#009194") + labs(x = "Reference",y = "Prediction") + scale_x_discrete(labels=c("0","1")) + scale_y_discrete(labels=c("1","0"))
dev.off()                                      
