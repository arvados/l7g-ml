#!/usr/bin/env python3

import random
import sys

seedsnumberstr, seedslimitstr = sys.argv[1:3]
seedsnumber = int(seedsnumberstr)
seedslimit = int(seedslimitstr)

if seedsnumber > seedslimit:
    seedslimit = seedsnumber

seeds = random.sample(range(seedslimit), seedsnumber)
for seed in seeds:
    print(seed)
