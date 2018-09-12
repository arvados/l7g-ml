#!/bin/bash

SAMPLE=$1
ORIGINALSTATS=$2
PHASEDSTATS=$3
ORIGINALIMPUTEDEVAL=$4
ORIGINALIMPUTEDOUTSIDEEVAL=$5

echo -e "#sample\toriginal\tphased\timputed\timputed_outsidebed"

ORIGINAL=`grep "Passed Filters" $ORIGINALSTATS | awk '{print $4}'`
PHASED=`grep "Passed Filters" $PHASEDSTATS | awk '{print $4}'`
IMPUTED=`grep "None" $ORIGINALIMPUTEDEVAL | awk '{print $4}'`
IMPUTEDOUTSIDE=`grep "None" $ORIGINALIMPUTEDOUTSIDEEVAL | awk '{print $4}'`

echo -e "$SAMPLE\t$ORIGINAL\t$PHASED\t$IMPUTED\t$IMPUTEDOUTSIDE"
