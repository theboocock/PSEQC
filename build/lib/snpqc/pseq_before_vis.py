#!/usr/bin/env python
#
# @James Boocock
# @date 23 Nov 2015
#
#
# Runs the plinkseq preparation pipeline. 
#
#

import argparse

def main():
    """
        Run the Pseq prep pipeline. 
    """
    parser = argparse.ArgumentParser(description="Plink/Seq QC pipeline for sequencing data")
    subparsers = parser.add_subparsers(help='Sub-command help')
    prepare_vcf = subparsers.add_parser("prepare",help="Prepare data")
    prepare_vcf 

    args = parser.parse_args()
    run_qc_first()
