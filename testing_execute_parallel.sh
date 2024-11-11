#!/bin/bash

cp ${2} ${2%.*}_updated.txt

parallel --jobs ${1} --colsep ',' --ungroup ./testing_parallel.sh {1} {2} {3} {4} {5} {6} ${2%.*}_updated.txt :::: ${2}
