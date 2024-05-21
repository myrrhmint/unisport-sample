from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class Price(BaseModel):
    currency: str
    min_price: str
    max_price: str
    recommended_retail_price: str
    discount_percentage: str


class LabelItem(BaseModel):
    id: int
    name: str
    priority: int
    color: str
    background_color: str
    active: bool


class StockItem(BaseModel):
    pk: int
    sku_id: int
    size_id: int
    barcode: str
    order_by: int
    name: str
    name_short: str
    stock_info: str
    price: str
    recommended_retail_price: str
    discount_percentage: str
    supplier: str
    is_marketplace: bool
    availability: str


class ProductItem(BaseModel):
    id: str
    product_id: int
    style: str
    prices: Price
    name: str
    relative_url: str
    image: str
    delivery: str
    online: bool
    active: bool
    labels: List[LabelItem]
    is_customizable: bool
    paid_print: bool
    is_exclusive: bool
    stock: List[StockItem]
    customization_template_id: Optional[int]
    currency: str
    url: str
    attributes: Dict[str, Any]
