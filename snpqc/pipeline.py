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
    pseq_stats.sh {0} {1} {2} {3}
"""
__PSEQ_STATS_R__="""
    pseq_stats.R {0}
"""
__INDIV_STATS_SH__="""
    pseq_indiv.sh {0} {1} {2} {3}
"""
__INDIV_STATS_R__="""
    pseq_indiv.R {0} {1} {2} {3}
"""

def individual_qc_func(args):
    """
        Individual quality control 
    """
    vcf_input = args.vcf_input
    phenotype = args.phenotype
    phenotype_column = args.phenotype_column 
    phenotype_file = args.phenotype
    resources = args.resources
    snp_max_pheno = args.original_phenotypes
    output_file = "indiv_qc.txt"
    command = __INDIV_STATS_SH__.format(vcf_input, phenotype, phenotype_column, resources)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        sys.exit(1)
        logging.error("Command: {0} failed".format(' '.join(command)))
    command = __INDIV_STATS_R__.format('qc/plink.mds','qc/all_stats.istats', snp_max_pheno, output_file)
    try:
        logging.info("Running: {0}".format(command))
        command = shlex.split(command)
        subprocess.check_call(command)
    except:
        sys.exit(1)
        logging.error("Command: {0} failed".format(' '.join(command)))

def site_qc_func(args):
    """ 
        Process quality control data for webapp. 
    """
    mask_string = args.filter_string
    phenotype_file = args.phenotype
    output_file = "site_qc.txt"
    individual_file = "individual_qc.txt"
    phenotype_column = args.phenotype_column 
    vcf_input = args.vcf_input
    resources = args.resources
    # First step is read the VCF file into pseq and then generate all the output files.
    command = __PSEQ_STATS_SH__.format(phenotype, mask_string, vcf_input, phenotype_column, resources)
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
    individual_qc = subparsers.add_parser("prep_indivqc",help="Prepare data")
    individual_qc.add_argument("vcf_input", help="VCF input file for QC analysis")
    individual_qc.add_argument("-p", "--phenotype", dest="phenotype", help="Phenotype file (pseq)", required=True)
    individual_qc.add_argument("-o", "--original-phenotypes", dest="original_phenotypes", help="Original phenotypes file (snpmax)", required=True)
    individual_qc.add_argument("-c", "--phenotype_column", dest="phenotype_column", help="Phenotype file", default="HYPER")
    individual_qc.add_argument("-r", "--resources", dest="resources", help="Resources", default="~/rm_G6174_G5913_AT0721/hg19")
    individual_qc.set_defaults(func=individual_qc_func)
    
    # Prepare VCF
    site_qc = subparsers.add_parser("prep_siteqc", help="Site QC")
    site_qc.add_argument("vcf_input", help="VCF input file for QC analysis")
    site_qc.add_argument("-f", "--filter", dest="filter_string", help="Filter for plink/seq", default="geno=DP:ge:10")
    site_qc.add_argument("-p", "--phenotype", dest="phenotype", help="Phenotype file", required=True) 
    site_qc.add_argument("-c", "--phenotype_column", dest="phenotype_column", help="Phenotype file", default="HYPER")
    site_qc.add_argument("-r", "--resources", dest="resources", help="Resources", default="~/rm_G6174_G5913_AT0721/hg19")
    site_qc.set_defaults(func=site_qc_func)
    post_qc_vcf = subparsers.add_parser("postqc", help="Post Quality control processing for Sites")
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
