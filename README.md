# Bac2Feature

![version](https://img.shields.io/badge/version-1.1-blue)

Bac2Feature is an easy-to-use interface to predict bacterial and archaeal traits from 16S rRNA gene sequences.

Bac2Feature integrates three representative methods for trait prediction and provided them with systematic evaluations for avoiding spurious predictions. See Citations for details.
## Predicted traits by Bac2Feature
Currently, Bac2Feature predicts 8 continuous and 10 categorical traits listed below.
- Continuous traits
	- Doubling time (log_10 hours)
	- Growth temperature (degrees C)
	- Optimum growth temperature (degrees C)
	- Genome size (base pair)
	- GC content (percentage)
	- Coding genes (number)
	- rRNA 16S genes (number)
	- tRNA genes (number)
- Categorical traits (All traits are predicted yes (=1) or no (=0).)
	- Gram stain
	- Sporulation
	- Anaerobes
	- Motility
	- Temperature range
		- Mesophiles, Thermophiles
	- Cell shape
		- Bacillus, Coccus, Filament, Spiral
## Download stand-alone version
Bac2Feature is currently supported on Linux-based operating systems and has been verified on Ubuntu 22.04 LTS, 24.04 LTS and Red Hat Enterprise Linux 8.7.
```sh
# Clone github repository
git clone https://github.com/fuyo780/Bac2Feature.git
cd Bac2Feature/

# Add Conda repositories, if necessary
conda config --append channels conda-forge
conda config --append channels bioconda

# Create Conda environment
conda create --name bac2feature --file environment/env_bac2feature.txt
conda activate bac2feature

# (Optional) Create Conda environment for taxonomy-based prediction
conda create --name qiime2-2023.5 --file environment/env_qiime2-2023.5-py38-linux-conda.txt

# Install Bac2Feature command line (execute at this directory Bac2Feature)
pip install bac2feature

# Print help message
bac2feature -h

usage: bac2feature [-h] -s FASTA FILE -o TSV FILE [-m {homology,taxonomy,phylogeny}] [--check_NSTI] [--without_filter]
                   [--intermediate_dir PATH] [--threads INT] [--ref_dir_placement PATH] [--ref_blastdb PATH] [--ref_trait PATH]

This script predicts prokaryotic traits from 16S rRNA gene sequences.
Three methods are available: homology-based, taxonomy-based, and phylogeny-based prediction.
Citation: Fujiyoshi et al., Bioinform. Adv., 2025. DOI: 10.1093/bioadv/vbad070

optional arguments:
  -h, --help            show this help message and exit
  -m {homology,taxonomy,phylogeny}, --method {homology,taxonomy,phylogeny}
                        Method to predict prokaryotic traits (default: phylogeny).
                          "homology": predict prokaryotic traits using homology search.
                          "taxonomy": predict prokaryotic traits using taxonomic classification.
                          "phylogeny": predict prokaryotic traits using phylogenetic placement.
  --check_NSTI          Check NSTI values for the phylogeny-based prediction,
                        or check alignment identity for the homology-based prediction.
  --without_filter      Disable filtering by NSTI threshold for the phylogeny-based prediction.
  --intermediate_dir PATH
                        Store intermediate file in this directory.
  --threads INT         Specify the number of CPU in parallel (default: 1).
  --ref_dir_placement PATH
                        Reference for phylogenetic placement (for developer use).
  --ref_blastdb PATH    Reference for homology search (for developer use).
  --ref_trait PATH      Reference for trait prediction (for developer use).

required arguments:
  -s FASTA FILE, --seq FASTA FILE
                        Input 16S rRNA sequences in fasta format.
  -o TSV FILE, --output TSV FILE
                        Output predicted trait table in tsv format.

Usage example:
bac2feature -s rep_seqs.fasta -o predicted_traits.tsv

```
## Citations
Bac2Feature: an easy-to-use interface for predicting prokaryotic traits from 16S rRNA gene sequences 
Masaki Fujiyoshi, Takao K Suzuki, Wataru Iwasaki, Chikara Furuwasa, Motomu Matsui. Bioinform. Adv., 2025.
## Contact
- Masaki Fujiyoshi (The University of Tokyo): fujiyoshi-masaki353@g.ecc.u-tokyo.ac.jp
- [Matsui Motomu](https://sites.google.com/site/motomumatsui/) (Kyoto University): motomu.matsui@gmail.com
