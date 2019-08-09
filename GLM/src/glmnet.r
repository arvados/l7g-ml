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
#cross validate and return the best lambda
maxlog <- 0
minlog <- -2
lamvals <- 10^seq(maxlog,minlog, length=100)
cvfit <- cv.glmnet(Xmat,y, family = "binomial", type.measure = type_measure, nfolds = 5, lambda=lamvals)

plotname <- paste0('glmnet_',colorblood,'_',type_measure,'.png')
png(plotname)
plot(cvfit)
dev.off()

filename <- paste0('glmnet_',colorblood,'_',type_measure,'min.txt' ) 
fileConn <- file(filename)

idxnzmin <- which(coef(cvfit,s="lambda.min") !=0)
idxnzmin <- idxnzmin[-1]
nznumbmin <- coef(cvfit,s="lambda.min")[idxnzmin]
coefPaths <- pathdataOH[idxnzmin]
#From equation Sarah has, basically reversing encoding: 
tile_path <- np$trunc(coefPaths/(16**5))
tile_step <- np$trunc((coefPaths - tile_path*16**5)/2)
tile_phase <- np$trunc((coefPaths- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

writeLines(c("Tile Location (min): ", tile_loc,"Nonnzero Coefs (min): ", nznumbmin,"Old Path (min): ", oldpath[idxnzmin],"Varvals (min): ", varvals[idxnzmin]), fileConn)
close(fileConn)

filename <- paste0('glmnet_',colorblood,'_',type_measure,'1se.txt' ) 
fileConn <- file(filename)

idxnzse <- which(coef(cvfit,s="lambda.1se") !=0)
idxnzse <- idxnzse[-1]
nznumbse <- coef(cvfit,s="lambda.1se")[idxnzse]
coefPaths <- pathdataOH[idxnzse]

#From equation Sarah has, basically reversing encoding: 
tile_path <- np$trunc(coefPaths/(16**5))
tile_step <- np$trunc((coefPaths - tile_path*16**5)/2)
tile_phase <- np$trunc((coefPaths- tile_path*16**5 - 2*tile_step))
tup <- tuple(tile_path, tile_step)
tile_loc <- np$column_stack(tup)

writeLines(c("Tile Location (1se): ", tile_loc,"Nonnzero Coefs (1se): ", nznumbse,"Old Path (1se): ", oldpath[idxnzse],"Varvals (1se): ", varvals[idxnzse]), fileConn)
close(fileConn)
