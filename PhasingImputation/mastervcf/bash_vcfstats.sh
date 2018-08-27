#!/bin/bash

OTOT=$(sed -n 's/Passed Filters//pg'  $1 | sed 's/[[:space:]][^0-9]//g')
PTOT=$(sed -n 's/Passed Filters//pg'  $2 | sed 's/[[:space:]][^0-9]//g')
IFPOS=$(grep "None" $3 | sed 's/[[:space:]][0-9]/a&/g' | cut -d\a -f4)
EIFPOS=$(grep "None" $4 | sed 's/[[:space:]][0-9]/a&/g' | cut -d\a -f4)  

echo -e $5 '\t' ${OTOT} '\t' ${PTOT} '\t' ${IFPOS} '\t' ${EIFPOS} >> $6
