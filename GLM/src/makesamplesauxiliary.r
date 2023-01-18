#!/usr/bin/env Rscript

library(reticulate)
np <- import("numpy")

args = commandArgs(trailingOnly=TRUE)

# Load samples file
sampledata <- read.csv(args[1], header=TRUE)

# Load phenotype files
phenotype_dfs <- lapply(list.files(args[2], full.names=TRUE), read.csv, sep="\t", stringsAsFactors=FALSE)
dfp <- do.call(rbind, phenotype_dfs)
dfp <- dfp[c("SampleID", "Sex", "Age_baseline")]
# Load pca file
pca <- np$load(args[3])
pca <- pca[,1:5]
pca <- as.data.frame(pca)
names(pca) <- c("pca1", "pca2", "pca3", "pca4", "pca5")
# Add phenotype and pca to sampledata
dfm <- merge(sampledata, dfp, by="SampleID", all.x=TRUE)
dfm <- dfm[order(dfm$Index),]
dfm <- cbind(dfm, pca)
# Remove non-CaseControl samples
dfm <- dfm[!is.na(sampledata$CaseControl),]
# Reorder Index
dfm$Index <- 0:(nrow(dfm)-1)

# Normalize age
dfm$Age_normalized <- dfm$Age_baseline
dfm$Age_normalized[dfm$Age_normalized == "90+"] <- "90"
dfm$Age_normalized <- as.numeric(dfm$Age_normalized)
dfm$Age_normalized[is.na(dfm$Age_normalized)] <- mean(dfm$Age_normalized, na.rm=TRUE)
Age_scaled = scale(dfm$Age_normalized)
dfm$Age_normalized <- scale(dfm$Age_normalized, center=attr(Age_scaled, "scaled:center"), scale=attr(Age_scaled, "scaled:scale"))

# Normalize pca components
for (p in names(pca)) {
  pn <- paste0(p, "_normalized")
  pca_scaled = scale(dfm[p])
  dfm[pn] <- scale(dfm[p], center=attr(pca_scaled, "scaled:center"), scale=attr(pca_scaled, "scaled:scale"))
}

dfm <- dfm[c("Index", "SampleID", "CaseControl", "TrainingValidation", "Sex", "Age_normalized", "pca1_normalized", "pca2_normalized", "pca3_normalized", "pca4_normalized", "pca5_normalized")]

fileConn <- file("samplesauxiliary.tsv", "w")
write.table(dfm, fileConn, sep= "\t", row.names=FALSE, quote=FALSE)
close(fileConn)
