from product import (Base, session, Inventory, engine)
import datetime
import csv
import time

#A menu allowing the user to choose what action to take.
#If invalid entry is entered, an error message will show and ask them to try again.
def menu():
    while True:
        print('''
                \n*****MAIN MENU*****:
                \rv : VIEW
                \ra : ADD
                \rb : BACKUP
            ''')
        users_choice = input('Please select a option:  ').lower()
        if users_choice in ['v', 'a', 'b']:
            return users_choice
        else:
            users_choice = input('''
            \n**********MENU ERROR***********
            \rInvalid Option (v = View, a = Add, b = Backup)
            \rPress Enter to try again.
            \r*****************************''')


#Before placing the date into the db, it will clean the date.
def clean_date(date_str):
    date_split = date_str.split('/')
    day = int(date_split[1])
    month = int(date_split[0])
    year = int(date_split[2])

    return datetime.date(year, month, day)


#Before placing the price into the db, it will remove the '$' symbol and covert it to a integer.
def clean_price(price_str):
        price_split = price_str.split('$')[1]
        price = float(price_split)
        return int(price * 100)


#Cleaning the date before it's place in the db.
def clean_id(id_str, options):
    try:
        product_id = int(id_str)
    except ValueError:
        input('''
        \n**********ID ERROR***********
        \rThe ID should be an Integer.
        \rPress Enter to try again.
        \r*****************************''')
        return
    else:
        if product_id in options:
            return product_id
        else:
            input(f'''
            \n**********ID ERROR*******
            \rThe ID isn't valid.
            \r{options}
            \rPress Enter to try again.
            \r*************************''')
        return

# Adding the CSV data to 'inventroy.db'.
def add_csv():
    with open('store-inventory/inventory.csv') as csvfile:
        data = csv.DictReader(csvfile)
        for row in data:
            product_in_db = session.query(Inventory).filter(Inventory.product_name==row['product_name']).one_or_none()
            product_name = row['product_name']
            product_quantity = row['product_quantity']
            product_quantity = int(product_quantity)
            product_price = clean_price(row['product_price'])
            date_updated = clean_date(row['date_updated'])
            new_product = Inventory(product_name=product_name, product_price=product_price, product_quantity=product_quantity, date_updated=date_updated)
            #If doesn't exist in db, then add it.
            if product_in_db == None:
                session.add(new_product)
            else:
                #If already exists. Update the 'product_quantity', 'product_price' and 'date_updated'.
                if session.query(Inventory).filter(Inventory.date_updated < new_product.date_updated):
                    session.query(Inventory).filter(Inventory.product_name==new_product.product_name).update({
                        Inventory.product_quantity: new_product.product_quantity,
                        Inventory.product_price: new_product.product_price,
                        Inventory.date_updated: new_product.date_updated})
                
        session.commit()



def database_backup():
    #Exports a back of the database to a CSV file.
    with open('inventory_backup.csv', 'w') as csvfile:
        headers = ['product_id', 'product_name', 'product_quantity', 'product_price', 'date_updated']
        backup = csv.DictWriter(csvfile, fieldnames=headers)
        backup.writeheader()

        for product in session.query(Inventory).order_by(Inventory.product_id).all():
            product_price = '$' + str(product.product_price / 100)
            product_date = product.date_updated.strftime('%m/%d/%Y')
            backup.writerow({'product_id': product.product_id, 'product_name': product.product_name, 'product_price': product_price, 'product_quantity': str(product.product_quantity), 'date_updated': product_date})



def view_database():
    #Asks the user for a valid 'product_id' and prints it out.
    # Creating an empty array to hold all the product ids.
    ids_available = []
    # Loops over the session and appends all the 'product IDs' into the 'ids_available' array.
    for product in session.query(Inventory):
        ids_available.append(product.product_id)
    id_error = True
    # Prints out the choices that are available to be viewed.
    # Takes the 'Product ID' that the user wants to view.
    # Takes the 'Product ID' the user wants to view an passes it to the 'clean_id' function that turns it into a Int and checks if it's valid and is available in the 'ids_available' array.
    while id_error:
        product_id_choice = input(f'''
            \nID OPTIONS): {ids_available}
            \rProduct ID: ''')
        product_id_choice = clean_id(product_id_choice, ids_available)
        # Checks the type of the user choice is an Integer.
        if type(product_id_choice) == int:
            id_error = False
    # A query to print out the 'Product Name' of the 'Product ID' the user wants to see.
    the_product = session.query(Inventory).filter(Inventory.product_id == product_id_choice).first()
    print(f'''
    \nProduct Name: {the_product.product_name}
    \rProduct Price: ${int(the_product.product_price)/100}
    \rProduct Quantity: {the_product.product_quantity}
    \rDate Updated: {the_product.date_updated}''')
    

def add_product():
    #Add a new product to the database.
    # Create a function to handle adding a new product to the database
    product_name = input('Product Name: ')

    product_quantity = input('Product Quantity: ')
    try:
        product_quantity = int(product_quantity)
    except ValueError:
        input('''
        \n******ERROR******
        \rInvalid Value Entered.
        \rPress Enter to try again.
        \r*****************
        ''')
        return

    product_price = input('Product Price (E.g. 25.89): ')
    try:
        product_price = float(product_price)
        product_price = (product_price * 100)
    except ValueError:
        input('''
        \n******ERROR******
        \rInvalid Value Entered.
        \rPress Enter to try again.
        \r*****************
        ''')
        return

    #Taking in the current date and passing it through.
    date_updated = datetime.date.today().strftime('%m/%d/%Y')
    date_updated = clean_date(date_updated)

    new_product = Inventory(product_name=product_name, product_quantity=product_quantity, product_price=product_price, date_updated=date_updated)

    #Updating the 'product_quantity', 'product_price' and 'date_updated' if the 'product_name' already exists in the db.
    #Otherwise, create a new product and commit it.
    if session.query(Inventory).filter(Inventory.product_name==new_product.product_name).first():
        session.query(Inventory).filter(Inventory.product_name==new_product.product_name).update({
            Inventory.product_quantity: new_product.product_quantity,
            Inventory.product_price: new_product.product_price,
            Inventory.date_updated: new_product.date_updated})

    else:
        session.add(new_product)
        session.commit()
        print('****PRODUCT UPDATED/CREATE****')
        time.sleep(1.5)

def app():
    add_csv()
    app_running = True
    while app_running:
        choice = menu()
        # This choice allows the user to view a particular product.
        if choice == 'v':
            view_database()
        elif choice == 'a':
            add_product()
        else :
            # Create a function to handle making a backup of the database. The backup should be written to a .csv file.
            database_backup()
            print("****CSV EXPORT COMPLETED****")
            time.sleep(1.5)


if __name__ == '__main__':
    #This will connect our engine with our model class to create our database table.
    Base.metadata.create_all(engine)
    app()

