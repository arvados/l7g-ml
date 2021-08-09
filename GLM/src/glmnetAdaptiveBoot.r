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

# xstr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/X.npz"
x <- as.vector(np$load(args[1]))

# Make them into an integer vector
i <- as.integer(as.vector(np$load(args[2]))) + 1
j <- as.integer(as.vector(np$load(args[3]))) + 1

# Create a new sparse matrix
Xmat <- sparseMatrix(i,j,x = x)

rm(i,j,x)

# Load the y array and make into vector in R
ynump <- np$load(args[4]) 
y <- as.vector(ynump)

pathdataOH <- as.vector(np$load(args[5]))
oldpath <- as.vector(np$load(args[6]))
varvals <- as.vector(np$load(args[7]))
zygosity <- as.vector(np$load(args[8]))
gamma <- args[9]
colorblood <- args[10]
type_measure <- args[11]
forcePCA <- args[12]
weighted <- args[13]
seedinput <- args[14]

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
checktype <- typeof(seedinput)
print(checktype)

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

# Test and Train Sampling
#nsample = round(.90*length(y))
#train = sample(seq(length(y)),nsample,replace=FALSE)
#ytrain = y[train]
#Xtrain = Xmat[train,]
#ytest = y[-train]
#Xtest = Xmat[-train,]
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
# Adaptive Lasso

cv.lasso.adaptive <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=1, nfolds = 10, parallel=TRUE, intercept=TRUE, standardize=FALSE, type.measure=type_measure, penalty.factor=w3,weights=wtrain)

# Plotting CV,Lambda plot
plotname_adaptive <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'.png')
png(plotname_adaptive)
plot(cv.lasso.adaptive)
dev.off()

# Output model params minimum lambda
coefVec <- coef(cv.lasso.adaptive, s= "lambda.min")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

tile_path <- as.vector(np$trunc(coefPathsMin/(16**5)))
tile_step <- as.vector(np$trunc((coefPathsMin - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

filename <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'min.txt' )
fileConn <- file(filename, "w")

dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin, "tile_path_min" = tile_path, "tile_step_min" = tile_step, "oldpath_min" = oldpath[idxnzmin], "varvals_min" = varvals[idxnzmin],"zygosity_min" = zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

# Output model params for 1std lambda

coefVse <- coef(cv.lasso.adaptive, s="lambda.1se")
coefVse <- coefVse[-1]

idxnzse <- which(coefVse !=0)
nznumbse <- coefVse[idxnzse]
coefPaths1st <- pathdataOH[idxnzse] 

tile_path <- as.vector(np$trunc(coefPaths1st/(16**5)))
tile_step <- as.vector(np$trunc((coefPaths1st - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPaths1st- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

dataF_1se <- data.frame("nonnzerocoefs_1se" = nznumbse, "tile_path_1se" = tile_path, "tile_step_1se" = tile_step, "oldpath_1se" = oldpath[idxnzse], "varvals_1se" = varvals[idxnzse],"zygosity_1se" = zygosity[idxnzse])
o_1se <- order(abs(dataF_1se$nonnzerocoefs_1se), decreasing = TRUE)
dataF_1se <- dataF_1se[o_1se,]

filename1 <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'1se.txt' )
fileConn1 <- file(filename1, "w")
write.table(dataF_1se, fileConn1, sep= "\t", row.names = FALSE)
close(fileConn1)
