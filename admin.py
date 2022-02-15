import os
import sqlite3
import tkinter


def add_product():
    name_produt = input("Veuillez entrer le nom du produit: ")
    quantity_product = input("Veuillez entrer la quantité du produit")
    product = {"name_produt": name_produt, "quantity_product": quantity_product}
    
    if name_produt and quantity_product.isdigit():
        conn = sqlite3.connect(path_list_products)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS list_products (
                        name_product text,
                        quantity_product int        
        )""")
        cursor.execute("INSERT INTO list_products VALUES (:name_produt, :quantity_product)", product)



        conn.commit()
    else:
        print('Veuillez entrer remplir tout les champs')
    

account = {"user": "nan", "password": "nan"}

root_folder = os.getcwd()
folder_data = os.path.join(root_folder, "data")
os.makedirs(folder_data, exist_ok=True)

# Basse de données
path_list_products = os.path.join(folder_data, "list_products.bd")

account_amdin = "nan"
password = "nan"

if account_amdin == account.get("user") and password == account.get("password"):
    add_product()
else:
    print('Mot de passe incorrete')
