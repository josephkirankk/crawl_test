#!/bin/bash

# Source conda.sh to enable conda command
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh

# Source Azure environment variables
source set_azure_env.sh

# Activate the conda environment
conda activate crawlenv

# Run the Python script
python test_azure_crawl4ai.py

# Deactivate the environment when done
conda deactivate
