"""
Base extractor class for e-commerce websites.
"""

import asyncio
import json
import os
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel

from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, LLMConfig
from crawl4ai.extraction_strategy import LLMExtractionStrategy
from crawl4ai.cache_context import CacheMode

from ecommerce_crawler.models.product import Product
from ecommerce_crawler.config.settings import SiteConfig, AppConfig


class ExtractionResult(BaseModel):
    """Result of an extraction operation."""
    success: bool
    products: List[Product] = []
    error_message: Optional[str] = None
    raw_html: Optional[str] = None
    query: str
    site: str
    url: str


class BaseExtractor:
    """Base class for e-commerce extractors."""
    
    def __init__(self, config: AppConfig, site_key: str):
        """
        Initialize the extractor.
        
        Args:
            config: Application configuration
            site_key: Key of the site configuration to use
        
        Raises:
            ValueError: If the site configuration is not found
        """
        self.app_config = config
        
        # Get site configuration
        if site_key not in config.sites:
            raise ValueError(f"Site configuration not found for {site_key}")
        
        self.site_config = config.sites[site_key]
        self.site_key = site_key
        
        # Create LLM configuration
        self.llm_config = LLMConfig(
            provider=config.llm.provider,
            api_token=config.llm.api_token
        )
        
        # Set Azure-specific environment variables if needed
        if config.llm.provider.startswith("azure/"):
            if config.llm.api_base:
                os.environ["AZURE_API_BASE"] = config.llm.api_base
            if config.llm.api_version:
                os.environ["AZURE_API_VERSION"] = config.llm.api_version
    
    async def extract(self, url: str, query: str) -> ExtractionResult:
        """
        Extract product information from the given URL.
        
        Args:
            url: URL to extract from
            query: Search query that generated this URL
            
        Returns:
            Extraction result with products and metadata
        """
        # Create extraction strategy
        extraction_strategy = self._create_extraction_strategy()
        
        # Configure crawler
        config = self._create_crawler_config(extraction_strategy)
        
        # Run crawler
        async with AsyncWebCrawler() as crawler:
            try:
                result = await crawler.arun(url=url, config=config)
            except Exception as e:
                return ExtractionResult(
                    success=False,
                    error_message=f"Error during crawling: {type(e).__name__}: {str(e)}",
                    query=query,
                    site=self.site_key,
                    url=url
                )
            
            if not result.success:
                return ExtractionResult(
                    success=False,
                    error_message=result.error_message,
                    query=query,
                    site=self.site_key,
                    url=url
                )
            
            # Process extraction result
            return self._process_result(result, query, url)
    
    def _create_extraction_strategy(self) -> LLMExtractionStrategy:
        """
        Create an LLM extraction strategy for the site.
        
        Returns:
            Configured LLM extraction strategy
        """
        return LLMExtractionStrategy(
            llm_config=self.llm_config,
            schema=Product.model_json_schema(),
            extraction_type="schema",
            instruction=self.site_config.extraction_instructions,
            verbose=True
        )
    
    def _create_crawler_config(self, extraction_strategy: LLMExtractionStrategy) -> CrawlerRunConfig:
        """
        Create a crawler configuration.
        
        Args:
            extraction_strategy: The extraction strategy to use
            
        Returns:
            Configured crawler configuration
        """
        return CrawlerRunConfig(
            extraction_strategy=extraction_strategy,
            verbose=True,
            cache_mode=getattr(CacheMode, self.app_config.cache_mode),
            experimental={
                "ssl_verify": self.app_config.ssl_verify,
                "headers": self.site_config.headers
            }
        )
    
    def _process_result(self, result: Any, query: str, url: str) -> ExtractionResult:
        """
        Process the crawler result.
        
        Args:
            result: Crawler result
            query: Search query
            url: URL that was crawled
            
        Returns:
            Processed extraction result
        """
        # Initialize extraction result
        extraction_result = ExtractionResult(
            success=True,
            query=query,
            site=self.site_key,
            url=url
        )
        
        # Save raw HTML for debugging if available
        if hasattr(result, 'html'):
            extraction_result.raw_html = result.html
        elif hasattr(result, 'fit_html'):
            extraction_result.raw_html = result.fit_html
        
        # Process extracted content if available
        if hasattr(result, 'extracted_content') and result.extracted_content:
            try:
                # Parse the extracted content
                products_data = json.loads(result.extracted_content)
                
                # Convert to Product objects and add source_site
                products = []
                for product_data in products_data:
                    # Add source site to each product
                    product_data['source_site'] = self.site_config.name
                    
                    # Handle price field conversion if needed
                    if isinstance(product_data.get('price'), str):
                        product_data['price'] = {
                            'current_price': product_data['price'],
                            'original_price': None,
                            'discount_percentage': None,
                            'currency': None
                        }
                    
                    # Create Product object
                    try:
                        product = Product(**product_data)
                        products.append(product)
                    except Exception as e:
                        print(f"Error creating product: {e}")
                        # Add partial product data anyway
                        products.append(Product(
                            name=product_data.get('name', 'Unknown'),
                            price={
                                'current_price': product_data.get('price', {}).get('current_price', 'N/A') 
                                if isinstance(product_data.get('price'), dict) else str(product_data.get('price', 'N/A'))
                            },
                            source_site=self.site_config.name
                        ))
                
                extraction_result.products = products
                
            except json.JSONDecodeError:
                extraction_result.success = False
                extraction_result.error_message = "Could not parse the extracted content as JSON"
        else:
            extraction_result.success = False
            extraction_result.error_message = "No structured data was extracted"
        
        return extraction_result
    
    def save_results(self, result: ExtractionResult, output_path: Optional[str] = None) -> str:
        """
        Save extraction results to files.
        
        Args:
            result: Extraction result to save
            output_path: Path to save the results. If None, uses the configured output directory.
            
        Returns:
            Path to the saved JSON file
        """
        # Create output directory if it doesn't exist
        output_dir = output_path or os.path.join(self.app_config.output_dir, self.site_key)
        os.makedirs(output_dir, exist_ok=True)
        
        # Create a filename based on the query
        safe_query = result.query.replace(' ', '_').lower()[:50]
        base_filename = f"{safe_query}_{result.site}"
        
        # Save products to JSON
        json_path = os.path.join(output_dir, f"{base_filename}.json")
        with open(json_path, 'w', encoding='utf-8') as f:
            f.write(json.dumps([p.dict() for p in result.products], indent=4))
        
        # Save raw HTML if available
        if result.raw_html:
            html_path = os.path.join(output_dir, f"{base_filename}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(result.raw_html)
        
        return json_path
