from models import (Base, session, engine, Brand, Product)

#import models
#main menu - add, search, analysis, exit, view
#add products to the database
#edit products
#delete products
#search products
#data cleaning
#loop runs program


if __name__ == '__main__':
    Base.metadata.create_all(engine)