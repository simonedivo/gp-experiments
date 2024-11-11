#!/bin/bash

#cp input_args_google/input_args_google.txt input_args_google/input_args_google_updated.txt

parallel --jobs ${1} --colsep ',' --ungroup ./parallel_google.sh {1} {2} {3} {4} {5} {6} :::: input_args_google/input_args_google.txt
