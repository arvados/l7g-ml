#! /usr/bin/awk -f
/#+/ {
	print;
}
!/#+/ {
	t="\t";
	format=substr($9,0,2);
	pos=index($10,"|");
	allele=substr($10, pos-1, pos+1);

	print $1 t $2 t $3 t $4 t $5 t $6 t $7 t "." t format t allele;
}

# CHROM	POS	ID		REF	ALT	QUAL	FILTER	INFO	FORMAT	HG001
# 19	259464	rs35943305	C	CA	50	PASS	platforms=1;platformnames=Illumina;datasets=1;datasetnames=HiSeqPE300x;callsets=2;callsetnames=HiSeqPE300xGATK,HiSeqPE300xfreebayes;datasetsmissingcall=CGnormal,10XChromium,IonExome,SolidPE50x50bp,SolidSE75bp;callable=CS_HiSeqPE300xGATK_callable;difficultregion=AllRepeats_lt51bp_gt95identity_merged_slop5,SimpleRepeat_imperfecthomopolgt10_slop5	GT:DP:ADALL:AD:GQ:IGT:IPS:PS	1|1:482:2,229:2,229:99:1/1:.:PATMAT
