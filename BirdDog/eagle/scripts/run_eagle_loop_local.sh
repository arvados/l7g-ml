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


# Relevant collection for ref: su92l-4zz18-9fu11mizta7zmtu
#b7cd392bc4aa229c3c771b496e79628+9990 
ref_dir="/home/keldin/rwkeep/by_id/ba7cd392bc4aa229c3c771b496e79628+9990"
target_dir="/home/keldin/rwkeep/by_id/74e87bded6216c65cc76d84864d40a03+8948"
eagle_dir="/home/keldin/eagle/Eagle_v2.3.4"
text_output_dir="/home/keldin/eagle/data/text_output"

test_sample_a="var-GS12877-1100-37-ASMgffgz_FinalAll_a.vcf"
test_sample_b="var-GS12877-1100-37-ASMgffgz_FinalAll_b.vcf"


# Print header lines from original sample file for sanity check
echo Head from original sample file...
zcat $target_dir/var-GS12877-1100-37-ASMgffgz_FinalAll.vcf.gz | head

# Decompress sample file
echo Decompressing...
bgzip --decompress --stdout \
$target_dir/var-GS12877-1100-37-ASMgffgz_FinalAll.vcf.gz > $test_sample_a

# Use sed to remove chr from sample file
echo sed...
cat $test_sample_a | sed 's/chr//g' > $test_sample_b

# Use bcftools to split up multiallelics
echo bcftools...
head $test_sample_b
bcftools norm --multiallelics -both --output $test_sample_a $test_sample_b

# Recompress using bgzip
echo Compressing...
bgzip --stdout $test_sample_a > $test_sample_b.gz

# Use tabix to create index file for sample
echo Indexing...
tabix --preset vcf $test_sample_b.gz

# Exclude Y and M for now because ref panel does not have them.
# Will address later.
#all_chroms=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X)
echo Phasing...
all_chroms=(19 20 21 X)
length=${#all_chroms[@]}
for ((i=0;i<length;i++)); do	
	chrom_num=${all_chroms[i]}
	echo Chromosome $chrom_num ...
	ref_file="chr$chrom_num.1kg.phase3.v5a.vcf.gz"
	echo $ref_file
	$eagle_dir/eagle \
	--geneticMapFile=$eagle_dir/tables/genetic_map_hg19_withX.txt.gz \
	--vcfRef=$ref_dir/$ref_file \
	--vcfTarget=$test_sample_b.gz \
	--vcfOutFormat=z \
	--outPrefix=GS12877_phased_chr$chrom_num \
	> $text_output_dir/from_run_on_chr$chrom_num  
done
