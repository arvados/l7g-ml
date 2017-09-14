#!/bin/sh

./getTileVariants.py -i 1792420 -l -b -vdi -pvd --assembly-gz='./tiling-files/assembly.00.hg19.fw.gz' --assembly-fwi='./tiling-files/assembly.00.hg19.fw.fwi' --keep='./keep/by_id/su92l-4zz18-fkbdz2w6b25ayj3' --hiq-info='./tiling-files/hiq-pgp-info'

# What each command means 
# -i [Index]: index of the array
# -l [Location]: provides the name of the tile, along with phase, step, and path
# -vdi [Variant Different Indices]: provides the Variant Difference Indices, in other words the locations where the base pairs are different
# -pvd [Print Variant Differences]: denotes the different base pairs in red
# --assembly-gz: the location of the assembly gz file, usually assembly.00.hg19.fw.gz
# --assembly-fwi: the location of the assembly fwi file, usually assembly.00.hg19.fw.fwi
# --hiq-info: the location of the high quality tile names, usually hiq-pgp-info
# --keep: the location of the keep collection containing the tiling library
