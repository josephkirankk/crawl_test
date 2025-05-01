"""
URL creator utilities for different e-commerce websites.
"""

import urllib.parse
from typing import Dict, Any, Optional


class UrlCreator:
    """Base class for URL creators."""
    
    @staticmethod
    def create_url(query: str, **kwargs) -> str:
        """
        Create a URL for the given query and parameters.
        
        Args:
            query: The search query
            **kwargs: Additional parameters specific to the platform
            
        Returns:
            A properly formatted URL
        """
        raise NotImplementedError("Subclasses must implement this method")


class GoogleShoppingUrlCreator(UrlCreator):
    """URL creator for Google Shopping."""
    
    @staticmethod
    def create_url(query: str, num: int = 100, start: int = 0, 
                  hl: str = 'en', gl: str = 'us', **kwargs) -> str:
        """
        Build a Google Shopping search URL for a given query.

        Args:
            query: Your search terms
            num: Number of results to return (max 100)
            start: Result offset for pagination
            hl: Interface language (ISO 639-1 code)
            gl: Geolocation country code (ISO 3166-1 alpha-2)
            **kwargs: Additional parameters

        Returns:
            A fully-formed Google Shopping URL
        """
        base = 'https://www.google.com/search'
        q_encoded = urllib.parse.quote_plus(query)
        return (
            f"{base}?tbm=shop"
            f"&q={q_encoded}"
            f"&num={num}"
            f"&start={start}"
            f"&hl={hl}"
            f"&gl={gl}"
        )


class AmazonUrlCreator(UrlCreator):
    """URL creator for Amazon."""
    
    @staticmethod
    def create_url(query: str, domain: str = 'amazon.com', 
                  sort: str = 'featured-rank', page: int = 1, **kwargs) -> str:
        """
        Build an Amazon search URL for a given query.

        Args:
            query: Your search terms
            domain: Amazon domain (e.g., amazon.com, amazon.in)
            sort: Sort order (e.g., featured-rank, price-asc-rank)
            page: Page number for pagination
            **kwargs: Additional parameters

        Returns:
            A fully-formed Amazon search URL
        """
        base = f'https://www.{domain}/s'
        q_encoded = urllib.parse.quote_plus(query)
        
        url = f"{base}?k={q_encoded}&s={sort}"
        
        # Add page parameter if greater than 1
        if page > 1:
            url += f"&page={page}"
            
        return url


class FlipkartUrlCreator(UrlCreator):
    """URL creator for Flipkart."""
    
    @staticmethod
    def create_url(query: str, page: int = 1, sort: str = 'relevance', **kwargs) -> str:
        """
        Build a Flipkart search URL for a given query.

        Args:
            query: Your search terms
            page: Page number for pagination
            sort: Sort order (e.g., relevance, price_asc, price_desc)
            **kwargs: Additional parameters

        Returns:
            A fully-formed Flipkart search URL
        """
        base = 'https://www.flipkart.com/search'
        q_encoded = urllib.parse.quote_plus(query)
        
        url = f"{base}?q={q_encoded}&sort={sort}"
        
        # Add page parameter if greater than 1
        if page > 1:
            url += f"&page={page}"
            
        return url


# Factory for URL creators
class UrlCreatorFactory:
    """Factory for creating URLs for different e-commerce platforms."""
    
    _creators = {
        'google_shopping': GoogleShoppingUrlCreator,
        'amazon': AmazonUrlCreator,
        'flipkart': FlipkartUrlCreator,
    }
    
    @classmethod
    def get_creator(cls, platform: str) -> UrlCreator:
        """
        Get the URL creator for the specified platform.
        
        Args:
            platform: The e-commerce platform name
            
        Returns:
            The appropriate URL creator
            
        Raises:
            ValueError: If the platform is not supported
        """
        creator = cls._creators.get(platform.lower())
        if not creator:
            supported = ", ".join(cls._creators.keys())
            raise ValueError(f"Unsupported platform: {platform}. Supported platforms: {supported}")
        return creator
    
    @classmethod
    def create_url(cls, platform: str, query: str, **kwargs) -> str:
        """
        Create a URL for the specified platform and query.
        
        Args:
            platform: The e-commerce platform name
            query: The search query
            **kwargs: Additional parameters specific to the platform
            
        Returns:
            A properly formatted URL for the specified platform
        """
        creator = cls.get_creator(platform)
        return creator.create_url(query, **kwargs)
    
    @classmethod
    def register_creator(cls, platform: str, creator: UrlCreator) -> None:
        """
        Register a new URL creator for a platform.
        
        Args:
            platform: The e-commerce platform name
            creator: The URL creator class
        """
        cls._creators[platform.lower()] = creator
