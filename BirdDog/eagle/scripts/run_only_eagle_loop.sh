#! /bin/bash

# Relevant collection for ref: su92l-4zz18-9fu11mizta7zmtu
#b7cd392bc4aa229c3c771b496e79628+9990 
ref_dir="/home/keldin/rwkeep/by_id/ba7cd392bc4aa229c3c771b496e79628+9990"
target_dir="/home/keldin/eagle/data/pgp_sarah"
eagle_dir="/home/keldin/eagle/Eagle_v2.3.4"
text_output_dir="/home/keldin/eagle/data/text_output"

# Exclude Y and M for now because ref panel does not have them.
# Will address later.
#all_chroms=(1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 X)
all_chroms=(19 20 21 X)
length=${#all_chroms[@]}
for ((i=0;i<length;i++)); do
	chrom_num=${all_chroms[i]}
	ref_file="chr$chrom_num.1kg.phase3.v5a.vcf.gz"
	echo $ref_file
	$eagle_dir/eagle \
	--geneticMapFile=$eagle_dir/tables/genetic_map_hg19_withX.txt.gz \
	--vcfRef=$ref_dir/$ref_file \
	--vcfTarget=$target_dir/var-GS12877-1100-37-ASMgffgz_FinalAll.vcf.gz \
	--vcfOutFormat=z \
	--outPrefix=GS12877_phased_chr$chrom_num \
	> $text_output_dir/from_run_on_chr$chrom_num  
done
