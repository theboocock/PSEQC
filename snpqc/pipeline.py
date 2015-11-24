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
import os
import shutil
import subprocess
import shlex
import logging 
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

__LOAD__VCF__TEMPLATE__="""
pseq_load_vcf.sh {0}
"""

__WRITE_VARDB_TEMPLATE__=""""
pseq_write_before_qc.sh {1} {2}
"""

# Hardcoded hyper for now
__PSEQ_STATS_SH__="""
    pseq_stats.sh {0} {1} {2}
"""
__PSEQ_STATS_R__="""
    pseq_stats.R {0}
"""

def process_qc(args):
    """ 
        Process quality control data for webapp. 
    """
    mask_string = args.filter_string
    output_file = args.output_file 
    phenotype = args.phenotype
    vcf_input = args.vcf_input
    # First step is read the VCF file into pseq and then generate all the output files.
    command = __PSEQ_STATS__.format(phenotype, mask_string, vcf_input)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        logger.error("Command: {0} failed".format(' '.join(command)))
    # Second step if to generate the QC file.
    command = __PSEQ_STATS_R__.format(output_file)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        logger.error("Command: {0} failed".format(' '.join(command)))
def post_qc(args):
    """ 
        Post-process quality control data from webapp.
    """
    return None
def main():
    """
   
    """
    parser = argparse.ArgumentParser(description="Plink/Seq QC pipeline for sequencing data")
    subparsers = parser.add_subparsers(help='Sub-command help')
    
    # Prepare VCF
    prepare_vcf = subparsers.add_parser("prepare",help="Prepare data")
    prepare_vcf.add_argument("vcf_input", help="VCF input file for QC analysis")
    prepare_vcf.add_argument("-f", "--filter", dest="filter_string", help="Filter for plink/seq", default="DP:ge:10")
    prepare_vcf.add_argument("-p", "--phenotype", dest="phenotype", help="Phenotype column", default="HYPER")
    prepare_vcf.add_argument("-o", "--output-file", dest="output_file", help="Output analysis", default="qc_file.txt")
    prepare_vcf.set_defaults(func=prepare_vcf)
    post_qc_vcf = subparsers.add_parser("snp_list", help="Post Quality control processing")
    post_qc_vcf.set_defaults(func=process_qc)

    args = parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()
