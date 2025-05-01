"""
Product data model for e-commerce product information.
"""

from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List, Dict, Any


class ProductReview(BaseModel):
    """Model for product reviews."""
    rating: Optional[float] = Field(None, description="Rating value (e.g., 4.5 out of 5)")
    count: Optional[int] = Field(None, description="Number of reviews")
    
    
class ProductPrice(BaseModel):
    """Model for product price information."""
    current_price: str = Field(..., description="The current price of the product including currency symbol")
    original_price: Optional[str] = Field(None, description="The original/list price before any discounts")
    discount_percentage: Optional[str] = Field(None, description="Discount percentage if available")
    currency: Optional[str] = Field(None, description="Currency code (e.g., USD, INR)")


class Product(BaseModel):
    """
    Enhanced product information model that works across different e-commerce platforms.
    """
    name: str = Field(..., description="The name of the product")
    price: ProductPrice = Field(..., description="Price information")
    product_url: Optional[str] = Field(None, description="The URL to the product page")
    image_url: Optional[str] = Field(None, description="URL to the product image")
    description: Optional[str] = Field(None, description="Short description of the product")
    brand: Optional[str] = Field(None, description="Brand name of the product")
    category: Optional[str] = Field(None, description="Product category")
    availability: Optional[str] = Field(None, description="Availability status (e.g., In Stock, Out of Stock)")
    reviews: Optional[ProductReview] = Field(None, description="Review information")
    seller: Optional[str] = Field(None, description="Name of the seller")
    features: Optional[List[str]] = Field(None, description="List of product features/highlights")
    specifications: Optional[Dict[str, Any]] = Field(None, description="Technical specifications")
    source_site: str = Field(..., description="The e-commerce site this product was extracted from")
    
    class Config:
        """Pydantic model configuration."""
        json_schema_extra = {
            "example": {
                "name": "iPhone 13 Pro Max",
                "price": {
                    "current_price": "$999.99",
                    "original_price": "$1099.99",
                    "discount_percentage": "9%",
                    "currency": "USD"
                },
                "product_url": "https://www.example.com/products/iphone-13-pro-max",
                "image_url": "https://www.example.com/images/iphone-13-pro-max.jpg",
                "description": "Apple iPhone 13 Pro Max with 256GB storage",
                "brand": "Apple",
                "category": "Smartphones",
                "availability": "In Stock",
                "reviews": {
                    "rating": 4.7,
                    "count": 2345
                },
                "seller": "Example Electronics",
                "features": ["A15 Bionic chip", "Pro camera system", "5G capable"],
                "specifications": {
                    "storage": "256GB",
                    "display": "6.7-inch Super Retina XDR",
                    "battery": "Up to 28 hours video playback"
                },
                "source_site": "amazon.in"
            }
        }
