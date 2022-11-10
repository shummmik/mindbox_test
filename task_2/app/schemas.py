from typing import List, Optional

from pydantic import BaseModel


class ProductName(BaseModel):
    product_name: str

    class Config:
        orm_mode = True


class Product(ProductName):
    id_product: int


class CategoryName(BaseModel):
    category_name: str

    class Config:
        orm_mode = True


class Category(CategoryName):
    id_category: int


class ProductOut(Product):
    categories: List[Category]


class CategoryOut(Category):
    products: List[Product]


class Pairs(BaseModel):
    product: ProductName
    category: CategoryName

    class Config:
        orm_mode = True
