# Bac2Feature

## Download stand-alone version
Bac2Feature uses a conda environment, so please prepare conda command before installing Bac2Feature.
```sh
# clone github repository
git clone https://fuyo780/Bac2Feature.git

# add conda repositories, if necessary
conda config --append channels conda-forge
conda config --append channels bioconda

# create Bac2Feature virtual environment from yml file
conda create --name bac2feature --file environment/bac2feature_packages.yml
conda activate bac2feature

# Test run
bac2feature -h
```

## Reproduce results in paper
