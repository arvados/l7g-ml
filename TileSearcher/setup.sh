#!/bin/sh

# set up keep-mount
mkdir -p ./keep
arv-mount --allow-other ./keep
# download dependencies
if [ ! -d ./tiling-files ]; then
	mkdir tiling-files && cd tiling-files
else
	cd tiling-files
fi

if [ ! -f ./assembly.00.hg19.fw.fwi ]; then
	wget https://workbench.su92l.arvadosapi.com/collections/download/su92l-4zz18-lj22pmb8h3ty0w8/1ojgsdawy3ldxu74nlu1cbkjduyadovqy2xcbmi1ui7wcpetaz/assembly.00.hg19.fw.fwi
fi
if [ ! -f ./assembly.00.hg19.fw.gz ]; then
	wget https://workbench.su92l.arvadosapi.com/collections/download/su92l-4zz18-lj22pmb8h3ty0w8/1ojgsdawy3ldxu74nlu1cbkjduyadovqy2xcbmi1ui7wcpetaz/assembly.00.hg19.fw.gz
fi

if [ ! -f ./assembly.00.hg19.fw.gz.gzi ]; then
	wget https://workbench.su92l.arvadosapi.com/collections/download/su92l-4zz18-lj22pmb8h3ty0w8/1ojgsdawy3ldxu74nlu1cbkjduyadovqy2xcbmi1ui7wcpetaz/assembly.00.hg19.fw.gz.gzi
fi
if [ ! -f ./hiq-pgp-info ]; then
	wget https://workbench.su92l.arvadosapi.com/collections/download/su92l-4zz18-xmmmg0qn0wuaxkl/5w2jsmz7ko275u355d9wu0q8q4neir7pxa6pzmj5ujmgq6tuhp/hiq-pgp-info
fi
