"""
Factory for creating extractors for different e-commerce sites.
"""

from typing import Dict, Type

from ecommerce_crawler.config.settings import AppConfig
from ecommerce_crawler.extractors.base import BaseExtractor
from ecommerce_crawler.extractors.google_shopping import GoogleShoppingExtractor
from ecommerce_crawler.extractors.amazon import AmazonExtractor
from ecommerce_crawler.extractors.flipkart import FlipkartExtractor


class ExtractorFactory:
    """Factory for creating extractors."""
    
    # Map of site keys to extractor classes
    _extractors: Dict[str, Type[BaseExtractor]] = {
        "google_shopping": GoogleShoppingExtractor,
        "amazon": AmazonExtractor,
        "amazon_in": AmazonExtractor,  # Uses the same extractor with different site_key
        "flipkart": FlipkartExtractor,
    }
    
    @classmethod
    def create_extractor(cls, config: AppConfig, site_key: str) -> BaseExtractor:
        """
        Create an extractor for the specified site.
        
        Args:
            config: Application configuration
            site_key: Site key to create an extractor for
            
        Returns:
            An extractor instance
            
        Raises:
            ValueError: If the site is not supported
        """
        # Check if site is supported
        if site_key not in cls._extractors:
            supported = ", ".join(cls._extractors.keys())
            raise ValueError(f"Unsupported site: {site_key}. Supported sites: {supported}")
        
        # Create and return extractor
        extractor_class = cls._extractors[site_key]
        
        # Special case for Amazon with different domains
        if site_key == "amazon_in":
            return extractor_class(config, site_key)
        
        return extractor_class(config)
    
    @classmethod
    def register_extractor(cls, site_key: str, extractor_class: Type[BaseExtractor]) -> None:
        """
        Register a new extractor class for a site.
        
        Args:
            site_key: Site key to register the extractor for
            extractor_class: Extractor class to register
        """
        cls._extractors[site_key] = extractor_class
