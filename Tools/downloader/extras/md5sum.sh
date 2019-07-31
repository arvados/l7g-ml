#!/bin/bash

KEEPDIR=$1

DIRECTORY=`basename $2`
FILENAME=$DIRECTORY/$DIRECTORY.bam

echo "KEEPDIR: $KEEPDIR"
echo "DIRECTORY: $DIRECTORY"
echo "FILENAME: $FILENAME"

echo "md5sum $FILENAME"

if [[ ! -d "$KEEPDIR/$DIRECTORY" ]]; then
  echo "Error, $KEEPDIR/$DIRECTORY not found!"
  exit 1
fi

if [[ ! -f "$KEEPDIR/$FILENAME" ]]; then
  echo "Error, $KEEPDIR/$FILENAME not found!"
  exit 1
fi

mkdir $DIRECTORY

# This is a trick; by symlinking the bam file from the keep mount,
# crunch-run will be smart enough to not copy it to generate the output
# collection, and instead do manifest manipulation
ln -s "$KEEPDIR/$FILENAME" "$FILENAME" 

if [[ -f "$KEEPDIR/$FILENAME".md5sum ]] && [[ -s "$KEEPDIR/$FILENAME".md5sum ]]; then
  echo "Skipping, non-zero size $KEEPDIR/$FILENAME.md5sum found!"
  ln -s "$KEEPDIR/$FILENAME.md5sum" "$FILENAME".md5sum
else
  md5sum -b "$FILENAME" > "$FILENAME".md5sum
fi
