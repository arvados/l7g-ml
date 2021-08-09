#!/usr/bin/env Rscript
# install.packages("Matrix", repos = 'http://cran.us.r-project.org')
# install.packages("reticulate", repos = 'http://cran.us.r-project.org')

# Inorder to use Python
#reticulate::use_python('/usr/local/bin/python3')
#reticulate::py_discover_config()

# R libraries
library(Matrix)
library(foreach)
library(reticulate)
library(methods)
library(ggplot2)
library(mpath)

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

# Convert sparse to dense due to no sparse support 
rm(i,j,x)
Xmat <- as.matrix(Xmat)

# Load the y array and make into vector in R
ynump <- np$load(args[4]) 
y <- as.vector(ynump)

pathdataOH <- as.vector(np$load(args[5]))
oldpath <- as.vector(np$load(args[6]))
varvals <- as.vector(np$load(args[7]))
colorblood <- args[8]

nsample = round(.90*length(y))
train = sample(seq(length(y)),nsample,replace=FALSE)

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
set.seed(999)

w3 <- rep(1,ncol(Xmat))
#w3[(length(w3) - 19):length(w3)] <- 0

# Adaptive Lasso
set.seed(999)

findnan = apply(is.na(Xmat), 2, which)
print(findnan)

reg.fit <- cv.glmreg(Xmat, y, family='binomial', intercept=TRUE, standardize=FALSE,penalty='snet',alpha=1,y.keep=FALSE,x.keep=FALSE)

fit <- reg.fit$fit

coef.beta = coef(fit)[,reg.fit$lambda.which]
dev.off()

coefVec = coef.beta[-1]
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 
tile_path <- as.vector(np$trunc(coefPathsMin/(16**5)))
tile_step <- as.vector(np$trunc((coefPathsMin - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

filename <- paste0('glmnet_lasso_cv_',colorblood,'.txt' )
fileConn <- file(filename, "w")
dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)
