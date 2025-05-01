"""
Main crawler class for extracting product information from e-commerce websites.
"""

import asyncio
import os
from typing import List, Optional, Dict, Any

from ecommerce_crawler.config.settings import AppConfig, load_config
from ecommerce_crawler.utils.url_creator import UrlCreatorFactory
from ecommerce_crawler.extractors.factory import ExtractorFactory
from ecommerce_crawler.extractors.base import ExtractionResult


class EcommerceCrawler:
    """Main crawler class for e-commerce websites."""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Initialize the crawler.
        
        Args:
            config_path: Path to the configuration file. If None, uses default locations.
        """
        self.config = load_config(config_path)
        
        # Create output directory if it doesn't exist
        os.makedirs(self.config.output_dir, exist_ok=True)
    
    async def extract_products(self, query: str, site_key: Optional[str] = None, 
                              url_params: Optional[Dict[str, Any]] = None) -> ExtractionResult:
        """
        Extract product information for the given query.
        
        Args:
            query: Search query
            site_key: Site to search on. If None, uses the default site.
            url_params: Additional parameters for URL creation
            
        Returns:
            Extraction result with products and metadata
        """
        # Use default site if not specified
        site_key = site_key or self.config.default_site
        
        # Check if site is supported
        if site_key not in self.config.sites:
            raise ValueError(f"Unsupported site: {site_key}")
        
        # Get site configuration
        site_config = self.config.sites[site_key]
        
        # Create URL
        url_params = url_params or {}
        if site_key == "amazon_in" or site_key == "amazon":
            # Add domain parameter for Amazon
            url_params["domain"] = site_config.domain or "amazon.com"
        
        url = UrlCreatorFactory.create_url(site_config.platform, query, **url_params)
        
        # Create extractor
        extractor = ExtractorFactory.create_extractor(self.config, site_key)
        
        # Extract products
        result = await extractor.extract(url, query)
        
        # Save results
        if result.success and result.products:
            extractor.save_results(result)
        
        return result
    
    async def extract_from_multiple_sites(self, query: str, site_keys: Optional[List[str]] = None,
                                         url_params: Optional[Dict[str, Dict[str, Any]]] = None) -> Dict[str, ExtractionResult]:
        """
        Extract product information from multiple sites.
        
        Args:
            query: Search query
            site_keys: List of sites to search on. If None, uses all configured sites.
            url_params: Additional parameters for URL creation, keyed by site_key
            
        Returns:
            Dictionary of extraction results, keyed by site_key
        """
        # Use all sites if not specified
        site_keys = site_keys or list(self.config.sites.keys())
        url_params = url_params or {}
        
        # Create tasks for each site
        tasks = []
        for site_key in site_keys:
            site_url_params = url_params.get(site_key, {})
            tasks.append(self.extract_products(query, site_key, site_url_params))
        
        # Run tasks concurrently
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        result_dict = {}
        for site_key, result in zip(site_keys, results):
            if isinstance(result, Exception):
                # Create error result
                result_dict[site_key] = ExtractionResult(
                    success=False,
                    error_message=f"Error: {type(result).__name__}: {str(result)}",
                    query=query,
                    site=site_key,
                    url=""
                )
            else:
                result_dict[site_key] = result
        
        return result_dict
