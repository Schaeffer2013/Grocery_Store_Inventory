from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import csv
from datetime import datetime

engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column('Brand Name', String)

    def __repr__(self):
        return f'{self.brand_name}'


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Product Quantity', Integer)
    product_price = Column('Product Price', Integer)
    date_updated = Column('Date Updated', Date)
    brand_id = Column(Integer, ForeignKey('brands.brand_id'))

    def __repr__(self):
        return f'Product Name: {self.product_name}  Product Quantity: {self.product_quantity} Product Price: {self.product_price} Date Updated: {self.date_updated}'
    


     

