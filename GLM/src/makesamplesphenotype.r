#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

# Load samples file
sampledata <- read.csv(args[1], header=FALSE)
names(sampledata) <- c("index", "SampleID", "AD", "status")

# Load phenotype files
phenotype_dfs <- lapply(list.files(args[2], full.names=TRUE), read.csv, sep="\t", stringsAsFactors=FALSE)
dfp <- do.call(rbind, phenotype_dfs)
dfp <- dfp[c("SampleID", "Sex", "Age_baseline")]
# Merge with sampledata
dfm = merge(sampledata, dfp, by="SampleID")
dfm <- dfm[order(dfm$index),]
# Normalize age
dfm$Age_normalized <- dfm$Age_baseline
dfm$Age_normalized[dfm$Age_normalized == "90+"] <- "90"
dfm$Age_normalized <- as.numeric(dfm$Age_normalized)
dfm$Age_normalized[is.na(dfm$Age_normalized)] <- mean(dfm$Age_normalized, na.rm=TRUE)
Age_scaled = scale(dfm$Age_normalized)
dfm$Age_normalized <- scale(dfm$Age_normalized, center=attr(Age_scaled, "scaled:center"), scale=attr(Age_scaled, "scaled:scale"))

fileConn <- file("samplesphenotype.tsv", "w")
write.table(dfm, fileConn, sep= "\t", row.names = FALSE, quote=FALSE)
close(fileConn)
