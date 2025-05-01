#!/usr/bin/env python3
"""
Main script to run the ecommerce crawler.
"""

import asyncio
import os
import sys
from ecommerce_crawler.cli import main

if __name__ == "__main__":
    # Set Azure OpenAI environment variables if they exist in the environment
    for env_var in ["AZURE_API_KEY", "AZURE_API_BASE", "AZURE_API_VERSION"]:
        if env_var in os.environ:
            print(f"Using {env_var} from environment")

    # Check if we need to add the 'search' command
    if len(sys.argv) > 1 and sys.argv[1] not in ['search', 'batch', 'init', 'list', '-h', '--help']:
        # Insert 'search' as the first argument
        sys.argv.insert(1, 'search')

    # Run the CLI
    asyncio.run(main())
