import os
import sqlite3
import tkinter
from style import style_admin, style_add_produt


account = {"user": "nan", "password": "nan"}
root_folder = os.getcwd()
folder_data = os.path.join(root_folder, "data")
os.makedirs(folder_data, exist_ok=True)

# Basse de données
path_list_products = folder_data + "/" + "list_products.bd"

def check_admin():
    login = enter_user_admin.get()
    password = enter_password_admin.get()
    
    if login == account.get("user") and password == account.get("password"):
        window["bg"] = "white"
        admin_space()
    else:
        label_error_admin["fg"] = "#FF0505"


def admin_space():
    frame_main.place_forget()
    frame_admin_space.place(x=0, y=0)
    frame_list_product.grid(row=3, column=0, sticky="w")
    
    label_title_name_product = tkinter.Label(frame_list_product, text="Nom produit", font=("Roboto", 24), bg="white")
    label_title_name_product.grid(row=0, column=0, padx=30)
    
    label_title_quantity_product = tkinter.Label(frame_list_product, text="Quantité en stock", font=("Roboto", 24), bg="white")
    label_title_quantity_product.grid(row=0, column=1, padx=120)
    
    # On affiche la liste de tout les produits
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_products (
                    name_product text,
                    quantity_product int)""")
    data = cursor.execute("SELECT * FROM list_products")
    list_product = data.fetchall()
    conn.commit()

    i = 1
    for product in list_product:
        name_product = product[0]
        quantity_product = product[1]
        
        label_product = tkinter.Label(frame_list_product, text=name_product, font=("Roboto", 18), bg="white")
        label_product.grid(row=i, column=0, sticky="w", padx=30)
        
        label_quantity = tkinter.Label(frame_list_product, text=quantity_product, font=("Roboto", 18), bg="white")
        label_quantity.grid(row=i, column=1, sticky="w", padx=120) 

        bnt_modify = tkinter.Button(frame_list_product, text="Modifier", command=modify_product)
        bnt_modify.grid(row=i, column=2, ipadx=3, ipady=2)       
        i += 1


    
def add_product():
    name_product = input("Veuillez entrer le nom du produit: ")
    quantity_product = input("Veuillez entrer la quantité du produit")
    product = {"name_product": name_product, "quantity_product": quantity_product}
    
    if name_product and quantity_product.isdigit():
        conn = sqlite3.connect(path_list_products)
        cursor = conn.cursor()
        cursor.execute("INSERT INTO list_products VALUES (:name_product, :quantity_product)", product)
        conn.commit()
        admin_space()
    else:
        print('Veuillez entrer remplir tout les champs')
    

window = tkinter.Tk()
window.geometry("1126x720")
#window.resizable(False, False)
window["bg"] = style_admin.main_color

# frame principale
frame_main = tkinter.Frame(window, bg=style_admin.main_color)
frame_main.place(x=200, y=200)

label_user_admin = tkinter.Label(frame_main, text="Nom d'utilisateur", bg=style_admin.main_color, font=style_admin.font, fg=style_admin.fg)
label_user_admin.grid(row=0, column=0, sticky="w")
enter_user_admin = tkinter.Entry(frame_main)
enter_user_admin.insert(0, "nan")
enter_user_admin.grid(row=1, column=0, pady=5, sticky="we")

label_password_admin = tkinter.Label(frame_main, text="Mot de passe", bg=style_admin.main_color, font=style_admin.font, fg=style_admin.fg)
label_password_admin.grid(row=2, column=0, sticky="w")
enter_password_admin = tkinter.Entry(frame_main, bg="white")
enter_password_admin.insert(0, "nan")
enter_password_admin.grid(row=3, column=0, pady=5, sticky="we")

label_error_admin = tkinter.Label(frame_main, text="Veullez remplir tout les champs", fg=style_admin.main_color, bg=style_admin.main_color, font=("Roboto", 14, "bold"))
label_error_admin.grid(row=4, column=0, sticky="we", pady=5,)

bnt_connection = tkinter.Button(frame_main, text="Se connecter", command=check_admin)
bnt_connection.grid(row=5, column=0, ipady=2, ipadx=10, pady=5, sticky="we")

# frame ajoute produit
frame_admin_space = tkinter.Frame(window, bg="white")
frame_search = tkinter.Frame(frame_admin_space, width=270, bg="#E5E5E5")
frame_search.grid(row=1, column=0, sticky="we", ipady=10)
frame_list_product = tkinter.Frame(frame_admin_space, bg="white")

label_title = tkinter.Label(frame_admin_space, text="POPO FOOD", fg="white", font=style_add_produt.font_title, bg=style_admin.main_color, width=70)
label_title.grid(row=0, column=0, sticky="we", ipady=25)

label_x = tkinter.Label(frame_search, bg="#E5E5E5")
label_x.grid(row=0, column=0)

enter_search = tkinter.Entry(frame_search)
enter_search.grid(row=1, column=0, sticky="w", padx=30)
bnt_search = tkinter.Button(frame_search, text="Rechercher")
bnt_search.grid(row=1, column=1, sticky="w", ipady=3, ipadx=2)

label_list_product = tkinter.Label(frame_admin_space, text="Liste des produits en vente", bg="#FFFFFF", font=("Roboto", 30, "bold"))
label_list_product.grid(row=2, column=0, sticky="w", pady=30, padx=30)

bnt_add_product = tkinter.Button(frame_admin_space, text="Ajouter un nouveau produit", bg="#FFFFFF", command=add_product)
bnt_add_product.grid(row=2, column=0, sticky="e", pady=30, ipady=3, ipadx=2, padx=30)

window.mainloop()
