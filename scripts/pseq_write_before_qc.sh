#!/usr/bin/env bash
#
# Writes vardb after QC has been performed.
#
# $1 = Included sites
# $2 = Output folder
#

FILTER="geno=geno=DP:ge:10"
OUTPUT_FOLDER=$1

if [[ $OUTPUT_FOLDER == "" ]]; then 
    echo "Usage pseq_write_vardb.sh <OUTPUT_FOLDER>"
    exit 1
fi

mkdir -p $OUTPUT_FOLDER
pseq proj write-vardb \
--mask $FILTER  \
--locdb ~/pseq/hg19/locdb \
--new-project ${OUTPUT_FOLDER}/proj \
--new-vardb ${OUTPUT_FOLDER}/proj_out


