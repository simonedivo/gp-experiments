#!/bin/bash

parallel --jobs ${1} --colsep ',' --ungroup .//parallel_ulysses.sh {1} {2} {3} {4} {5} {6} :::: input_args_ulysses/input_args_ulysses_943369.txt
