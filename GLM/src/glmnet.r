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

# Load the y array and make into vector in R
# ystr <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/y.npy"
ynump <- np$load(args[2]) 
y <- as.vector(ynump)

# oldpath_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/oldpath.npy"
# pathdata_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/pathdataOH.npy"
# varvals_file <- "/data-sdd/owebb/keep/by_id/su92l-4zz18-jq2eftdx22eow6s/varvals.npy"

oldpath <- np$load(args[3])
pathdataOH <- np$load(args[4])
varvals <- np$load(args[5])
colorblood <- args[6]
type_measure <- args[7]

#adaptiveLasso
#Ridge Regression to create the Adaptive Weights Vector
set.seed(999)
cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=TRUE)
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(x)+1)] ))^1 ## Using gamma = 1
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999

#Adaptive Lasso
set.seed(999)
cv.lasso <- cv.glmnet(Xmat, y, family='binomial', alpha=1, parallel=TRUE, standardize=TRUE, type.measure='auc', penalty.factor=w3)

plotname <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'.png')
png(plotname)
plot(cv.lasso)
plot(cv.lasso$glmnet.fit, xvar="lambda", label=TRUE)
abline(v = log(cv.lasso$lambda.min))
dev.off()

filename <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'min.txt' )
fileConn <- file(filename)

idxnzmin <- which(coef(cv.lasso,s="lambda.min") !=0)
idxnzmin <- idxnzmin[-1] #why drop top one?
nznumbmin <- coef(cv.lasso,s="lambda.min")[idxnzmin]
coefPathsMin <- pathdataOH[idxnzmin]

#coef <- coef(cv.lasso, s='lambda.min')
#selected_attributes <- (coef@i[-1]+1) ## Considering the structure of the data frame dataF as shown earlier

#I chose to get the coef with lambda.min because that is what was previously done. 
#This caputures the lambda values with the min cross validation error. instead of largest lambda st error within 1stdv of minimum 
#


#cross validate and return the best lambda
##maxlog <- 0
##minlog <- -2
##lamvals <- 10^seq(maxlog,minlog, length=100)
##cvfit <- cv.glmnet(Xmat,y, family = "binomial", type.measure = type_measure, nfolds = 5, lambda=lamvals)


#From equation Sarah has, basically reversing encoding: 
tile_path <- np$trunc(coefPathsMin/(16**5))
tile_step <- np$trunc((coefPathsMin - tile_path*16**5)/2)
tile_phase <- np$trunc((coefPathsMin- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

writeLines(c("Tile Location (min): ", tile_loc,"Nonnzero Coefs (min): ", nznumbmin,"Old Path (min): ", oldpath[idxnzmin],"Varvals (min): ", varvals[idxnzmin]), fileConn)
close(fileConn)

filename <- paste0('glmnet_lasso_',colorblood,'_',type_measure,'1se.txt' ) 
fileConn <- file(filename)

idxnzse <- which(coef(cv.lasso,s="lambda.1se") !=0)
idxnzse <- idxnzse[-1]
nznumbse <- coef(cv.lasso,s="lambda.1se")[idxnzse]
coefPaths1st <- pathdataOH[idxnzse] #should this be the same name as before? 

#From equation Sarah has, basically reversing encoding: 
tile_path <- np$trunc(coefPaths1st/(16**5))
tile_step <- np$trunc((coefPaths1st - tile_path*16**5)/2)
tile_phase <- np$trunc((coefPaths1st- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

writeLines(c("Tile Location (1se): ", tile_loc,"Nonnzero Coefs (1se): ", nznumbse,"Old Path (1se): ", oldpath[idxnzse],"Varvals (1se): ", varvals[idxnzse]), fileConn)
close(fileConn)
