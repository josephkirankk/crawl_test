"""
Command-line interface for the ecommerce crawler.
"""

import argparse
import asyncio
import json
import os
import sys
from typing import List, Dict, Any, Optional

from ecommerce_crawler.crawler import EcommerceCrawler
from ecommerce_crawler.config.settings import load_config, save_config, AppConfig
from ecommerce_crawler.utils.url_creator import UrlCreatorFactory


def parse_args():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Extract product information from e-commerce websites.")

    # Create subparsers for commands
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize configuration")
    init_parser.add_argument("--output-path", default="./ecommerce_config.yaml", help="Path to save configuration")

    # List command
    list_parser = subparsers.add_parser("list", help="List supported sites")

    # Search command (default)
    search_parser = subparsers.add_parser("search", help="Search for products")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--site", "-s", help="Site to search on (e.g., google_shopping, amazon, amazon_in, flipkart)")
    search_parser.add_argument("--config", "-c", help="Path to configuration file")
    search_parser.add_argument("--output", "-o", help="Output directory for results")
    search_parser.add_argument("--domain", "-d", help="Domain for Amazon (e.g., amazon.com, amazon.in)")
    search_parser.add_argument("--page", "-p", type=int, default=1, help="Page number for pagination")
    search_parser.add_argument("--sort", help="Sort order (e.g., relevance, price_asc)")
    search_parser.add_argument("--all-sites", "-a", action="store_true", help="Search on all configured sites")

    # Batch command
    batch_parser = subparsers.add_parser("batch", help="Process multiple queries from a file")
    batch_parser.add_argument("batch_file", help="Path to batch file with queries (one per line)")
    batch_parser.add_argument("--site", "-s", help="Site to search on (e.g., google_shopping, amazon, amazon_in, flipkart)")
    batch_parser.add_argument("--config", "-c", help="Path to configuration file")
    batch_parser.add_argument("--output", "-o", help="Output directory for results")
    batch_parser.add_argument("--domain", "-d", help="Domain for Amazon (e.g., amazon.com, amazon.in)")
    batch_parser.add_argument("--page", "-p", type=int, default=1, help="Page number for pagination")
    batch_parser.add_argument("--sort", help="Sort order (e.g., relevance, price_asc)")
    batch_parser.add_argument("--all-sites", "-a", action="store_true", help="Search on all configured sites")

    # For backwards compatibility, handle the case where the first argument is not a command
    args = parser.parse_args()

    # If no command is specified, show help
    if not hasattr(args, 'command') or not args.command:
        parser.print_help()
        sys.exit(1)

    return args


async def run_single_query(crawler: EcommerceCrawler, query: str, site: Optional[str], url_params: Dict[str, Any]):
    """Run a single query."""
    print(f"Searching for '{query}' on {site or crawler.config.default_site}...")

    # Extract products
    if site:
        result = await crawler.extract_products(query, site, url_params)
        process_result(result)
    else:
        # Use default site
        result = await crawler.extract_products(query, url_params=url_params)
        process_result(result)


async def run_multi_site_query(crawler: EcommerceCrawler, query: str, url_params: Dict[str, Dict[str, Any]]):
    """Run a query on multiple sites."""
    print(f"Searching for '{query}' on multiple sites...")

    # Extract products from all sites
    results = await crawler.extract_from_multiple_sites(query, url_params=url_params)

    # Process results
    for site_key, result in results.items():
        print(f"\n--- Results from {site_key} ---")
        process_result(result)


async def run_batch_queries(crawler: EcommerceCrawler, batch_file: str, site: Optional[str], url_params: Dict[str, Any]):
    """Run batch queries from a file."""
    print(f"Running batch queries from {batch_file}...")

    # Read queries from file
    with open(batch_file, 'r', encoding='utf-8') as f:
        queries = [line.strip() for line in f if line.strip()]

    # Run each query
    for query in queries:
        if site:
            await run_single_query(crawler, query, site, url_params)
        else:
            await run_multi_site_query(crawler, query, {site_key: url_params for site_key in crawler.config.sites})
        print("\n" + "-" * 50 + "\n")


def process_result(result):
    """Process and display extraction result."""
    if result.success:
        print(f"Successfully extracted {len(result.products)} products.")

        # Display products
        for i, product in enumerate(result.products, 1):
            print(f"\nProduct {i}:")
            print(f"  Name: {product.name}")
            print(f"  Price: {product.price.current_price}")
            if product.price.original_price:
                print(f"  Original Price: {product.price.original_price}")
            if product.price.discount_percentage:
                print(f"  Discount: {product.price.discount_percentage}")
            if product.product_url:
                print(f"  URL: {product.product_url}")
            if product.brand:
                print(f"  Brand: {product.brand}")
            if product.reviews and product.reviews.rating:
                print(f"  Rating: {product.reviews.rating}/5 ({product.reviews.count} reviews)")

        print(f"\nResults saved to {os.path.join(result.site, result.query.replace(' ', '_').lower()[:50] + '_' + result.site + '.json')}")
    else:
        print(f"Error: {result.error_message}")


def list_supported_sites(config: AppConfig):
    """List supported sites."""
    print("Supported sites:")
    for site_key, site_config in config.sites.items():
        print(f"  - {site_key}: {site_config.name}")


def init_config(output_path: str):
    """Initialize configuration."""
    # Load default configuration
    config = load_config()

    # Save to specified path
    save_config(config, output_path)
    print(f"Configuration initialized and saved to {output_path}")


async def main():
    """Main entry point."""
    args = parse_args()

    # Handle configuration commands
    if args.command == "init":
        init_config(args.output_path)
        return

    # Load configuration
    config_path = getattr(args, 'config', None)
    crawler = EcommerceCrawler(config_path)

    # Handle list command
    if args.command == "list":
        list_supported_sites(crawler.config)
        return

    # Set output directory if specified
    if hasattr(args, 'output') and args.output:
        crawler.config.output_dir = args.output

    # Prepare URL parameters
    url_params = {}
    if hasattr(args, 'domain') and args.domain:
        url_params["domain"] = args.domain
    if hasattr(args, 'page') and args.page:
        url_params["page"] = args.page
    if hasattr(args, 'sort') and args.sort:
        url_params["sort"] = args.sort

    # Handle batch command
    if args.command == "batch":
        if not os.path.exists(args.batch_file):
            print(f"Error: Batch file {args.batch_file} not found.")
            return

        await run_batch_queries(crawler, args.batch_file, getattr(args, 'site', None), url_params)
        return

    # Handle search command
    if args.command == "search":
        if hasattr(args, 'all_sites') and args.all_sites:
            # Multi-site mode
            site_params = {site_key: url_params.copy() for site_key in crawler.config.sites}
            await run_multi_site_query(crawler, args.query, site_params)
        else:
            # Single site mode
            await run_single_query(crawler, args.query, getattr(args, 'site', None), url_params)
        return


if __name__ == "__main__":
    asyncio.run(main())
