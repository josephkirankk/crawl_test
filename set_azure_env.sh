#!/bin/bash

# Set Azure OpenAI environment variables
export AZURE_API_KEY="957badf7e39643dca147a6b8d157f66d"
export AZURE_API_BASE="https://pep-ee-pepgenxsbx-nonprod-eus2-openai.openai.azure.com"
export AZURE_API_VERSION="2025-01-01-preview"

# Verify the variables are set
echo "Azure OpenAI environment variables set:"
echo "AZURE_API_KEY: ${AZURE_API_KEY:0:5}*****"
echo "AZURE_API_BASE: $AZURE_API_BASE"
echo "AZURE_API_VERSION: $AZURE_API_VERSION"

# Note: Run this script with 'source set_azure_env.sh' to ensure
# variables are set in your current shell session 