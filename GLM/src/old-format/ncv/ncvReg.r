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
library(ncvreg)

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

# Convert sparse to dense due to no sparse support in nvcreg
rm(i,j,x)
Xmat <- as.matrix(Xmat)

# Load the y array and make into vector in R
ynump <- np$load(args[4]) 
y <- as.vector(ynump)

pathdataOH <- as.vector(np$load(args[5]))
oldpath <- as.vector(np$load(args[6]))
varvals <- as.vector(np$load(args[7]))
colorblood <- args[8]

# Use MCP for regularization
cv_fit <- cv.ncvreg(Xmat,y,family='binomial',alpha=1,gamma=35,returnX=FALSE,nfolds=5,trace=TRUE)

# Plotting variables sel vs mFDR (marginal false discovery rates)
plotname_fit<- paste0('cvfit_',colorblood,'.png')
png(plotname_fit)
par(mfrow=c(2,2))
plot(cv_fit, type='all')

#op <- par(mfcol=c(2,2))
#plot(pmfit)
#plot(pmfit, type="EF")
#plot(pmfit$fit)
#lam <- pmfit$fit$lambda
#pmfit.r <- perm.ncvreg(Xmat, y, permute='residuals')
#plot(pmfit.r, col="red")

dev.off()

coefVec <- coef(cv_fit, lambda=cv_fit$lambda.min,drop=TRUE)
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
sizeCoefMin <- length(coef(cv_fit, lambda=cv_fit$lambda.min, type="coefficents"))
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 
tile_path <- as.vector(np$trunc(coefPathsMin/(16**5)))
tile_step <- as.vector(np$trunc((coefPathsMin - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

filename <- paste0('ncvreg_',colorblood,'min.txt' )
fileConn <- file(filename, "w")

dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)
