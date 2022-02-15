import os
import sqlite3
import tkinter
from style import style_admin

account_amdin = "nan"
password = "nan"

account = {"user": "nan", "password": "nan"}
root_folder = os.getcwd()
folder_data = os.path.join(root_folder, "data")
os.makedirs(folder_data, exist_ok=True)

# Basse de données
path_list_products = os.path.join(folder_data, "list_products.bd")


def check_admin():
    login = enter_user_admin.get()
    password = enter_password_admin.get()
    
    if login == account.get("user") and password == account.get("password"):
        add_product()
    else:
        label_error_admin["fg"] = "#FF0505"


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
    



window = tkinter.Tk()
window.geometry("720x480")
window.resizable(False, False)
window["bg"] = style_admin.main_color

frame_main = tkinter.Frame(window, bg=style_admin.main_color)
frame_main.grid(row=0, column=0, padx=250, pady=150)

label_user_admin = tkinter.Label(frame_main, text="Nom d'utilisateur", bg=style_admin.main_color, font=style_admin.font, fg=style_admin.fg)
label_user_admin.grid(row=0, column=0, sticky="w")
enter_user_admin = tkinter.Entry(frame_main)
enter_user_admin.grid(row=1, column=0, pady=5, sticky="we")

label_password_admin = tkinter.Label(frame_main, text="Mot de passe", bg=style_admin.main_color, font=style_admin.font, fg=style_admin.fg)
label_password_admin.grid(row=2, column=0, sticky="w")
enter_password_admin = tkinter.Entry(frame_main, bg="white")
enter_password_admin.grid(row=3, column=0, pady=5, sticky="we")

label_error_admin = tkinter.Label(frame_main, text="Veullez remplir tout les champs", fg=style_admin.main_color, bg=style_admin.main_color, font=("Roboto", 14, "bold"))
label_error_admin.grid(row=4, column=0, sticky="we", pady=5,)

bnt_connection = tkinter.Button(frame_main, text="Se connecter", command=check_admin, )
bnt_connection.grid(row=5, column=0, ipady=2, ipadx=10, pady=5, sticky="we")



window.mainloop()





