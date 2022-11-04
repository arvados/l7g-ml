#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

# Load samples file
sampledata <- read.csv(args[1], header=FALSE)
names(sampledata) <- c("index", "SampleID", "AD", "status")

# Load phenotype files
phenotype_dfs <- lapply(list.files(args[2], full.names=TRUE), read.csv, sep="\t", stringsAsFactors=FALSE)
dfp <- do.call(rbind, phenotype_dfs)
dfp <- dfp[c("SampleID", "Sex", "Age_baseline", "Ethnicity", "Race")]
# Merge with sampledata
dfm <- merge(sampledata, dfp, by="SampleID")
dfm <- dfm[order(dfm$index),]
# Fill in Ethnicity and one hot encode Race
dfm$Ethnicity[is.na(dfm$Ethnicity)] <- 0
races <- c("American_Indian_Alaska_Native", "Asian",	"Native_Hawaiian_or_Other_Pacific_Islander", "Black_or_African_American", "White", "Other")
dfm[races] <- 0
for (i in seq_along(races)) {
  dfm[[races[i]]][!is.na(dfm$Race) & dfm$Race == i] <- 1
}
# Normalize age
dfm$Age_normalized <- dfm$Age_baseline
dfm$Age_normalized[dfm$Age_normalized == "90+"] <- "90"
dfm$Age_normalized <- as.numeric(dfm$Age_normalized)
dfm$Age_normalized[is.na(dfm$Age_normalized)] <- mean(dfm$Age_normalized, na.rm=TRUE)
Age_scaled = scale(dfm$Age_normalized)
dfm$Age_normalized <- scale(dfm$Age_normalized, center=attr(Age_scaled, "scaled:center"), scale=attr(Age_scaled, "scaled:scale"))

dfm <- dfm[append(c("index", "SampleID", "AD", "status", "Sex", "Age_normalized", "Ethnicity"), races)]
fileConn <- file("samplesphenotype.tsv", "w")
write.table(dfm, fileConn, sep= "\t", row.names = FALSE, quote=FALSE)
close(fileConn)
