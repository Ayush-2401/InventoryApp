from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

class Operator(Base):
    __tablename__='operators'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique = True, nullable = False)
    password = Column(String(100), nullable=False)

class Product(Base):
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    barcode = Column(String(50), unique=True)
    sku_id = Column(String(50), unique=True)
    category = Column(String(50))
    subcategory = Column(String(50))
    product_name = Column(String(100), nullable=False)
    description = Column(String(255))
    tax = Column(Float)
    price = Column(Float)
    unit = Column(String(20))
    image_path = Column(String(255))
    stock_quantity = Column(Float, default=0.0)

class GoodReceiving(Base):
    __tablename__ = 'goods_receiving'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    supplier_name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20))
    rate = Column(Float, nullable=False)
    total_rate = Column(Float)
    tax = Column(Float)
    receiving_date = Column(DateTime, default=datetime.now)

    product = relationship("Product")

class Sale(Base):
    __tablename__='sales'
    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    customer_name = Column(String(100), nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String(20))
    rate = Column(Float, nullable=False)
    total_rate = Column(Float)
    tax = Column(Float)
    sale_date = Column(DateTime, default=datetime.now)

    product = relationship("Product")