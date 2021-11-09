## Using R for an example to show to load the Tiled Data 
## and perform a simple GLM on the data.  Note: using R because GLMnet
## is much faster than scikitlearn for performing LASSO and finding optimial regularization

# Inorder to use Python
reticulate::use_python('/usr/local/bin/python3')
reticulate::py_discover_config()

# R libraries
library(Matrix)
library(foreach)
suppressMessages(library(glmnet))
library(reticulate)
library(methods)

# Python libraries
scipy <- import("scipy")
np <- import("numpy")

# Loading in Tiled Data
Xdata_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/X.npy'
Xrdata_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/Xr.npy'
Xcdata_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/Xc.npy' 
tilevariant_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/varvals.npy' 
tiletagnumber_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/tiletag.npy'
zygosity_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/zygosity.npy'
XPCA_file = '../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/XPCA.npy'

Xdata <- as.vector(np$load(Xdata_file))
Xr <- as.integer(as.vector(np$load(Xrdata_file))) + 1
Xc <- as.integer(as.vector(np$load(Xcdata_file))) + 1

XPCA <- as.vector(np$load(XPCA_file))
XPCA <- as(matrix(XPCA,nco =20,nrow=length(XPCA)/20),"sparseMatrix")

varvals <- as.integer(as.vector(np$load(tilevariant_file)))
tiletag <- as.integer(as.vector(np$load(tiletagnumber_file)))
zygosity <- as.integer(as.vector(np$load(zygosity_file)))

# Create a new sparse matrix
Xmat <- sparseMatrix(Xr,Xc,x = Xdata)

rm(Xr,Xc,Xdata) # Saving memory 

# Load the y array and make into vector in R
ynump <- np$load("../keep/by_id/2xpu4-4zz18-bmvaczs8gw7di41/y.npy")
y <- as.vector(ynump)

rm(ynump) # Saving memory

# Setting up test and train data (50-50)
dt = sort(sample(nrow(Xmat), nrow(Xmat)*0.5))
Xmat = cbind(Xmat,XPCA)
Xtrain <- Xmat[dt,]
Xtest <- Xmat[-dt,]
ytrain <- y[dt]
ytest <- y[-dt]

# Weights

fraction_0 <- rep(1 - sum(ytrain == 0) / length(ytrain), sum(ytrain == 0))
fraction_1 <- rep(1 - sum(ytrain == 1) / length(ytrain), sum(ytrain == 1))
# assign that value to a "weights" vector

wtrain <- rep(1,length(ytrain))

wtrain[ytrain == 0] <- fraction_0
wtrain[ytrain == 1] <- fraction_1

# Using LASSO 
cv.lasso.class <- cv.glmnet(Xtrain, ytrain, family='binomial', alpha=1, nfolds = 10, parallel=FALSE, keep=FALSE,standardize=FALSE, weights=wtrain, type.measure='class', trace.it=1)

# Plot and Save Figure 
png('regularization_lasso.png')
plot(cv.lasso.class)
dev.off()

# Assessing model
preds = predict(cv.lasso.class, newx = Xtest, s = "lambda.min")
outcome = assess.glmnet(preds, newy = ytest, family = "binomial")
print(outcome)

# Confusion Matrix
cm = confusion.glmnet(cv.lasso.class, newx = Xtest, newy = ytest, s = "lambda.min")
print(cm)

# Using glm on 50% of data to get an estimate of p values for each selected feature


# Find regularization and nonzero coefficents corresponding to minimum "error"
coefVec <- coef(cv.lasso.class, s= "lambda.min")
coefVec <- coefVec[-1]
idxnzmin <- which(coefVec !=0)
nzcoefVal <- coefVec[idxnzmin]

# Sort to find largest coefficent values, collecting tiledata in dataframe
varvals <- varvals[idxnzmin] 
zygosity <- zygosity[idxnzmin]
tiletag <- tiletag[idxnzmin]

tiledata <- data.frame("nonnzerocoefs" = nzcoefVal, "tileta" = tiletag, "varvals" = varvals)
idxsort <- order(abs(tiledata$nonnzerocoefs), decreasing = TRUE)
tiledata <- tiledata[idxsort,]
print(tiledata)

# Finding HGVS annotations for top tile variants in model
