from product import (Base, session, Inventory, engine)
import datetime
import csv

def menu():
    while True:
        print('''
                \n*****MAIN MENU*****:
                \rv : VIEW
                \ra : ADD
                \rb : BACKUP
            ''')
        users_choice = input('Please select a option:  ')
        if users_choice in ['v', 'a', 'b']:
            return users_choice
        else:
            print("Error -- INVALID ENTRY")


def clean_date(date_str):
    date_split = date_str.split('/')
    day = int(date_split[1])
    month = int(date_split[0])
    year = int(date_split[2])

    return datetime.date(year, month, day)


def clean_price(price_str):
    price_split = price_str.split('$')[1]
    price = float(price_split)
    return int(price * 100)


# Adding the CVS
def add_csv():
    with open('store-inventory/inventory.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            product_name = row['product_name']
            product_price = clean_price(row['product_price'])
            product_quantity = row['product_quantity']
            date_updated = clean_date(row['date_updated'])
            new_product = Inventory(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)
            session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            # Create a function to handle getting and displaying a product by its product_id.
            #Input message to ask the user which 'Product ID' they wish to view.
            id_selection = input('\nPlease enter the Product ID you wish to view: ')
            # A FOR LOOP to go over the session and filter out the product with the same value as the users selection. Once found, print the 'Product Name'.
            for product in session.query(Inventory):
                filter(Inventory.product_id == id_selection)
                print(f'{product.product_name}')
        elif choice == 'a':
            # Create a function to handle adding a new product to the database
            pass
        else :
            # Create a function to handle making a backup of the database. The backup should be written to a .csv file.
            pass



if __name__ == '__main__':
    #This will connect our engine with our model class to create our database table.
    Base.metadata.create_all(engine)
    # app()
    # add_csv()

    # for product in session.query(Inventory):
    #     print(product)

