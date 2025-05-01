# E-commerce Product Crawler

A flexible, extensible, and maintainable tool for extracting product information from various e-commerce websites like Amazon, Flipkart, Google Shopping, and more.

## Features

- Extract product information from multiple e-commerce platforms
- Configurable extraction parameters
- Support for different regions (e.g., Amazon.com, Amazon.in)
- Command-line interface for easy use
- Batch processing of multiple queries
- Concurrent extraction from multiple sites
- Extensible architecture for adding new sites

## Supported Sites

- Google Shopping
- Amazon (US)
- Amazon India
- Flipkart

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/josephkirankk/crawl_test.git
   cd crawl_test
   ```

2. Set up a conda environment:
   ```
   conda create -n crawlenv python=3.10
   conda activate crawlenv
   ```

3. Install dependencies:
   ```
   pip install pydantic crawl4ai pyyaml
   ```

## Configuration

The crawler uses a YAML configuration file to define settings for different e-commerce sites. You can initialize a default configuration with:

```
./run_crawler.py init
```

This will create an `ecommerce_config.yaml` file that you can customize.

## Usage

### Command-line Interface

Search for products on Google Shopping:
```
./run_ecommerce_crawler.sh "smart door lock"
```

Search on a specific site:
```
./run_ecommerce_crawler.sh "smart door lock" --site amazon_in
```

Search on all configured sites:
```
./run_ecommerce_crawler.sh "smart door lock" --all-sites
```

Process multiple queries from a file:
```
./run_ecommerce_crawler.sh --batch queries.txt
```

### Python API

```python
import asyncio
from ecommerce_crawler.crawler import EcommerceCrawler

async def main():
    # Create crawler
    crawler = EcommerceCrawler()
    
    # Extract products from Google Shopping
    result = await crawler.extract_products(
        query="smart door lock",
        site_key="google_shopping"
    )
    
    # Display results
    if result.success:
        print(f"Successfully extracted {len(result.products)} products")
        for product in result.products:
            print(f"Name: {product.name}, Price: {product.price.current_price}")
    else:
        print(f"Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Extending

### Adding a New Site

1. Create a URL creator in `ecommerce_crawler/utils/url_creator.py`
2. Add site configuration to `ecommerce_config.yaml`
3. Create a site-specific extractor in `ecommerce_crawler/extractors/`
4. Register the extractor in `ecommerce_crawler/extractors/factory.py`

## License

MIT
