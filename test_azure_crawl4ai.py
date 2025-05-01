import asyncio
import json
import os
from pydantic import BaseModel, Field
from typing import Optional
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.cache_context import CacheMode
from url_creator import build_shopping_url

# Define a Pydantic model for product information
class Product(BaseModel):
    name: str = Field(..., description="The name of the product")
    price: str = Field(..., description="The price of the product including currency symbol")
    product_url: Optional[str] = Field(None, description="The URL to the product page")

async def main():
    # Create an LLM extraction strategy for Google Shopping products
    # This uses Azure OpenAI to extract structured product information

    # Set Azure OpenAI environment variables directly
    os.environ["AZURE_API_BASE"] = os.environ.get("AZURE_API_BASE", "https://pep-ee-pepgenxsbx-nonprod-eus2-openai.openai.azure.com")
    os.environ["AZURE_API_VERSION"] = os.environ.get("AZURE_API_VERSION", "2025-01-01-preview")

    # Create LLM configuration
    llm_config = LLMConfig(
        provider="azure/gpt-4.1",  # Using Azure OpenAI GPT-4.1
        api_token=os.environ.get("AZURE_API_KEY", "957badf7e39643dca147a6b8d157f66d")
    )

    extraction_strategy = LLMExtractionStrategy(
        llm_config=llm_config,
        schema=Product.model_json_schema(),  # Use our Product schema for extraction (using model_json_schema instead of schema)
        extraction_type="schema",  # Extract data according to the schema
        instruction="""
        Extract product information from the Google Shopping results page.
        For each product, extract:
        1. The product name
        2. The price (including currency symbol)
        3. The URL to the product page (if available)

        Return the data in the specified schema format.
        """,
        verbose=True  # Enable verbose output for debugging
    )

    # Configure crawler with proper parameters
    config = CrawlerRunConfig(
        extraction_strategy=extraction_strategy,
        verbose=True,                # Enable verbose output
        cache_mode=CacheMode.BYPASS, # Disable cache to force a fresh request
        experimental={
            "ssl_verify": False,  # Disable SSL verification
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/"
            }
        }
    )

    # Run crawler
    async with AsyncWebCrawler() as crawler:
        print("Starting Google Shopping page fetch with LLMExtractionStrategy...")
        # Use build_shopping_url to get a properly formatted Google Shopping URL
        shopping_url = build_shopping_url(query="low budget smartphone")
        print(f"Using shopping URL: {shopping_url}")

        try:
            result = await crawler.arun(
                url=shopping_url,
                config=config
            )
        except Exception as e:
            print(f"Error during crawling: {type(e).__name__}: {str(e)}")
            import traceback
            traceback.print_exc()
            return

        if result.success:
            print("\nFetch successful!")

            # Process and display the extracted product information
            if hasattr(result, 'extracted_content') and result.extracted_content:
                print("\n=== Extracted Product Information ===\n")

                # Parse the extracted content
                try:
                    products = json.loads(result.extracted_content)

                    # Display each product
                    for i, product in enumerate(products, 1):
                        print(f"Product {i}:")
                        print(f"  Name: {product.get('name', 'N/A')}")
                        print(f"  Price: {product.get('price', 'N/A')}")
                        print(f"  URL: {product.get('product_url', 'N/A')}")
                        print()

                    # Save the extracted data to a JSON file
                    with open("extracted_products.json", "w", encoding="utf-8") as f:
                        f.write(result.extracted_content)
                    print("Extracted data saved to extracted_products.json")

                except json.JSONDecodeError:
                    print("Error: Could not parse the extracted content as JSON")
                    print(f"Raw content: {result.extracted_content}")
            else:
                print("No structured data was extracted.")

                # Save the HTML content for debugging
                if hasattr(result, 'html'):
                    with open("google_shopping_results.html", "w", encoding="utf-8") as f:
                        f.write(result.html)
                    print("HTML saved to google_shopping_results.html")
                elif hasattr(result, 'fit_html'):
                    with open("google_shopping_results.html", "w", encoding="utf-8") as f:
                        f.write(result.fit_html)
                    print("HTML saved to google_shopping_results.html")
        else:
            print(f"Error: {result.error_message}")

if __name__ == "__main__":
    asyncio.run(main())