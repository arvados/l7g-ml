h2. The following is a short explanation of the items in this directory

This directory is where most of the actual development work was done.

h3. abram_clean.py and clean_vcf.awk

Genome in a Bottle (GIAB) comes to us as a very visually messy VCF. At least, this is true of HG001—the other genomes in the cohort might be different. It is very difficult to see what's going on or even if this VCF follows the same format as others. These two scripts represent efforts to clean up the VCF.

h3. beagle_command.sh

Just a compact/convient way to invoke Beagle on the command line with all the options and flags that were needed.

h3. beagle_command_homozygous_test.sh

A lot of work with Beagle (as well as Eagle) was trying to determine how 
