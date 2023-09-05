# compare_insaflu_snakemake

## Install and activate compare_insaflu environment 
```
mamba env create --name compare_insaflu --file compare_insaflu.yaml
conda activate compare_insaflu
```
## To set up the directory

Copy the main_results from INSaFLU and from INSaFLU-Snakemake.

Make sure that the fasta identifiers are exactly the same.
The coverage files as well.

## Compare multisegmented genomes

`bash compare_all.sh 8` 

This is an example for Influenza

## Compare one segmented genomes

`bash compare_all.sh 1` 

This is an example for SARS-CoV-2 and Monkeypox.



