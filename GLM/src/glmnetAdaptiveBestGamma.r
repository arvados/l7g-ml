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

if (length(args) <= 8) {
  stop("8 arguments must be supplied", call.=FALSE)
}

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
colorblood <- args[8]
type_measure <- args[9]

# Look at range of gammas to find "best" value 

#gamma = 2.0

gammamin<-0.5
gammastep<-0.5
gammamax<-5

gamma_seq<-seq(gammamin,gammamax,gammastep)
nzero_seq<-rep(NA, length(gamma_seq)) 
cvm_seq<-rep(NA, length(gamma_seq))
cvsd_seq<-rep(NA, length(gamma_seq))

for (j in gamma_seq){
   # Use Adaptive Lasso for regularization
   # Use Ridge Regression to create the Adaptive Weights Vector
   set.seed(999)
   cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE)
   w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^j # 
   w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999

   # Adaptive Lasso
   set.seed(999)
   cv.lasso.auc <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 5, parallel=TRUE, standardize=FALSE, type.measure='auc', penalty.factor=w3)
   cv.lasso.class <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 5, parallel=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3)

   idminclass <- match(cv.lasso.class$lambda.min, cv.lasso.class$lambda)
   cvsdclass <-cv.lasso.class$cvsd[idminclass]
   cvmclass <-cv.lasso.class$cvm[idminclass]
   nzeroclass <- cv.lasso.class$nzero[idminclass]

   print(cvsdclass,digits=3) 
   print(cvmclass,digits=3)
   print(nzeroclass,digits=3)

   }

# Final plots and finding non-zero coefficents and tile locations


