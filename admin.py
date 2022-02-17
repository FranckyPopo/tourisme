import os
import sqlite3
import tkinter
from tkinter import messagebox
from functools import partial
from style import style_admin, style_add_produt


account = {"user": "nan", "password": "nan"}
root_folder = os.getcwd()
folder_data = os.path.join(root_folder, "data")
os.makedirs(folder_data, exist_ok=True)

# BD
path_list_products = folder_data + "/" + "list_products.bd"

def window_modify_product(name_product):
    
    
    def modify_product():
        new_name = enter_new_name_product.get().strip()
        try:
            new_quantity = int(enter_new_quantity_product.get())
        except ValueError:
            label_error_safeguard_product.config(fg="#FF0505")
        else:
            d = {
                "old_name": name_product,
                "new_name": new_name,
                "new_quantity": new_quantity
            }
            conn = sqlite3.connect(path_list_products)
            cursor = conn.cursor()
            cursor.execute("""UPDATE list_products SET name_product=:new_name,  quantity_product=:new_quantity 
                        WHERE name_product=:old_name""", d
            )
            conn.commit()
            conn.close()
            admin_space()
    
    
    root = tkinter.Toplevel()
    root.geometry("480x320")
    root.resizable(False, False)
    root.title("Ajout produit")
    root.config(bg=style_admin.main_color)
    frame_modify_product = tkinter.Frame(root,  bg=style_admin.main_color)
    frame_modify_product.pack(expand="yes")
    
    label_new_name_product = tkinter.Label(frame_modify_product, text="Nouveau nom du produit", bg=style_admin.main_color, font=("Roboto", 18), fg="white", justify="left")
    label_new_name_product.grid(row=0, column=0, sticky="w")
    enter_new_name_product = tkinter.Entry(frame_modify_product)
    enter_new_name_product.grid(row=1, column=0, sticky="we", pady=5)
    
    label_new_quantity_product = tkinter.Label(frame_modify_product, text="Nouvelle quantité du produit", bg=style_admin.main_color, font=("Roboto", 18), fg="white", justify="left")
    label_new_quantity_product.grid(row=2, column=0, sticky="w")
    enter_new_quantity_product = tkinter.Entry(frame_modify_product)
    enter_new_quantity_product.grid(row=3, column=0, sticky="we", pady=5)
    
    label_error_safeguard_product = tkinter.Label(frame_modify_product, text="Un erreur est survenue lors de la sauvegarde du produit", bg=style_admin.main_color, fg=style_admin.main_color, font=("Roboto", 12, "bold"))
    label_error_safeguard_product.grid(row=4, column=0, pady=5)

    bnt_safeguard_product = tkinter.Button(frame_modify_product, text="Sauvegarder les modifications", command=modify_product)
    bnt_safeguard_product.grid(row=5, column=0, sticky="we", ipadx=3, ipady=2, pady=5)


def delete_product(name_product, *labels_delete):
    for label in labels_delete:
        label.grid_forget()
    
    d = {"product_delete": name_product}
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM list_products WHERE name_product=:product_delete", d)
    conn.commit()
    conn.close()
    

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
    frame_list_product.grid(row=4, column=0, sticky="w")
    
    label_title_name_product = tkinter.Label(frame_admin_space, text="Nom produit", font=("Roboto", 24), bg="white")
    label_title_name_product.grid(row=3, column=0, padx=30, sticky="w")
    
    label_title_quantity_product = tkinter.Label(frame_admin_space, text="Quantité en stock", font=("Roboto", 24), bg="white")
    label_title_quantity_product.grid(row=3, column=0, padx=255, sticky="w")
    
    # On affiche la liste de tout les produits
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE IF NOT EXISTS list_products (
                    name_product text,
                    quantity_product int)""")
    data = cursor.execute("SELECT * FROM list_products")
    list_product = data.fetchall()
    conn.commit()
    conn.close()

    for widget in frame_list_product.winfo_children():
        widget.grid_forget()
    
    i = 1
    for product in list_product:
        name_product = product[0]
        quantity_product = product[1]
        
        label_product = tkinter.Label(frame_list_product, text=name_product, font=("Roboto", 18), bg="white")
        label_product.grid(row=i, column=0, sticky="w", padx=30, pady=5)
        
        label_quantity = tkinter.Label(frame_list_product, text=quantity_product, font=("Roboto", 18), bg="white")
        label_quantity.grid(row=i, column=1, sticky="w", padx=120, pady=5) 

        bnt_modify = tkinter.Button(frame_list_product, text="Modifier", command=partial(window_modify_product, name_product), relief="flat")
        bnt_modify.grid(row=i, column=2, ipadx=3, ipady=2, pady=5)  
        
        bnt_delete = tkinter.Button(frame_list_product, text="Supprimer", relief="flat")
        
        bnt_delete["command"] = partial(delete_product, name_product, label_product, label_quantity, bnt_modify, bnt_delete)
        bnt_delete.grid(row=i, column=3, ipadx=3, ipady=2, pady=5)    
        i += 1


def window_add_product():
    
    
    def add_product():
        name_product = enter_name_product.get().strip()
        try:
            quantity_product = int(enter_quantity_product.get())
        except ValueError:
            label_error_add_product.config(fg="#FF0505")
        else:
            conn = sqlite3.connect(path_list_products)
            cursor = conn.cursor()
            data = cursor.execute("SELECT * FROM list_products")
            list_products = data.fetchall()
            conn.commit()
            conn.close()
            
            for produit in list_products:
                if produit[0] == name_product:
                    label_error_add_product.config(fg="#FF0505")
                    break
            else:
                product = {"name_product": name_product, "quantity_product": quantity_product}
                conn = sqlite3.connect(path_list_products)
                cursor = conn.cursor()
                cursor.execute("INSERT INTO list_products VALUES (:name_product, :quantity_product)", product)
                conn.commit()
                conn.close()
                label_error_add_product.config(fg=style_admin.main_color)
                enter_name_product.delete(0, "end")
                enter_quantity_product.delete(0, "end")
                messagebox.showinfo("Ajout produit", "Félicitation le produit a été ajouté avec succès")
                admin_space()
        

    root = tkinter.Toplevel()
    root.geometry("480x320")
    root.resizable(False, False)
    root.title("Ajout produit")
    root.config(bg=style_admin.main_color)
    frame_add_product = tkinter.Frame(root,  bg=style_admin.main_color)
    frame_add_product.pack(expand="yes")
    
    label_name_product = tkinter.Label(frame_add_product, text="Nom du produit", bg=style_admin.main_color, font=("Roboto", 18), fg="white", justify="left")
    label_name_product.grid(row=0, column=0, sticky="w")
    enter_name_product = tkinter.Entry(frame_add_product)
    enter_name_product.grid(row=1, column=0, sticky="we", pady=5)
    
    label_quantity_product = tkinter.Label(frame_add_product, text="Quantité du produit", bg=style_admin.main_color, font=("Roboto", 18), fg="white", justify="left")
    label_quantity_product.grid(row=2, column=0, sticky="w")
    enter_quantity_product = tkinter.Entry(frame_add_product)
    enter_quantity_product.grid(row=3, column=0, sticky="we", pady=5)
    
    label_error_add_product = tkinter.Label(frame_add_product, text="Un erreur est survenur lors de l'ajout du produit", bg=style_admin.main_color, fg=style_admin.main_color, font=("Roboto", 12, "bold"))
    label_error_add_product.grid(row=4, column=0, pady=5)

    bnt_add_product = tkinter.Button(frame_add_product, text="Ajouter le produit", command=add_product)
    bnt_add_product.grid(row=5, column=0, sticky="we", ipadx=3, ipady=2, pady=5)


def search_product(event):
    x = list()
    product_search = enter_search.get()
    
    for windget in frame_list_product.winfo_children():
        windget.grid_forget()
    
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM list_products")
    list_product = data.fetchall()
    conn.commit()
    conn.close()
    
    for product in list_product:
        name_product = product[0]
        if product_search in name_product:
            x.append(product)
    
    i = 0
    for product in x:
        name_product = product[0]
        quantity_product = product[1]
        
        label_product = tkinter.Label(frame_list_product, text=name_product, font=("Roboto", 18), bg="white")
        label_product.grid(row=i, column=0, sticky="w", padx=30, pady=5)
        
        label_quantity = tkinter.Label(frame_list_product, text=quantity_product, font=("Roboto", 18), bg="white")
        label_quantity.grid(row=i, column=1, sticky="w", padx=120, pady=5) 

        bnt_modify = tkinter.Button(frame_list_product, text="Modifier", command=partial(window_modify_product, name_product), relief="flat")
        bnt_modify.grid(row=i, column=2, ipadx=3, ipady=2, pady=5)  
        
        bnt_delete = tkinter.Button(frame_list_product, text="Supprimer", relief="flat")
        
        bnt_delete["command"] = partial(delete_product, name_product, label_product, label_quantity, bnt_modify, bnt_delete)
        bnt_delete.grid(row=i, column=3, ipadx=3, ipady=2, pady=5)    
        i += 1
    
    
    

window = tkinter.Tk()
window.geometry("1126x720")
#window.resizable(False, False)
window.config(bg=style_admin.main_color)
window.title("POPO FOOD")

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
enter_search.bind("<Key>", search_product)
enter_search.grid(row=1, column=0, sticky="w", padx=30)
bnt_search = tkinter.Button(frame_search, text="Rechercher")
bnt_search.grid(row=1, column=1, sticky="w", ipady=3, ipadx=2)

label_list_product = tkinter.Label(frame_admin_space, text="Liste des produits en vente", bg="#FFFFFF", font=("Roboto", 30, "bold"))
label_list_product.grid(row=2, column=0, sticky="w", pady=30, padx=30)

bnt_add_product = tkinter.Button(frame_admin_space, text="Ajouter un nouveau produit", bg="#FFFFFF", command=window_add_product)
bnt_add_product.grid(row=2, column=0, sticky="e", pady=30, ipady=3, ipadx=2, padx=30)

window.mainloop()
