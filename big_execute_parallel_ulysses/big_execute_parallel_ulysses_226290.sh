#!/bin/bash

parallel --jobs ${1} --colsep ',' --ungroup ./parallel_ulysses.sh {1} {2} {3} {4} {5} {6} :::: big_input_args_ulysses/big_input_args_ulysses_226290.txt
