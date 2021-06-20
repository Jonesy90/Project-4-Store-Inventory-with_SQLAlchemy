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
        data = csv.reader(csvfile)
        data.__next__() #Skips the header row of the CSV file.
        for row in data:
            product_name = row[0]
            product_price = clean_price(row[1])
            product_quantity = row[2]
            date_updated = clean_date(row[3])
            new_product = Inventory(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)
            session.add(new_product)
        session.commit()


def app():
    app_running = True
    while app_running:
        choice = menu()
        if choice == 'v':
            # Create a function to handle getting and displaying a product by its product_id.
            id_selection = input('\nPlease enter the Product ID you wish to view: ')
            for product in session.query(Inventory):
                filter(Inventory.product_id == id_selection)
                print(product.product_name)
        elif choice == 'a':
            # Create a function to handle adding a new product to the database
            pass
        else :
            # Create a function to handle making a backup of the database. The backup should be written to a .csv file.
            pass



if __name__ == '__main__':
    #This will connect our engine with our model class to create our database table.
    Base.metadata.create_all(engine)
    app()
    # add_csv()

    # for product in session.query(Inventory):
    #     print(product)

