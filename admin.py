import os
import sqlite3
import tkinter
from style import style_admin, style_add_produt

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
        window["bg"] = "white"
        add_product()
    else:
        label_error_admin["fg"] = "#FF0505"


def add_product():
    frame_main.place_forget()
    frame_product.place(x=0, y=0)
    
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
window.geometry("1080x720")
window.resizable(False, False)
window["bg"] = style_admin.main_color

# frame principale
frame_main = tkinter.Frame(window, bg=style_admin.main_color)
frame_main.place(x=200, y=200, )

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

bnt_connection = tkinter.Button(frame_main, text="Se connecter", command=check_admin)
bnt_connection.grid(row=5, column=0, ipady=2, ipadx=10, pady=5, sticky="we")

# frame ajoute produit
frame_product = tkinter.Frame(window, bg="white")
frame_search = tkinter.Frame(frame_product, width=270, bg="grey")
frame_search.grid(row=1, column=0, sticky="we", ipady=15)

label_title = tkinter.Label(frame_product, text="POPO FOOD", fg="white", font=style_add_produt.font_title, bg=style_admin.main_color, width=70,)
label_title.grid(row=0, column=0, sticky="we", ipady=25)

enter_search = tkinter.Entry(frame_search)
enter_search.grid(row=0, column=0, sticky="w", padx=30)
bnt_search = tkinter.Button(frame_search, text="Rechercher")
bnt_search.grid(row=0, column=1, padx=20, sticky="w", ipady=3, ipadx=2)


label_list_product = tkinter.Label(frame_product, text="Liste des produits en vente")
label_list_product.grid(row=2, column=0)

bnt_add_product = tkinter.Button(frame_product, text="Ahouter un produit")
bnt_add_product.grid(row=2, column=1)

window.mainloop()





