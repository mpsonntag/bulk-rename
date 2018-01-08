#!/usr/bin/env bash

echo Running install_conda.sh

set -e
set -v

if [[ "$TRAVIS_OS_NAME" = "linux" ]]; then
    sudo apt-get update
    MINICONDAVERSION="Linux"
else
    MINICONDAVERSION="MacOSX"
fi

if [[ "$CONDAPY" == "2.7" ]]; then
  wget https://repo.continuum.io/miniconda/Miniconda2-latest-$MINICONDAVERSION-x86_64.sh -O miniconda.sh;
else
  wget https://repo.continuum.io/miniconda/Miniconda3-latest-$MINICONDAVERSION-x86_64.sh -O miniconda.sh;
fi

bash miniconda.sh -b -p $HOME/miniconda
export PATH="$HOME/miniconda/bin:$PATH"
hash -r
conda config --set always_yes yes --set changeps1 no
conda update -q conda

# Useful for debugging any issues with conda
conda info -a
which python

# Create conda environment
conda create -q -n condaenv python=$CONDAPY
source activate condaenv
which python

# Install supported gi dependencies as provided by the installation guide.
conda install -c pkgw/label/superseded gtk3
conda install -c conda-forge pygobject
conda install -c conda-forge gdk-pixbuf
conda install -c pkgw-forge adwaita-icon-theme
