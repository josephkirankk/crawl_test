"""
Amazon specific extractor.
"""

from ecommerce_crawler.extractors.base import BaseExtractor
from ecommerce_crawler.config.settings import AppConfig


class AmazonExtractor(BaseExtractor):
    """Extractor for Amazon."""
    
    def __init__(self, config: AppConfig, site_key: str = "amazon"):
        """
        Initialize the Amazon extractor.
        
        Args:
            config: Application configuration
            site_key: Site configuration key to use (e.g., "amazon" or "amazon_in")
        """
        super().__init__(config, site_key)
    
    # Override methods if needed for Amazon specific behavior
