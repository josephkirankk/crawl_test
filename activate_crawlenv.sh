#!/bin/zsh

# Source conda.sh to enable conda command
source /opt/homebrew/Caskroom/miniconda/base/etc/profile.d/conda.sh

# Activate the conda environment
conda activate crawlenv

# Print confirmation
echo "Conda environment 'crawlenv' is now activated."
echo "You can now run your Python scripts with 'python' command."
echo ""
echo "When you're done, type 'conda deactivate' to exit the environment."
echo ""
echo "To run your Azure crawl script, you can use:"
echo "source set_azure_env.sh && python test_azure_crawl4ai.py"
