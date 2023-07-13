from models import (Base, session, engine, Brand, Product)
import datetime
import csv

def menu():
    while True:
        print('''*Grocery Store Inventory*
              \nChoose one of the following options:
              \nV) View a product's inventory
              \rN) Add a new product
              \rA) View analysis
              \rB) Make a backup of the entire inventory database
              ''')
        choice = input('What would you like to do? ')
        if choice in ['v', 'n', 'a', 'b']:
            return choice.lower()
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rV, N, A, or B. 
                  \rPress enter to try again ''')

#edit products
#delete products
#search products

def clean_quantity(quantity):
    product_quantity = int(quantity)
    return product_quantity

def clean_price(price_str):
    try:
        price_string = price_str.strip('$')
        price_float = float(price_string)
    except ValueError:
        input('''
              \n****** RPICE ERROR ******
              \rThe price should be a number without a currency symbol.
              \rEx: 9.99
              \rPress enter to try again.
              \r*************************''')
    else:
        return int(price_float * 100)
    

def clean_date(date_str):
    split_date = date_str.split('/')
    month = int(split_date[0])
    day = int(split_date[1].split(',')[0])
    year = int(split_date[2])
    return datetime.date(year, month, day)
 


def add_csv():
    with open('brands.csv') as csvfile:
        data = csv.reader(csvfile)
        rows = list(data)
        for brand_row in rows[1:]:
            brand_in_db = session.query(Brand).filter(Brand.brand_name==brand_row[0]).one_or_none()
            if brand_in_db == None:
                brand_name = brand_row[0]
                new_brand = Brand(brand_name=brand_name)
                session.add(new_brand)
        session.commit()
               

    with open('inventory.csv') as csvfile2:
        data = csv.reader(csvfile2)
        rows = list(data)
        for inventory_row in rows[1:]:
            product_in_db = session.query(Product).filter(Product.product_name==inventory_row[0]).one_or_none()
            if product_in_db == None:
                product_name = inventory_row[0]
                product_price = clean_price(inventory_row[1])
                product_quantity = clean_quantity(inventory_row[2])
                date_updated = clean_date(inventory_row[3])
                brand_id = session.query(Brand.brand_id).filter(Brand.brand_name==inventory_row[4])
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_id)
                session.add(new_product)
        session.commit()



def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            #view
            pass
        elif choice == 'n':
            #add new product
            product_name = input('Product Name: ')
            price_error =True
            while price_error:
                product_price = input('Product Price (Ex: 9.99): ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            product_quantity = input('Product Qunatity: ')
            date_updated = datetime.datetime.now()

        elif choice == 'a':
            #view analysis
            pass
        elif choice == 'b':
            #backup
            pass





if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()


    