from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import String, Integer, Column, MetaData, Table, ForeignKey

metadata_obj = MetaData(schema="app")


# product_category = Table(
#     "product_category",
#     metadata_obj,
#     Column("id_product", ForeignKey("product.id_product"),primary_key=True),
#     Column("id_category", ForeignKey("category.id_category"),primary_key=True),
# )


class Product(Base):
    __tablename__ = 'product'
    __table_args__ = {'schema': 'app'}
    id_product = Column(Integer, primary_key=True)
    product_name = Column(String(50), nullable=False)

    categories = relationship(
      'Category', 
      secondary='app.product_category', 
      back_populates="products"
    )


class Category(Base):
    __tablename__ = 'category'
    __table_args__ = {'schema': 'app'}
    id_category = Column(Integer, primary_key=True)
    category_name = Column(String(50), nullable=False)

    products = relationship(
       'Product', 
       secondary='app.product_category', 
       back_populates="categories"
    )


class ProductCategory(Base):
    __tablename__ = 'product_category'
    __table_args__ = {'schema': 'app'}
    id_product = Column(Integer, ForeignKey(Product.id_product), primary_key=True)
    id_category = Column(Integer, ForeignKey(Category.id_category), primary_key=True)

    product = relationship('Product')
    category = relationship('Category')
