#!/usr/bin/python

import os
import sys

def make_field_index_map(field):
  field_idx_map = {}
  field_parts  = field.split(":")
  for idx in range(len(field_parts)):
    field_idx_map[field_parts[idx]] = idx
  return field_idx_map


for line in sys.stdin:
  line = line.strip()

  if len(line)==0:
    print ""
    continue

  if line[0]=='#':
    print line
    continue

  line_parts = line.split("\t")
  fmt_field = line_parts[8]
  gtinfo_field = line_parts[9]

  fmt_idx = make_field_index_map(fmt_field)
  gtinfo_fields = gtinfo_field.split(":")

  out_line = []

  if "GT" in fmt_idx:
    line_parts[8] = "GT"
    line_parts[9] = gtinfo_fields[ fmt_idx["GT"] ]

  print "\t".join(line_parts)
