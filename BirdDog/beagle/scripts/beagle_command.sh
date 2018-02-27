#! /bin/bash

# Directory of genetic map
#mapdir=~/keep/by_id/b1b4015340fb9ef47ad5bdc6ee7bd1f4+2008
mapdir=/home/keldin/beagle/map

# Directory of reference panel
#refpaneldir=~/keep/by_id/ba7cd392bc4aa229c3c771b496e79628+9990
# ^ this is actually from eagle ref panel, which is basically
# the same as beagle panel
refpaneldir=/home/keldin/eagle/data/onekgenomes_sarah


# bird-dog tests collection
# su92l-j7d0g-siv7q4gt8h8ve5m



java -jar /home/keldin/beagle/beagle.08Jun17.d8b.jar \
	map=$mapdir/plink.chr19.GRCh37.map \
	ref=$refpaneldir/chr19.1kg.phase3.v5a.vcf.gz \
	gt=/home/keldin/beagle/targets/concise_giab_chr19_pr.vcf.gz \
	out=output.giab.imputed
#	nthreads=
#	window=
#	overlap=
