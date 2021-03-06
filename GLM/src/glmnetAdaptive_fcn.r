adaptiveGLM <- function(Xfile,ifile,jfile,yfile,pathfile,oldpathfile,varvalsfile,pheno,measure) {
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

#args = commandArgs(trailingOnly=TRUE)

#if (length(args) <= 8) {
#  stop("8 arguments must be supplied", call.=FALSE)
#}

# xstr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/X.npz"
x <- as.vector(np$load(args[Xfile]))

# Make them into an integer vector
i <- as.integer(as.vector(np$load(args[ifile]))) + 1
j <- as.integer(as.vector(np$load(args[jfile]))) + 1

# Create a new sparse matrix
Xmat <- sparseMatrix(i,j,x = x)

rm(i,j,x)

# Load the y array and make into vector in R
ynump <- np$load(args[yfile]) 
y <- as.vector(ynump)

pathdataOH <- as.vector(np$load(args[pathfile]))
oldpath <- as.vector(np$load(args[oldpathfile]))
varvals <- as.vector(np$load(args[varvalsfile]))
colorblood <- args[pheno]
type_measure <- args[measure]

# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector
set.seed(999)
cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE)
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^2 ## Using gamma = 2 
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999

# Adaptive Lasso
set.seed(999)
cv.lasso.auc <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 5, parallel=TRUE, standardize=FALSE, type.measure='auc', penalty.factor=w3)

cv.lasso.class <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 5, parallel=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3)
plotname_class <- paste0('glmnet_lasso_',colorblood,'_class.png')
png(plotname_class)
plot(cv.lasso.class)
dev.off()

plotname <- paste0('glmnet_lasso_',colorblood,'_auc','.png')
png(plotname)
plot(cv.lasso.auc)
dev.off()

coefVec <- coef(cv.lasso.class, s= "lambda.min")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
sizeCoefMin <- length(coef(cv.lasso.class,s="lambda.min"))
nznumbmin <- coefVec[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 
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

coefVse <- coef(cv.lasso.class, s="lambda.1se")
coefVse <- coefVse[-1]

idxnzse <- which(coefVse !=0)
nznumbse <- coefVse[idxnzse]
coefPaths1st <- pathdataOH[idxnzse] 

tile_path <- as.vector(np$trunc(coefPaths1st/(16**5)))
tile_step <- as.vector(np$trunc((coefPaths1st - tile_path*16**5)/2))
tile_phase <- np$trunc((coefPaths1st- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

dataF_1se <- data.frame("nonnzerocoefs_1se" = nznumbse, "tile_path_1se" = tile_path, "tile_step_1se" = tile_step, "oldpath_1se" = oldpath[idxnzse], "varvals_1se" = varvals[idxnzse])
o_1se <- order(abs(dataF_1se$nonnzerocoefs_1se), decreasing = TRUE)
dataF_1se <- dataF_1se[o_1se,]

return <- dataF_1se

filename1 <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'1se.txt' )
fileConn1 <- file(filename1, "w")
write.table(dataF_1se, fileConn1, sep= "\t", row.names = FALSE)
close(fileConn1) }
