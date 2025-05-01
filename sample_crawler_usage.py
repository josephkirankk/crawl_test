#!/usr/bin/env python3
"""
Sample script demonstrating how to use the ecommerce crawler.
"""

import asyncio
import json
import os
from ecommerce_crawler.crawler import EcommerceCrawler


async def sample_google_shopping():
    """Sample Google Shopping extraction."""
    print("=== Google Shopping Example ===")
    
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from Google Shopping
    result = await crawler.extract_products(
        query="smart door lock under 10000 rupees",
        site_key="google_shopping"
    )
    
    # Display results
    if result.success:
        print(f"Successfully extracted {len(result.products)} products from Google Shopping")
        print(f"First product: {result.products[0].name}, Price: {result.products[0].price.current_price}")
    else:
        print(f"Error: {result.error_message}")


async def sample_amazon():
    """Sample Amazon extraction."""
    print("\n=== Amazon Example ===")
    
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from Amazon
    result = await crawler.extract_products(
        query="smart door lock",
        site_key="amazon",
        url_params={"domain": "amazon.com"}
    )
    
    # Display results
    if result.success:
        print(f"Successfully extracted {len(result.products)} products from Amazon")
        print(f"First product: {result.products[0].name}, Price: {result.products[0].price.current_price}")
    else:
        print(f"Error: {result.error_message}")


async def sample_amazon_india():
    """Sample Amazon India extraction."""
    print("\n=== Amazon India Example ===")
    
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from Amazon India
    result = await crawler.extract_products(
        query="smart door lock",
        site_key="amazon_in"
    )
    
    # Display results
    if result.success:
        print(f"Successfully extracted {len(result.products)} products from Amazon India")
        print(f"First product: {result.products[0].name}, Price: {result.products[0].price.current_price}")
    else:
        print(f"Error: {result.error_message}")


async def sample_flipkart():
    """Sample Flipkart extraction."""
    print("\n=== Flipkart Example ===")
    
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from Flipkart
    result = await crawler.extract_products(
        query="smart door lock",
        site_key="flipkart"
    )
    
    # Display results
    if result.success:
        print(f"Successfully extracted {len(result.products)} products from Flipkart")
        print(f"First product: {result.products[0].name}, Price: {result.products[0].price.current_price}")
    else:
        print(f"Error: {result.error_message}")


async def sample_multi_site():
    """Sample multi-site extraction."""
    print("\n=== Multi-site Example ===")
    
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from multiple sites
    results = await crawler.extract_from_multiple_sites(
        query="smart door lock",
        site_keys=["google_shopping", "amazon", "flipkart"]
    )
    
    # Display results
    for site_key, result in results.items():
        if result.success:
            print(f"Successfully extracted {len(result.products)} products from {site_key}")
            if result.products:
                print(f"First product: {result.products[0].name}, Price: {result.products[0].price.current_price}")
        else:
            print(f"Error from {site_key}: {result.error_message}")


async def main():
    """Run all samples."""
    # Set Azure OpenAI environment variables
    os.environ["AZURE_API_BASE"] = os.environ.get("AZURE_API_BASE", "https://pep-ee-pepgenxsbx-nonprod-eus2-openai.openai.com")
    os.environ["AZURE_API_VERSION"] = os.environ.get("AZURE_API_VERSION", "2025-01-01-preview")
    os.environ["AZURE_API_KEY"] = os.environ.get("AZURE_API_KEY", "957badf7e39643dca147a6b8d157f66d")
    
    # Run samples
    await sample_google_shopping()
    await sample_amazon()
    await sample_amazon_india()
    await sample_flipkart()
    await sample_multi_site()


if __name__ == "__main__":
    asyncio.run(main())
