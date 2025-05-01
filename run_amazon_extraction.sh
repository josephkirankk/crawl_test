#!/bin/zsh

# Exit on error
set -e

# Source conda.sh to enable conda command
if [ -f "/opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh" ]; then
    source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh
else
    echo "Error: conda.sh not found at expected location."
    echo "Please update the script with the correct path to conda.sh"
    exit 1
fi

# Source Azure environment variables
if [ -f "set_azure_env.sh" ]; then
    source set_azure_env.sh
else
    echo "Error: set_azure_env.sh not found."
    exit 1
fi

# Make sure pydantic is installed
echo "Checking for required packages..."
pip install -q pydantic

# Activate the conda environment
echo "Activating conda environment 'crawlenv'..."
if conda activate crawlenv; then
    echo "Environment activated successfully."
else
    echo "Error: Failed to activate conda environment 'crawlenv'."
    exit 1
fi

# Run the Python script
echo "Running Google Shopping product extraction script..."
python test_azure_crawl4ai.py

# Deactivate the environment when done
echo "Extraction complete. Deactivating conda environment..."
conda deactivate
echo "Done."
