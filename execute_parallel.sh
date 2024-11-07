#!/bin/bash

cp ./btbpg_input_args.txt ./btbpg_input_args_updated.txt

parallel --jobs ${1} --colsep ',' --ungroup ./parallel.sh {1} {2} {3} {4} {5} {6} :::: btbpg_input_args.txt
