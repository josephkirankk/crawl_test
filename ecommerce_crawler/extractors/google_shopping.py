"""
Google Shopping specific extractor.
"""

from ecommerce_crawler.extractors.base import BaseExtractor
from ecommerce_crawler.config.settings import AppConfig


class GoogleShoppingExtractor(BaseExtractor):
    """Extractor for Google Shopping."""
    
    def __init__(self, config: AppConfig):
        """
        Initialize the Google Shopping extractor.
        
        Args:
            config: Application configuration
        """
        super().__init__(config, "google_shopping")
    
    # Override methods if needed for Google Shopping specific behavior
