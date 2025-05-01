"""
Flipkart specific extractor.
"""

from ecommerce_crawler.extractors.base import BaseExtractor
from ecommerce_crawler.config.settings import AppConfig


class FlipkartExtractor(BaseExtractor):
    """Extractor for Flipkart."""
    
    def __init__(self, config: AppConfig):
        """
        Initialize the Flipkart extractor.
        
        Args:
            config: Application configuration
        """
        super().__init__(config, "flipkart")
    
    # Override methods if needed for Flipkart specific behavior
