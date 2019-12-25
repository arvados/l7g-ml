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

if (length(args) <= 6) {
  stop("6 arguments must be supplied", call.=FALSE)
}

# xstr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/X.npz"
Xscp <- scipy$sparse$load_npz(args[1])
xind <- Xscp$nonzero()

# Make them into an integer vector
i <- as.integer(xind[[1]]) + 1
j <- as.integer(xind[[2]]) + 1

# Collect nonzero data and put as vector
x <- as.vector(Xscp$data)

# Create a new sparse matrix
Xmat <- sparseMatrix(i,j,x = x)

rm(i,j,x)

# Load the y array and make into vector in R
# ystr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/y.npy"
ynump <- np$load(args[2]) 
y <- as.vector(ynump)

# oldpath_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/oldpath.npy"
# pathdata_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/pathdataOH.npy"
# varvals_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/varvals.npy"

pathdataOH <- as.vector(np$load(args[3]))
oldpath <- as.vector(np$load(args[4]))
varvals <- as.vector(np$load(args[5]))
colorblood <- args[6]
type_measure <- args[7]

#adaptiveLasso
#Ridge Regression to create the Adaptive Weights Vector
set.seed(999)
cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE)
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^2.0 ## Using gamma = .5
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999
w3[(length(w3)-15):length(w3),1] <- 0 ## Keeping last 15 PCA components

rm(cv.ridge)
#Adaptive Lasso
set.seed(999)
cv.lasso <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 10, parallel=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3)

plotname <- paste0('glmnet_lasso_',colorblood,'_class','.png')
png(plotname)
plot(cv.lasso)
dev.off()

plotname1 <- paste0('glmnet_lasso_coefficients_',colorblood, '_class.png')
png(plotname1)
plot(cv.lasso$glmnet.fit, xvar="lambda", label=TRUE)
abline(v = log(cv.lasso$lambda.min))
dev.off()

coefVec <- coef(cv.lasso, s= "lambda.1se")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
sizeCoefMin <- length(coef(cv.lasso,s="lambda.1se"))
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]


#From equation Sarah has, basically reversing encoding: 
tile_path <- as.vector(np$trunc(coefPathsMin/(16**5)))
tile_step <- as.vector(np$trunc((coefPathsMin - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

filename <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'min.txt' )
fileConn <- file(filename, "w")

dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

