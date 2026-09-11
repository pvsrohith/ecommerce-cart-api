from typing import List
from datetime import datetime

from pydantic import BaseModel

class ProductCreate(BaseModel):
    name: str
    price: float
    stock: int = 0

class ProductOut(ProductCreate):
    id: int

    class Config:
        from_attributes = True

class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemOut(BaseModel):
    id: int
    product: ProductOut
    quantity: int

    class Config:
        from_attributes = True

class CartOut(BaseModel):
    id: int
    created_at: datetime
    items: List[CartItemOut]
    total: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    id: int
    cart_id: int
    total: float
    created_at: datetime

    class Config:
        from_attributes = True
