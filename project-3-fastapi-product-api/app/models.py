"""
Pydantic data schemas for request validation and response serialization
"""
from typing import List, Optional, Generic, TypeVar, Dict, Any
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime, timezone

T = TypeVar("T")


class ProductBase(BaseModel):
    """Base fields shared across product schemas"""
    product_id: str = Field(..., description="Unique product identifier (e.g. slug or SKU)", json_schema_extra={"example": "its-only-the-himalayas_981"})
    title: str = Field(..., description="Product title/name", json_schema_extra={"example": "It's Only the Himalayas"})
    url: Optional[str] = Field(None, description="Source page URL", json_schema_extra={"example": "http://books.toscrape.com/catalogue/its-only-the-himalayas_981/index.html"})
    price: float = Field(..., ge=0, description="Product price", json_schema_extra={"example": 45.17})
    original_price: Optional[float] = Field(None, ge=0, description="Original list price", json_schema_extra={"example": 45.17})
    discount: Optional[float] = Field(0.0, ge=0, description="Discount amount or percentage", json_schema_extra={"example": 0.0})
    currency: Optional[str] = Field("GBP", description="Price currency code", json_schema_extra={"example": "GBP"})
    rating: Optional[float] = Field(0.0, ge=0, le=5.0, description="Star rating (0.0 to 5.0)", json_schema_extra={"example": 4.5})
    reviews_count: Optional[int] = Field(0, ge=0, description="Total user reviews", json_schema_extra={"example": 12})
    availability: Optional[str] = Field("In stock", description="Stock availability status", json_schema_extra={"example": "In stock (19 available)"})
    category: Optional[str] = Field("Default", description="Product category taxonomy", json_schema_extra={"example": "Travel"})
    image_url: Optional[str] = Field(None, description="Direct URL to product image", json_schema_extra={"example": "http://books.toscrape.com/media/cache/6d/41/6d418a73cc7d4ecfd75ca11d854041db.jpg"})
    source_website: Optional[str] = Field("books.toscrape.com", description="Scraped domain", json_schema_extra={"example": "books.toscrape.com"})


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    scraped_date: Optional[str] = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class ProductUpdate(BaseModel):
    """Schema for partially updating a product (PATCH/PUT)"""
    title: Optional[str] = None
    url: Optional[str] = None
    price: Optional[float] = Field(None, ge=0)
    original_price: Optional[float] = Field(None, ge=0)
    discount: Optional[float] = Field(None, ge=0)
    currency: Optional[str] = None
    rating: Optional[float] = Field(None, ge=0, le=5.0)
    reviews_count: Optional[int] = Field(None, ge=0)
    availability: Optional[str] = None
    category: Optional[str] = None
    image_url: Optional[str] = None
    source_website: Optional[str] = None


class ProductResponse(ProductBase):
    """Schema for returning product data to consumers"""
    id: Optional[str] = Field(None, description="MongoDB ObjectId string")
    scraped_date: Optional[str] = Field(None, description="ISO timestamp of when the product was scraped")

    model_config = ConfigDict(populate_by_name=True, from_attributes=True)


class PaginatedResponse(BaseModel, Generic[T]):
    """Standard generic pagination envelope"""
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool


class CategoryStat(BaseModel):
    """Category aggregated metrics"""
    category: str
    count: int
    avg_price: float
    min_price: float
    max_price: float
    avg_rating: float


class PriceDistributionBucket(BaseModel):
    """Price bucket distribution"""
    label: str
    min_price: float
    max_price: Optional[float]
    count: int
    percentage: float


class AnalyticsOverview(BaseModel):
    """High-level catalog analytics overview"""
    total_products: int
    avg_price: float
    min_price: float
    max_price: float
    avg_rating: float
    in_stock_count: int
    out_of_stock_count: int
    total_categories: int


class QuoteResponse(BaseModel):
    """Schema for quotes extracted via dynamic crawler (Project 2 integration)"""
    id: Optional[str] = None
    text: str
    author: str
    author_url: Optional[str] = None
    tags: List[str] = []
    source: Optional[str] = None
    scraped_date: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response schema"""
    status: str
    app_name: str
    version: str
    environment: str
    database_connected: bool
    products_count: int
    quotes_count: int
    response_time_ms: float
    timestamp: str


class MessageResponse(BaseModel):
    """Standard message response"""
    message: str
    success: bool
    details: Optional[Dict[str, Any]] = None
