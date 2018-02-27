#! /bin/bash


# * Read in sample file
# * Decompress sample file with bgzip
# * Use awk to remove chr from sample file 
# * Use bcftools to split up multiallelics
# * Recompress using bgzip
# * Use tabix to create index file for sample
# * Loop through all chromosomes in reference
#	* Read in chromosome
#	* Use tabix to create index file for reference
#	* Run eagle on chrom

ref_dir=$1
target_vcf=$2
eagle_dir=/Eagle_v2.3.4

# Print header lines from original sample file for sanity check
echo Head from original sample file...
zcat $target_vcf | head

# Decompress sample file
echo Decompressing...
bgzip --decompress --stdout \
$target_vcf > a.vcf

# Use sed to remove chr from sample file
echo sed...
cat a.vcf | sed 's/chr//g' > b.vcf

# Use bcftools to split up multiallelics
echo bcftools...
head b.vcf
bcftools norm --multiallelics -both --output c.vcf b.vcf 

# Recompress using bgzip
echo Compressing...
bgzip --stdout c.vcf > c.vcf.gz

# Use tabix to create index file for sample
echo Indexing...
tabix --preset vcf c.vcf.gz

# Exclude Y and M for now because ref panel does not have them.
# Will address later.
#all_chroms=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X)
echo Phasing...
all_chroms="19 20 21 X"
for chrom_num in $all_chroms;
do	
	echo Chromosome $chrom_num ...
	ref_path=$ref_dir/"chr$chrom_num.1kg.phase3.v5a.vcf.gz"
	echo $ref_path
	eagle \
	--geneticMapFile=$eagle_dir/tables/genetic_map_hg19_withX.txt.gz \
	--vcfRef=$ref_path \
	--vcfTarget=c.vcf.gz \
	--vcfOutFormat=z \
	--outPrefix=GS12877_phased_chr$chrom_num
done
