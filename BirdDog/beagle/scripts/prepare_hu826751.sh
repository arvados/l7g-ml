#! /bin/bash

# get chrom 19
bzcat ../PGP-Harvard-hu826751-var.vcf.bz2 | bgzip > pgp_hu826751.vcf.gz
tabix --preset=vcf pgp_hu826751.vcf.gz
bcftools filter --regions chr19 --output-type z --output pgp_hu826751_chr19.vcf.gz pgp_hu826751.vcf.gz


# remove chr

