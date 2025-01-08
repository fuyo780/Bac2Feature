#!/usr/bin/bash

while getopts i:o:c:t: option
do
  case $option in
    i ) in_fasta_path=$OPTARG;;
    o ) out_taxonomy_path=$OPTARG;;
    c ) ref_classfier_path=$OPTARG;;
    t ) threads=$OPTARG;;
    \?) echo "This is unexpected option." 1>&2
        exit 1
  esac
done

intermediate_seq_qza_path="intermediate_seq.qza"
intermediate_tax_qza_path="intermediate_tax.qza"

# Import
qiime tools import --type 'FeatureData[Sequence]' --input-path $in_fasta_path --output-path $intermediate_seq_qza_path > /dev/null

# Taxonomic assignment
qiime feature-classifier classify-sklearn --i-classifier $ref_classfier_path --i-reads $intermediate_seq_qza_path --o-classification $intermediate_tax_qza_path --p-n-jobs $threads > /dev/null

# Export
qiime tools export --input-path $intermediate_tax_qza_path --output-path . > /dev/null

# Rename
mv ./taxonomy.tsv $out_taxonomy_path
yes | rm $intermediate_seq_qza_path $intermediate_tax_qza_path
