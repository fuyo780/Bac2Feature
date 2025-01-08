# Bac2Feature
Bac2Feature is an interface for predicting bacterial and archaeal traits from 16S rRNA gene sequences. Currently, Bac2Feature predicts 8 continuous and 10 categorical traits listed below.

Bac2Feature integrates three representative methods for trait prediction and provided them with systematic evaluations for avoiding spurious predictions. See details for Citations.
## Predicted traits by Bac2Feature
- Continuous traits
	- Doubling time (log_10 hours)
	- Growth temperature (Degrees C)
	- Optimum growth temperature (Degrees C)
	- Genome size (Base Pair)
	- GC content (Percentage)
	- Coding genes, rRNA 16S genes, tRNA genes (Number)
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
Bac2Feature depends on conda environments, so please install [conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html) in advance.
```sh
# Clone github repository
git clone https://fuyo780/Bac2Feature.git

# Add conda repositories, if necessary
conda config --append channels conda-forge
conda config --append channels bioconda

# Create conda environment
conda create --name bac2feature --file environment/bac2feature_packages.yml
conda activate bac2feature

# (Optional) Create conda environment for taxonomy-based prediction
conda create --name qiime2-2023.5 --file environment/env_qiime2-2023.5-py38-linux-conda.yml

# Install Bac2Feature command line
pip install .

# Print help message
bac2feature -h
```
## Citations
Bac2Feature: an easy-to-use interface for predicting prokaryotic traits from 16S rRNA gene sequences 
Masaki Fujiyoshi, Takao K Suzuki, Wataru Iwasaki, Chikara Furuwasa, Motomu Matsui
bioRxiv
## Contact
- Masaki Fujiyoshi (Graduate School of Frontier Sciences, The University of Tokyo, Japan): fujiyoshi-masaki353@g.ecc.u-tokyo.ac.jp
- [Matsui Motomu](https://sites.google.com/site/motomumatsui/) (Institute for Chemical Research, Kyoto University, Japan): motomu.matsui@gmail.com
