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
import sys
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

__WRITE_VARDB_TEMPLATE__="""
pseq_write_after_qc.sh {0} {1}
"""
__PED_VCF_SH__="""
out_vcf_ped.sh {0} {1} {2}
"""

# Hardcoded hyper for now
__PSEQ_STATS_SH__="""
    pseq_stats.sh {0} {1} {2}
"""
__PSEQ_STATS_R__="""
    pseq_stats.R {0}
"""

def prepare_qc(args):
    """ 
        Process quality control data for webapp. 
    """
    mask_string = args.filter_string
    output_file = args.output_file 
    phenotype = args.phenotype
    vcf_input = args.vcf_input
    # First step is read the VCF file into pseq and then generate all the output files.
    command = __PSEQ_STATS_SH__.format(phenotype, mask_string, vcf_input)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        sys.exit(1)
        logging.error("Command: {0} failed".format(' '.join(command)))
    # Second step if to generate the QC file.
    command = __PSEQ_STATS_R__.format(output_file)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        logging.error("Command: {0} failed".format(' '.join(command)))
        sys.exit(1)

def post_qc(args):
    """ 
        Post-process quality control data from webapp.
    """
    sites = args.sites
    output_folder = args.folder_out
    ped_output = args.ped_output 
    vcf_output = args.vcf_output
    command = __WRITE_VARDB_TEMPLATE__.format(sites, output_folder)
    #logging.info("Running: {0}".format(command))
    try:
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        logging.error("Command: {0} failed".format(' '.join(command)))
    current_dir = os.getcwd()
    os.chdir(output_folder)
    command = __PED_VCF_SH__.format(ped_output, vcf_output, os.path.join(current_dir,sites))
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        logging.error("Command: {0} failed".format(' '.join(command)))
        sys.exit(1)

def main():
    """
   
    """
    parser = argparse.ArgumentParser(description="Plink/Seq QC pipeline for sequencing data")
    subparsers = parser.add_subparsers(help='Sub-command help')
    
    # Prepare VCF
    prepare_vcf = subparsers.add_parser("prepare",help="Prepare data")
    prepare_vcf.add_argument("vcf_input", help="VCF input file for QC analysis")
    prepare_vcf.add_argument("-f", "--filter", dest="filter_string", help="Filter for plink/seq", default="geno=DP:ge:10")
    prepare_vcf.add_argument("-p", "--phenotype", dest="phenotype", help="Phenotype column", default="HYPER")
    prepare_vcf.add_argument("-o", "--output-file", dest="output_file", help="Output analysis", default="qc_file.txt")
    prepare_vcf.set_defaults(func=prepare_qc)
    post_qc_vcf = subparsers.add_parser("postqc", help="Post Quality control processing")
    post_qc_vcf.add_argument('-s','--sites',dest='sites', help="List of sites to retain from SHINY app", required=True)
    post_qc_vcf.add_argument('-o','--output_folder', dest='folder_out', 
                             help='Output folder for plink/seq project', required=True)
    post_qc_vcf.add_argument('-v','--vcf', dest="vcf_output", default="out.vcf",
                             help="VCF output file", required=True)
    post_qc_vcf.add_argument('-p','--ped', dest="ped_output", default="plink",
                             help="PED output file", required=True)
    post_qc_vcf.set_defaults(func=post_qc)
    clean = subparsers.add_parser('clean', help="Clean data")
    args = parser.parse_args()
    args.func(args)

if __name__=="__main__":
    main()
