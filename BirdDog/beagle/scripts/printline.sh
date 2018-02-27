#! /bin/bash

sed -n $1p $2

line=$(sed -n 5p broken_positions)
keldin@lightning-dev1:~/beagle/targets$ echo $line
