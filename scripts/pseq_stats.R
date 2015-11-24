#!/usr/bin/env Rscript
#
# @author James Boocock
# @date 22/Nov/2015
#
args = commandArgs(trailingOnly= TRUE)
print(args[1])
if(is.na(args[1])){
    print("Need to run with Rscript pseq_stats.R <output_file>") 
    quit("yes")
}
options(warn=2)
output_file = args[1]
write("Read counts\n", stderr())
counts = read.table("qc/counts.txt",header=T)
write("Read Pval all\n", stderr())
pval = read.delim("qc/pval_all.txt",header=T, sep='\t')
write("Read gqgm stats\n", stderr())
ggdp = read.table("qc/gqgm.stats",header=F)
write("Read hwe all \n", stderr())
hwe_all = read.delim("qc/hwe_all.txt", header=T, sep='\t')
write("Read cases.txt\n", stderr())
hwe_cases = read.delim("qc/cases.txt", header=T, sep='\t')
write("Read controls.txt\n", stderr())
hwe_controls=read.delim("qc/controls.txt",sep='\t', header=T) 
write("Read gqgm cases \n", stderr())
ggdp_cases = read.table("qc/gqgm.cases.stats", header=F) 
write("Read gqgm controls \n", stderr())
ggdp_controls = read.table("qc/gqgm.controls.stats", header=F)
ggdp_names = c("VAR","REFALT","FILTER","GQM","DPM")
colnames(ggdp_cases) = ggdp_names
colnames(ggdp_controls) = ggdp_names
colnames(ggdp) = ggdp_names
allelic_balance = read.table("qc/site.ab.summ",header=T)
case_allelic_balance = read.table("qc/site.cases.ab.summ",header=T)
controls_allelic_balance = read.table("qc/site.controls.ab.summ",header=T)
ab = merge(case_allelic_balance, controls_allelic_balance,by="VAR",suffixes=c(".cases",".controls"))
ab = merge(allelic_balance,ab)
# GQ counts
ggi = read.table("qc/count_bad_good.txt",header=F)
names(ggi) = c("VAR","GQ10","GQ50")
# Then merge them all together
h = merge(hwe_cases,hwe_controls, by="VAR", suffixes=c(".cases",".controls"))
g = merge(ggdp_cases, ggdp_controls, by="VAR", suffixes=c(".cases",".controls"))
gh = merge(h,g,by="VAR")
variant_type = read.table('qc/annot_all_variants.txt',header=T) 
count_m = merge(gh,pval,by="VAR")
m = merge(count_m, counts,by="VAR")
m = merge(variant_type, m ,by="VAR")
m = merge(ggi,m,by="VAR")
m = merge(m,ab,by="VAR")
m = merge(m,ggdp,by="VAR")
print(nrow(m))
m = m[m$CNTU +  m$CNTA != 0 ,]
print(nrow(m))
write.table(m,file=output_file)
