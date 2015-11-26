#!/usr/bin/env Rscript

args = commandArgs(trailingOnly = TRUE)
print(args)
mds = read.table(args[1], header=T)
istats = read.delim(args[2], header=T, sep='\t')
pheno = read.delim(args[3], header=T, sep='\t')
shiny_output = args[4]
m1 = merge(mds, pheno, by=1)
m2 = merge(m1,istats, by=1)
write.table(m2, file=shiny_output)
