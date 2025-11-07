# Bac2Feature

![version](https://img.shields.io/badge/version-1.1-blue)

> [!WARNING]  
> Bac2Feature web service is currently stopped due to server migration. Please wait for a few weeks.

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

# Add Conda repositories, if necessary
conda config --append channels conda-forge
conda config --append channels bioconda

# Create Conda environment
conda create --name bac2feature --file environment/env_bac2feature.txt
conda activate bac2feature

# (Optional) Create Conda environment for taxonomy-based prediction
conda create --name qiime2-2023.5 --file environment/env_qiime2-2023.5-py38-linux-conda.txt

# Install Bac2Feature command line (execute at this directory Bac2Feature)
cd Bac2Feature/
pip install bac2feature

# Print help message
bac2feature -h

# Usage example
bac2feature -s test_seqs.fasta -o predicted_traits.tsv

```
## Citations
Bac2Feature: an easy-to-use interface to predict prokaryotic traits from 16S rRNA gene sequences  
Masaki Fujiyoshi, Takao K Suzuki, Wataru Iwasaki, Chikara Furuwasa, Motomu Matsui. Bioinform. Adv., 2025.
## Contact
- Masaki Fujiyoshi (The University of Tokyo): fujiyoshi-masaki353@g.ecc.u-tokyo.ac.jp
- [Matsui Motomu](https://sites.google.com/site/motomumatsui/) (Kyoto University): motomu.matsui@gmail.com
