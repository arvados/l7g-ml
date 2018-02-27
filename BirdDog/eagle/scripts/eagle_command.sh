#! /bin/bash
# Using absolute paths in this script

~/eagle/Eagle_v2.3.4/eagle \
    --geneticMapFile=/home/keldin/eagle/Eagle_v2.3.4/tables/genetic_map_hg19_withX.txt.gz \
    --vcfRef=/home/keldin/eagle/data/onekgenomes_sarah/chr19.1kg.phase3.v5a.vcf.gz \
    --vcfTarget=/home/keldin/eagle/data/giab/giab_chr19_unphased.vcf.gz \
    --vcfOutFormat=z \
    --outPrefix=giab_chr19_phased \
