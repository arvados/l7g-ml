#! /bin/bash
# beagledir=/home/keldin/beagle
# beagledir= /home/keldin/rwkeep/by_id/su92l-4zz18-vr9sw4frmxf29nm

# reference=/home/keldin/eagle/data/onekgenomes_sarah/homozygous_test.vcf.gz
# refdir=/home/keldin/keep/by_id/ba7cd392bc4aa229c3c771b496e79628+9990
# ^ this is actually from eagle ref panel, which is basically
# the same as beagle panel

# mapdir=/home/keldin/beagle/map
# /home/keldin/keep/by_id/b1b4015340fb9ef47ad5bdc6ee7bd1f4+2008

# bird-dog tests collection
# su92l-j7d0g-siv7q4gt8h8ve5m


java -jar /home/keldin/beagle/beagle.08Jun17.d8b.jar \
	map=/home/keldin/beagle/map/plink.chr19.GRCh37.map \
	ref=/home/keldin/beagle/refs/homzyg_test_long.vcf.gz \
	gt=/home/keldin/beagle/targets/GS12877_chr19_drmcub.vcf.gz\
	out=output.homozygous_test
#	nthreads=
#	window=
#	overlap=
