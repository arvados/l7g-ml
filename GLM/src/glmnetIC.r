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
Xrc <- np$load(args[1])
Xrc <- as.matrix(Xrc)
Xdim <- dim(Xrc)

Xdata <- matrix(data = 1, nrow = 1, ncol = Xdim[2])
row_ind = as.matrix(Xrc[1,])
col_ind = as.matrix(Xrc[2,])

# Make them into an integer vector
row_ind <- as.integer(row_ind) + 1
col_ind <- as.integer(col_ind) + 1

# Create a new sparse matrix

Xdata <- as.numeric(Xdata)
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


# Adaptive Lasso
set.seed(999)


# Weighning, if optioned
fraction_0 <- rep(1 - sum(y == 0) / length(y), sum(y == 0))
fraction_1 <- rep(1 - sum(y == 1) / length(y), sum(y == 1))
# assign that value to a "weights" vector

wtrain <- rep(1,length(y))

wtrain[y == 0] <- fraction_0
wtrain[y == 1] <- fraction_1

#cv.ridge <- cv.glmnet(Xmat, y, family='binomial', alpha=0, parallel=TRUE, standardize=FALSE,intercept = TRUE, weights=wtrain)

#print(cv.ridge)

#w3 <- 1/abs(matrix(coef(cv.ridge, s=cv.ridge$lambda.min)
#                   [, 1][2:(ncol(Xmat)+1)] ))^gamma ## Using gamma = 2 

#w3[w3[,1] == Inf] <- 999999999 ## Replacing values estimated as Infinite for 999999999


reg.fit <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=1, intercept=TRUE, standardize=FALSE, type.measure='class', weights=wtrain) #, penalty.factor=w3)

coef.beta = rbind(reg.fit$a0,as.matrix(reg.fit$beta))  # extract coefficients at all values of lambda,  including the intercept

n = nrow(Xmat)
p = ncol(Xmat)
gamma.ebic = 0.50

dev = deviance(reg.fit)
reg.df = reg.fit$df
aic_obj = dev + 2 * reg.df
bic_obj = dev + log(n) * reg.df
ebic_obj = dev + log(n) * reg.df + 4 * gamma.ebic * reg.df * log(p)

lambda.ind = which.min(bic_obj)
coef.beta = coef.beta[, lambda.ind]
lambda = reg.fit$lambda[lambda.ind]
lamb = reg.fit$lambda

results <- data.frame(x = lamb, y = bic_obj)

coefVec = coef.beta[-1]
#coefVec = coef.beta
idxnzmin <- which(coefVec !=0)
nznumbmin <- coefVec[idxnzmin]

# Calculate Path, Step and Phase related to non-zero coefficents 

filename <- paste0('glmnet_lasso_bic.txt' )
fileConn <- file(filename, "w")


dataF_min <- data.frame("nonnzerocoefs_min" = nznumbmin,  "tag" = tags[idxnzmin], "variant" = varvals[idxnzmin],"zygosity"=zygosity[idxnzmin])
o <- order(abs(dataF_min$nonnzerocoefs_min), decreasing = TRUE)
dataF_min <- dataF_min[o,]

write.table(dataF_min, fileConn, sep= "\t", row.names = FALSE)
close(fileConn)
