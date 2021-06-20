#source ./env/bin/activate

from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#This will create a locall database on my computer.
engine = create_engine('sqlite:///inventory.db', echo=False)
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base() #This base maps our models to the database.

class Inventory(Base):
    __tablename__ = 'inventory'

    product_id = Column(Integer, primary_key=True)
    product_name = Column('Product Name', String)
    product_quantity = Column('Procut Quantity', Integer)
    product_price = Column('Product Price', Integer) #Will be stored as Integer and converted.
    date_updated = Column('Date Updated', Date)

    def __repr__(self):
        return f'<Inventory(Product Name={self.product_name}, Product Quantity={self.product_quantity}, Product Price={self.product_price}, Date Updated={self.date_updated})'





    