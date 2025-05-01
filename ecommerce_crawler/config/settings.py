"""
Configuration settings for the ecommerce crawler.
"""

import os
import yaml
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field


class LLMSettings(BaseModel):
    """LLM configuration settings."""
    provider: str = Field(..., description="LLM provider (e.g., azure/gpt-4.1)")
    api_token: str = Field(..., description="API token for the LLM provider")
    api_base: Optional[str] = Field(None, description="API base URL (for Azure)")
    api_version: Optional[str] = Field(None, description="API version (for Azure)")


class SiteConfig(BaseModel):
    """Configuration for a specific e-commerce site."""
    name: str = Field(..., description="Site name")
    platform: str = Field(..., description="Platform identifier (e.g., amazon, flipkart)")
    domain: Optional[str] = Field(None, description="Domain for the site (e.g., amazon.in)")
    headers: Dict[str, str] = Field(default_factory=dict, description="HTTP headers to use")
    extraction_instructions: str = Field(..., description="Instructions for the LLM extractor")


class AppConfig(BaseModel):
    """Main application configuration."""
    llm: LLMSettings = Field(..., description="LLM configuration")
    sites: Dict[str, SiteConfig] = Field(..., description="Site-specific configurations")
    default_site: str = Field(..., description="Default site to use")
    output_dir: str = Field("./output", description="Directory to save output files")
    cache_mode: str = Field("BYPASS", description="Cache mode (BYPASS, READ_ONLY, READ_WRITE)")
    ssl_verify: bool = Field(True, description="Whether to verify SSL certificates")


def load_config(config_path: Optional[str] = None) -> AppConfig:
    """
    Load configuration from a YAML file.
    
    Args:
        config_path: Path to the configuration file. If None, uses default locations.
        
    Returns:
        The application configuration
    """
    # Default config locations to check
    default_locations = [
        "./ecommerce_config.yaml",
        "./ecommerce_config.yml",
        os.path.expanduser("~/.ecommerce_crawler/config.yaml"),
    ]
    
    # Use provided path or try defaults
    config_paths = [config_path] if config_path else default_locations
    
    # Try to load from each path
    config_data = None
    for path in config_paths:
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    config_data = yaml.safe_load(f)
                break
        except Exception as e:
            print(f"Error loading config from {path}: {e}")
    
    # If no config found, use environment variables and defaults
    if not config_data:
        config_data = _create_default_config()
    
    # Create and validate the config
    return AppConfig(**config_data)


def _create_default_config() -> Dict[str, Any]:
    """
    Create a default configuration using environment variables.
    
    Returns:
        Default configuration dictionary
    """
    # Default LLM settings from environment variables
    llm_settings = {
        "provider": os.environ.get("LLM_PROVIDER", "azure/gpt-4.1"),
        "api_token": os.environ.get("AZURE_API_KEY", ""),
        "api_base": os.environ.get("AZURE_API_BASE", ""),
        "api_version": os.environ.get("AZURE_API_VERSION", ""),
    }
    
    # Default site configurations
    sites = {
        "google_shopping": {
            "name": "Google Shopping",
            "platform": "google_shopping",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.google.com/"
            },
            "extraction_instructions": """
            Extract product information from the Google Shopping results page. Ensure you extract the URL of the product page accurately if available.

            For each product, extract:
            1. The product name
            2. The price information (current price, original price if available)
            3. The URL to the product page (if available)
            4. Any other available information like brand, reviews, etc.

            Return the data in the specified schema format.
            """
        },
        "amazon": {
            "name": "Amazon",
            "platform": "amazon",
            "domain": "amazon.com",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-US,en;q=0.9",
            },
            "extraction_instructions": """
            Extract product information from the Amazon search results page. Ensure you extract the URL of the product page accurately.

            For each product, extract:
            1. The product name
            2. The price information (current price, original price if available)
            3. The URL to the product page
            4. The image URL if available
            5. The star rating and number of reviews if available
            6. The seller/brand name if available
            7. Any badges or labels (e.g., "Best Seller", "Amazon's Choice")

            Return the data in the specified schema format.
            """
        },
        "amazon_in": {
            "name": "Amazon India",
            "platform": "amazon",
            "domain": "amazon.in",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-IN,en;q=0.9",
            },
            "extraction_instructions": """
            Extract product information from the Amazon India search results page. Ensure you extract the URL of the product page accurately.

            For each product, extract:
            1. The product name
            2. The price information (current price, original price if available)
            3. The URL to the product page
            4. The image URL if available
            5. The star rating and number of reviews if available
            6. The seller/brand name if available
            7. Any badges or labels (e.g., "Best Seller", "Amazon's Choice")
            8. Delivery information if available

            Return the data in the specified schema format.
            """
        },
        "flipkart": {
            "name": "Flipkart",
            "platform": "flipkart",
            "headers": {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                "Accept-Language": "en-IN,en;q=0.9",
            },
            "extraction_instructions": """
            Extract product information from the Flipkart search results page. Ensure you extract the URL of the product page accurately.

            For each product, extract:
            1. The product name
            2. The price information (current price, original price if available)
            3. The URL to the product page
            4. The image URL if available
            5. The star rating and number of reviews if available
            6. The seller/brand name if available
            7. Any badges or labels (e.g., "Flipkart Assured")
            8. Delivery information if available
            9. Discount percentage if available

            Return the data in the specified schema format.
            """
        }
    }
    
    # Complete default configuration
    return {
        "llm": llm_settings,
        "sites": sites,
        "default_site": "google_shopping",
        "output_dir": "./output",
        "cache_mode": "BYPASS",
        "ssl_verify": False
    }


def save_config(config: AppConfig, path: str) -> None:
    """
    Save configuration to a YAML file.
    
    Args:
        config: The configuration to save
        path: Path to save the configuration file
    """
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    
    # Convert to dictionary and save
    with open(path, 'w') as f:
        yaml.dump(config.dict(), f, default_flow_style=False)
