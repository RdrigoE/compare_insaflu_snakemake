source insaflu
echo "Comparing AllConsensus"
python compare_consensus.py --f1 ./snakemake/AllConsensus_no_ref.fasta --f2 ./insaflu/AllConsensus.fasta --output all_consensus_output.csv -v
# echo "Comparing Alignment_nt_All"
# python compare_consensus.py --f1 ./snakemake/Alignment_nt_All.fasta --f2 ./insaflu/Alignment_nt_All.fasta --output alignment_output.csv -v
echo "Comparing Coverage"
python compare_coverage.py --f1 snakemake/coverage.csv --f2 insaflu/coverage.tsv --n_locus 8 --output coverage_output.csv -v
echo "Comparing Validated Variants"
python compare_snps.py --f1 snakemake/validated_variants.csv --f2 insaflu/validated_variants.tsv --output validated_output.csv -v
echo "Comparing Minor Variants"
python compare_snps.py --f1 snakemake/validated_minor_iSNVs.csv --f2 insaflu/validated_minor_iSNVs.tsv --output minor_output.csv -v


