#!/bin/bash
#
#
# @date 26 November 2015
# @author James Boocock
#
#
VCF=$1
PHENOTYPES=$2
PHENOTYPES_COLUMN=$3
RESOURCES=$4

if [[ $RESOURCES == "" ]]; then
    echo "Usage:  pseq_indiv.sh <VCF> <phenotypes> <phenotype_column> <resources>" 
    exit 1
fi

mkdir -p qc
echo "Load project"
pseq proj new-project --resources $RESOURCES 
echo "Load VCF"
pseq proj load-vcf --vcf $VCF

echo "Variant frequency"
pseq proj v-freq --mask hwe=0:1e-7 > qc/hwe_fail.txt &

echo "Individual statistics"
pseq proj i-stats --stats gmean=DP ref=dbsnp --mask filter=VQSRTrancheSNP99.90to100.00,VQSRTrancheSNP99.00to99.90,PASS  \
reg.ex=chrX,chrY  \
--out qc/all_stats
echo "singletons"
  pseq proj i-stats --stats gmean=DP ref=dbsnp --mask \
 filter=VQSRTrancheSNP99.90to100.00,VQSRTrancheSNP99.00to99.90,PASS \
 mac=1-1\
reg.ex=chrX,chrY  \
--out qc/singleton
echo "doubletons"
  pseq proj i-stats --stats gmean=DP ref=dbsnp --mask \
 filter=VQSRTrancheSNP99.90to100.00,VQSRTrancheSNP99.00to99.90,PASS mac=2-2 \
reg.ex=chrX,chrY  \
 --out qc/doubleton

echo "Write pedigree file"
pseq proj write-ped --mask  snp biallelic maf=0.05-0.95 \
geno.req=GQ:ge:95,DP:ge:10 --out qc/snp_plink

echo "Snp plink QC"
plink --tfile qc/snp_plink --geno 0.01 --hwe 0.001 --make-bed \
--out qc/snp_plink_qc
echo "Poly MDS"
plink --bfile qc/snp_plink_qc --indep-pairwise 100 50 0.1 \
--out  qc/poly_mds
echo "4MDS"
plink --bfile qc/snp_plink_qc --extract qc/poly_mds.prune.in \
--make-bed --out qc/4mds
echo "MDS Frequency"
plink --bfile qc/snp_plink_qc --freq --out qc/4mds_freq
echo "Plink genome"
plink --bfile qc/snp_plink_qc --genome
echo "Plink MDS"
plink --bfile qc/4mds --read-genome plink.genome --cluster --mds-plot 4 --out qc/plink

# Clean up temporary project at the end.
rm -Rf proj_out/ proj.pseq 

