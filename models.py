from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///inventory.db', echo=True)
Base = declarative_base()

class Brand(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True)
    brand_name = Column(String)

    def __repr__(self):
       return f'' 

