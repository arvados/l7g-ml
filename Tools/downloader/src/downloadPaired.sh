#!/bin/bash

URL=${1%\?*}

URL=${URL%/}

FILENAME=`basename $URL`

DIRECTORY=${FILENAME%_*}

echo $FILENAME
echo $DIRECTORY

if [[ ! -d $DIRECTORY ]]; then
  mkdir $DIRECTORY
fi

cd $DIRECTORY

curl "$1" | tee "$FILENAME" | md5sum -b > "$FILENAME".md5sum

# We mostly care about the curl exit code
exit ${PIPESTATUS[0]}

# To print just the percentage of progress:
#  2>&1 -# | stdbuf -oL tr '\r' '\n' | grep -o '[0-9]*\.[0-9]'

