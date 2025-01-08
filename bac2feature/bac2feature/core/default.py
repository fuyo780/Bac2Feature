#!/usr/bin/env python3

# Default setting of Bac2Feature
from os import path

project_dir = path.dirname(path.dirname(path.abspath(__file__)))

# Core directory
b2f_core_dir = path.join(project_dir, "core")

# Data directory
b2f_data_dir = path.join(project_dir, "data")

# Reference trait data
ref_trait = path.join(b2f_data_dir, "trait_data_madin.tsv")

# Reference 16S rRNA gene sequences
fasta = path.join(b2f_data_dir, "16S_rRNA_seqs.fasta")

# Refernce direcotry for homology-based prediction
ref_homology = path.join(b2f_data_dir, "ref_homology")
ref_blastdb = path.join(ref_homology, "ref_blastdb")

# Refernce direcotry for taxonomy-based prediction
ref_dir_taxonomy = path.join(b2f_data_dir, "ref_taxonomy")
ref_nb_classfier = path.join(ref_dir_taxonomy, "nb_classifier.qza")
ref_trait_taxonomy = path.join(ref_dir_taxonomy, "empirical_dist.json")
qiime_env = "qiime2-2023.5"

# Refernce direcotry for phylogeny-based prediction
ref_dir_phylogeny = path.join(b2f_data_dir, "ref_phylogeny")
ref_dir_placement = ref_dir_phylogeny
# fasta = path.join(b2f_data_dir, "b2f_ref.fasta")

tree = path.join(ref_dir_phylogeny, "ref_phylogeny.tre")

hmm = path.join(ref_dir_phylogeny, "ref_phylogeny.hmm")

model = path.join(ref_dir_phylogeny, "ref_phylogeny.model")
