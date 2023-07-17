from models import (func, Base, session, engine, Brand, Product)
import datetime
import csv 
import time

def menu():
    while True:
        print('''*Grocery Store Inventory*
              \nChoose one of the following options:
              \nV) View a product's inventory
              \rN) Add a new product
              \rA) View analysis
              \rB) Make a backup of the entire inventory database
              \rE) Exit the program''')
        choice = input('What would you like to do? ')
        if choice in ['v', 'n', 'a', 'b', 'e']:
            return choice.lower()
        else:
            input('''
                  \rPlease choose one of the options above.
                  \rV, N, A, B, or E 
                  \rPress enter to try again ''')
            

def submenu():
    while True:
        print('''
              \r1) Edit
              \r2) Delete
              \r3) Return to main menu''')
        choice = input('What would you like to do? ')
        if choice in ['1', '2', '3']:
            return choice
        else:
            input('''
                  \rPlease choose one number of the options above.
                  \rAnumber from 1-3.
                  \rPress enter to try again.''')

def clean_id(id_str, id_options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
              \n****** ID ERROR ******
              \rThe id should be a number.
              \rPress enter to try again.
              \r**********************''')
        return
    else:
        if product_id in id_options:
            return product_id
        else:
            input(f'''
              \n****** ID ERROR ******
              \rOptions: {id_options}.
              \rPress enter to try again.
              \r**********************''')
            return
        

def clean_quantity(quantity):
    try:
        product_quantity = int(quantity)
    except ValueError:
        input('''
              \n****** QUANTITY ERROR ******
              \rThe quantity should be a number.
              \rPress enter to try again.
              \r****************************''')
        return
    else:
        return product_quantity


def clean_price(price_str):
    try:
        price_string = price_str.strip('$')
        price_float = float(price_string)
    except ValueError:
        input('''
              \n****** PRICE ERROR ******
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
 

def edit_check(column_name, current_value):
    print(f'\n****** EDIT {column_name} ******')
    if column_name == 'Product Price':
        print(f'\rCurrent Value: {current_value/100}')
    elif column_name == 'Date Updated':
        print(f'\rCurrent Value: {current_value.strftime("%m/%d/%Y")}')
    else:
        print(f'\rCurrent Value: {current_value}')

    if column_name == 'Date Updated' or column_name == 'Product Price':
        while True:
            changes = input('What would you like to change the value to?')
            if column_name == 'Date Updated':
                changes = clean_date(changes)
                if type(changes) == datetime.date:
                    return changes
            elif column_name == 'Product Price':
                changes = clean_price(changes)
                if type(changes) == int:
                    return changes
    else: 
        return input('What would you like to change the value to?')



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
            id_options = []
            for product in session.query(Product.product_id):
                id_options.append(product[0])
            id_error = True
            while id_error:
                id_choice = input(f'''
                    \nId Options: {id_options}
                    \rProduct id: ''')
                id_choice = clean_id(id_choice, id_options)
                if type(id_choice) == int:
                    id_error = False
            the_product = session.query(Product, Brand.brand_name).join(Brand, Product.brand_id == Brand.brand_id).filter(Product.product_id == id_choice).first()
            if the_product:
                product_name = the_product[0].product_name
                product_price = the_product[0].product_price / 100
                product_quantity = the_product[0].product_quantity
                brand_name = the_product[1]
                print(f'''
                    \nProduct Name: {product_name}
                    \rProduct Price: ${product_price}
                    \rProduct Quantity: {product_quantity}
                    \rBrand: {brand_name}''')
                sub_choice = submenu()
                if sub_choice == '1':
                    product_name = edit_check('Product Name', product_name)
                    product_price = edit_check('Product Price', product_price)
                    product_quantity = edit_check('Product Quantity', product_quantity)
                    date_updated = edit_check('Date Updated', date_updated)
                    session.commit()
                    print('Product Updated!')
                    time.sleep(1.5)
                if sub_choice == '2':
                    session.delete(the_product)
                    session.commit()
                    print('Product Deleted!')
                    time.sleep(1.5)

        elif choice == 'n':
            product_name = input('Product Name: ')
            price_error = True
            while price_error:
                product_price = input('Product Price (Ex: 9.99): ')
                product_price = clean_price(product_price)
                if type(product_price) == int:
                    price_error = False
            quantity_error = True
            while quantity_error:
                product_quantity = input('Product Qunatity: ')
                product_quantity = clean_quantity(product_quantity)
                if type(product_quantity) == int:
                    quantity_error = False
            brand_name_input = input('Brand Name: ')
            brand_name_in_db = session.query(Brand).filter(Brand.brand_name==brand_name_input).one_or_none()
            if brand_name_in_db == None:
                new_brand = Brand(brand_name=brand_name_input)
                session.add(new_brand)
                session.commit() 
                brand_name = session.query(Brand).filter(Brand.brand_name==brand_name).first().product_id
            else:
                brand_name = brand_name_in_db
                new_product = Product(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated, brand_id=brand_name)
            date_updated = datetime.datetime.now()
            session.add(new_product)
            session.commit()
            input('Product was added. Press enter to continue.')

        elif choice == 'a':
            most_expensive = session.query(Product.product_name).order_by(Product.product_price.desc()).first()
            least_expensice = session.query(Product.product_name).order_by(Product.product_price).first()
            total_products = session.query(Product).count()
            brand_most_product = session.query(Brand.brand_name).join(Product).group_by(Brand.brand_id).order_by(func.count(Product.product_id).desc()).first()
            brand_least_product = session.query(Brand.brand_name).join(Product).group_by(Brand.brand_id).order_by(func.count(Product.product_id)).first()
            print(f'''
                  \n******* PRODUCT ANALYSIS ******
                  \rMost Expensive Product: {most_expensive}
                  \rLeast Expensive Product: {least_expensice}
                  \rTotal amount of Products: {total_products}
                  \rBrand with most amount of Product: {brand_most_product}
                  \rBrand with least amount of Products: {brand_least_product}
                ''')
            input('\nPress enter to return to main menu.')
        elif choice == 'b':
                def backup_inventory():
                    inventory_data = session.query(Product.product_name, 
                                                   Product.product_price / 100, 
                                                   Product.product_quantity, 
                                                   Product.date_updated.strftime('%m/%d/%Y').label('date_updated'), 
                                                   Brand.brand_name).join(Brand).all()
                    field_names = ['product_name', 'product_price', 'product_quantity','date_updated', 'brand_name']
                    with open('backup_inventory.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerows(map(dict, inventory_data))
                def backup_brands():
                    brand_data = session.query(Brand.brand_name).all()
                    field_names = ['brand_name']
                    with open('backup_brands.csv', 'w', newline='') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=field_names)
                        writer.writeheader()
                        writer.writerows(map(dict, brand_data))
                backup_inventory()
                backup_brands()

        else:
            print('\nGOODBYE')
            app_running = False






if __name__ == '__main__':
    Base.metadata.create_all(engine)
    add_csv()
    app()


    