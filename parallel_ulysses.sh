#!/bin/bash

ORANGE=$'\033[0;33m'
NC=$'\033[0m' # No Color
GREEN=$'\033[0;32m'

echo "${ORANGE} started processing $*.. ${NC}"
python3 gpgomea_experiments_no_list.py $*;
echo "${GREEN}finished processing $* ${NC}";
