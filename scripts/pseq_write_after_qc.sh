#!/usr/bin/env bash
#
# Writes vardb after QC has been performed.
#
# $1 = Included sites
# $2 = Output folder
#

INCLUDED_SITES=$1
OUTPUT_FOLDER=$2

if [[ $INCLUDED_SITES == "" ]]; then 
    echo "Usage pseq_write_vardb.sh <sites> <output_folder>"
    exit 1
fi

mkdir -p $OUTPUT_FOLDER
pseq proj write-vardb \
--mask ereg=@${INCLUDED_SITES} \
--locdb ~/pseq/hg19/locdb \
--new-project ${OUTPUT_FOLDER}/proj \
--new-vardb ${OUTPUT_FOLDER}/proj_out




