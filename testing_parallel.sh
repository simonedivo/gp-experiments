#!/bin/bash

YELLOW=$'\033[0;33m'
NC=$'\033[0m' # No Color
GREEN=$'\033[0;32m'

echo "${YELLOW} started processing $*.. ${NC}"
python3 gpgomea_experiments_no_list.py $*;
python3 edit_input_args.py $*;
echo "${GREEN}finished processing $* ${NC}";
