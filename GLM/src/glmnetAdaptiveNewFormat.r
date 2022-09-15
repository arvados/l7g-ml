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
np <- import("numpy")

args = commandArgs(trailingOnly=TRUE)
# 11057 x 98692
Xrc <- np$load(args[1])
Xrc <- as.matrix(Xrc)
Xdim <- dim(Xrc)
print(Xdim)

Xdata <- matrix(data = 1, nrow = 1, ncol = Xdim[2])
row_ind = as.matrix(Xrc[1,])
col_ind = as.matrix(Xrc[2,])


# Make them into an integer vector
row_ind <- as.integer(row_ind) + 1
col_ind <- as.integer(col_ind) + 1


# Create a new sparse matrix

Xdata <- as.numeric(Xdata)
#row_ind <- as.numeric(row_ind)
#col_ind <- as.numeric(col_ind)

Xmat <- sparseMatrix(row_ind,col_ind,x = Xdata)
print(dim(Xmat))
rm(row_ind,col_ind,Xdata)

# Load the y array and make into vector in R
coldata <- np$load(args[2]) 
coldata <- as.matrix(coldata)
#coldata <- as.numeric(coldata)

sampledata = read.csv(args[3],header=FALSE)
sampledata = as.matrix(sampledata)

print(dim(sampledata))
print(dim(coldata))
		      
y <- as.numeric(sampledata[,3])
y <- as.matrix(y)

print(dim(y))

# col data cols --tag, tile variant, zygosity with heterozygous = 0 and homozygous = 1, p-value * 1e6

tags <- as.matrix(as.numeric(coldata[1,]))
varvals <- as.matrix(as.numeric(coldata[2,]))
zygosity <- as.matrix(as.numeric(coldata[3,]))

print(dim(tags))
print(tags)


# Use Adaptive Lasso for regularization
# Use Ridge Regression to create the Adaptive Weights Vector

cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE,intercept = TRUE)
w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
                   [, 1][2:(ncol(Xmat)+1)] ))^2 ## Using gamma = 2 
w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999

# Adaptive Lasso
set.seed(999)

cv.lasso.adaptive <- cv.glmnet(Xmat, y, family='binomial', alpha=1, nfolds = 10, parallel=TRUE, intercept=TRUE, standardize=FALSE, type.measure='class', penalty.factor=w3)

plotname_adaptive <- paste0('glmnet_lasso.png')
png(plotname_adaptive)
plot(cv.lasso.adaptive)
dev.off()

coefVec <- coef(cv.lasso.adaptive, s= "lambda.min")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 

filename <- paste0('glmnet_lasso_min.txt' )
fileConn <- file(filename, "w")

dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin,  "tag" = tags[idxnzmin], "variant" = varvals[idxnzmin],"zygosity"=zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)

