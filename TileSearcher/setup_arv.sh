#!/bin/sh

# set up keep-mount
mkdir -p ./keep
arv-mount ./keep
# download dependencies
if [ ! -f ./tiling-files ]; then
	mkdir tiling-files && cd tiling-files
else
	cd tiling-files
fi

if [ ! -f ./assembly.00.hg19.fw.fwi ]; then
	arv-get b8835cbca4f8dfd3396f39f5ca10bb84+780/assembly.00.hg19.fw.fwi . 
fi
if [ ! -f ./assembly.00.hg19.fw.gz ]; then
	arv-get b8835cbca4f8dfd3396f39f5ca10bb84+780/assembly.00.hg19.fw.gz . 
fi

if [ ! -f ./assembly.00.hg19.fw.gz.gzi ]; then
	arv-get b8835cbca4f8dfd3396f39f5ca10bb84+780/assembly.00.hg19.fw.gz.gzi .
fi
if [ ! -f ./hiq-pgp-info ]; then
	arv-get bfba01c5b9b4053f596a2dc36d072cd6+46480/hiq-pgp-info .
fi
