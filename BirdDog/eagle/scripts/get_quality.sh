#! /bin/bash

awk '$1 !~ /##*/{print $6}' $1 > ./qualities_only
