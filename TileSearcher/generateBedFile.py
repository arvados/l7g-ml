#!/usr/bin/env python

import gzip
import time
import sys

if len(sys.argv) != 2:
    print("Usage: ./generatedBedFile.py <assembly.gz file>")
    sys.exit(1)

assembly_path = sys.argv[1]

# set some initial counters
prev_end = 0
active_chr = None
old_chr = None
active_path = None

start = time.time()

with open("hg19.bed", "w") as bedfile, gzip.open(assembly_path, 'rb') as gzip_file:
    for line in gzip_file:
        # new line with ">" --> new chromosome/path
        if active_chr == None or ">" in line:
            if active_chr != None:
               old_chr = active_chr
            _, active_chr, active_path = line.split(":")
            active_path = active_path.strip()
            print(line)

            if active_chr == old_chr:
               prev_end = int(curr_pos) + 1
            else:
               prev_end = 0
        else:
            # process line of gzipped assembly file
            curr_step, curr_pos = line.split('\t')[0], line.split('\t')[-1]
            curr_step = curr_step.strip()
            curr_pos = curr_pos.strip()
            line_txt = "{active_chr}\t{start}\t{stop}\t{path}.{step}".format(
                active_chr=active_chr.strip(), start=prev_end, stop=curr_pos, path=active_path, step=curr_step)
            prev_end = int(curr_pos) + 1
            bedfile.write(line_txt + '\n')


end = time.time()
print("Bedfile creation finished. Elapsed time: {:.2f}s".format(end - start))
