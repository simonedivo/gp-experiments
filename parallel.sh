#!/bin/bash

echo "started processing $*.."
python3 gpgomea_experiments_no_list.py $*;
echo finished processing "$*";
