#!/bin/bash

echo "started processing $*.."
python3 gpgomea_experiments_no_list.py $*;
python3 edit_input_args.py $*;
echo "finished processing $*";
