#!/usr/bin/env bash
#
# @author James Boocock
# @date 24 November 2015
#

PED_OUTPUT_NAME=$1
VCF_OUTPUT_NAME=$2
SITES=$3

if [[ $SITES = "" ]]; then
    echo "out_vcf_ped.sh <ped basename> <vcf_output> <sites>" 
    exit 1
fi

pseq proj write-ped --name culling --out $PED_OUTPUT_NAME
pseq proj write-vcf --mask ereg=@${SITES} >  $VCF_OUTPUT_NAME 
