import tkinter
from tkinter import ttk
import os
import random
import sqlite3
from functools import partial
from PIL import Image, ImageTk
from style import style_admin, style_add_produt, style_client

root_folder = os.getcwd()
folder_data = os.path.join(root_folder, "data")
folder_img = os.path.join(root_folder, "img")
os.makedirs(folder_data, exist_ok=True)

# BD
path_list_client = folder_data + "/" + "list_client.bd"
path_list_products = folder_data + "/" + "list_products.bd"

i = 2

def display_menu():
    frame_container_connection.place_forget()
    frame_container_recording.place_forget()
    frame_price.grid(row=2, column=0, padx=900, pady=160)
    frame_main.place(x=0, y=0)


def display_recording():
    frame_choice.place_forget()
    frame_container_recording.place(x=0, y=0, width=1100)
    window.config(bg="#F7F7F7")

       
def display_connection():
    frame_choice.place_forget()
    frame_container_connection.place(x=0, y=0, width=1100)
    window.config(bg="#F7F7F7")
    enter_user_name.insert(0, "afri_123")
    enter_password_connection.insert(0, "pass")
    
    
def check_recording():
    last_name = enter_last_name.get()
    first_name = enter_first_name.get()
    user_name = enter_user.get()
    email = enter_email.get()
    genre = enter_genre_sexe.get()
    password_one = enter_password.get()
    password_two = enter_check_password.get()

    try:
        number_phone = int(enter_number_phone.get())
    except ValueError:
        label_error_recording.config(fg="red")
    else:
        conn = sqlite3.connect(path_list_client)
        cursor = conn.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS list_client (
                        last_name text, first_name text,
                        user_name text, email text,
                        number_phone int, genre text,
                        password text
                        )""")
        data_clients = cursor.execute("SELECT * FROM list_client")
        list_client = data_clients.fetchall()
        conn.commit()
        conn.close()
        
        for client in list_client:
            email_client = client[3]
            user_name_client = client[2]
            number_phone_client = client[4]
            
            if (password_one != password_two) or (user_name == user_name_client) or (number_phone == number_phone_client) or not last_name or email == email_client or not first_name or not genre:  
                label_error_recording.config(fg="red")
                break
        else:
            data_recording = {
                "last_name": last_name,
                "first_name": first_name,
                "user_name": user_name,
                "email": email,
                "number_phone": number_phone,
                "genre": genre,
                "password": password_one
            }
            conn = sqlite3.connect(path_list_client)
            cursor = conn.cursor()
            cursor.execute("""INSERT INTO list_client VALUES (:last_name, :first_name, :user_name, :email,
                            :number_phone, :genre, :password)""", data_recording)
            conn.commit()
            conn.close()
            display_menu()
    
    
def check_connection():
    user_name = enter_user_name.get()
    password = enter_password_connection.get()
    
    
    if user_name and password:
        conn = sqlite3.connect(path_list_client)
        cursor = conn.cursor()
        liste_client = cursor.execute("SELECT * FROM list_client").fetchall()
        conn.commit()
        conn.close()
        
        for client in liste_client:
            user_name_client = client[2]
            password_client = client[6]
            if user_name == user_name_client and password == password_client:
                display_menu()
                break
        else:
            label_error_connection.config(fg="red")
    else:
        label_error_connection.config(fg="red")


def cancel_recording():
    frame_container_recording.place_forget()
    frame_choice.place(x=200, y=150)    
    window.config(bg=style_admin.main_color)   


def cancel_connection():
    frame_container_connection.place_forget()
    frame_choice.place(x=200, y=150)    
    window.config(bg=style_admin.main_color)   
   
   
def popup(event):
    global i
    if i % 2 == 0:
        frame_pupop.place(x=980, y=35)
        i += 1
    else:
        frame_pupop.place_forget()
        i += 1


def list_product_favoris():
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    list_product = cursor.execute("SELECT * FROM list_products").fetchall()
    conn.commit()
    conn.close()

    r = 2
    i = 0
    for item in list_product:
        frame = tkinter.Frame(frame_product_favoris, bg="#F7F7F7", bd=1, relief="solid")
        frame.grid(row=r, column=i % 2, padx=20,)
        
        product = random.choice(list_product)
        name_product = product[0]
        price_product = product[2]
        
        label_name_product = tkinter.Label(frame, text=name_product, font=("Roboto", 18, "bold"), bg="#F7F7F7")
        label_name_product.grid(row=0, column=0, sticky="w", ipadx=10, ipady=5, pady=5)

        price = f"Prix: {price_product} FCFA"
        label_price = tkinter.Label(frame, text=price, font=("Roboto", 14, "bold"), bg="#F7F7F7")
        label_price.grid(row=1, column=0, sticky="w", ipadx=10, ipady=5)
        
        bnt_cash = tkinter.Button(frame, image=img_add_product, highlightbackground="#F7F7F7", command=partial(add_product_list_buy, name_product))
        bnt_cash.grid(row=1, column=1, padx=10, sticky="n")        
                
        if i % 2 != 0:
            r += 1
        if i == 1:
            break
        else:
            i += 1
    

def list_product():
    conn = sqlite3.connect(path_list_products)
    cursor = conn.cursor()
    list_product = cursor.execute("SELECT * FROM list_products").fetchall()
    conn.commit()
    conn.close()
    
    i = 0
    r = 2
    for item in list_product:
        frame = tkinter.Frame(frame_product, bg="#F7F7F7", bd=1, relief="solid")
        frame.grid(row=r, column=i % 2, pady=20, padx=5) 

        name_product = item[0]
        price_product = item[2]
        
        label_name_product = tkinter.Label(frame, text=name_product, font=("Roboto", 18, "bold"), bg="#F7F7F7")
        label_name_product.grid(row=0, column=0, sticky="w", ipadx=10, ipady=5, pady=5)

        price = f"Prix: {price_product} FCFA"
        label_price = tkinter.Label(frame, text=price, font=("Roboto", 14, "bold"), bg="#F7F7F7")
        label_price.grid(row=1, column=0, sticky="w", ipadx=10, ipady=5)
        
        bnt_cash = tkinter.Button(frame, image=img_add_product, highlightbackground="#F7F7F7",  command=partial(add_product_list_buy, name_product))
        bnt_cash.grid(row=1, column=1, padx=10, sticky="n")   
        
        
        if i % 2 != 0:
            r += 1 
        i += 1
        
        
def add_product_list_buy(name_product):
    quantity = 1
    d = {"name_product": name_product, "quantity_product": quantity}
    for item in list_product_buy:
        if item["name_product"] == name_product:
            item["quantity_product"] += quantity
            break
    else:
        list_product_buy.append(d) 
    refresh_p()
   

def less_product_list_buy(name_product, frame_del):
    for product in list_product_buy:
        if product["name_product"] == name_product:
            if product["quantity_product"] == 1:
                list_product_buy.remove(product) 
                refresh_p()
            else:
                product["quantity_product"] -= 1
                refresh_p()
            break
            
            

def del_product(event, name_product):
    print(event)
    print(name_product)
    for product in list_product_buy:
        if product["name_product"] == name_product:
            list_product_buy.remove(product)
            refresh_p()
            break
   
   
def refresh_p():    
    i = 1
    x = 0
    for frame in frame_price.winfo_children():
        if x != 0:
            frame.destroy()
        x += 1    
    
    for product in list_product_buy:
        name_product = product["name_product"]
        quantity = product["quantity_product"]
        frame = tkinter.Frame(frame_price, bg="#F7F7F7", bd=1, relief="solid")
        frame.grid(row=i, column=0, pady=15, padx=15, ipadx=5, sticky="we")
        
        label_title = tkinter.Label(frame, text=name_product, bg="#F7F7F7", font=("Arial", 14))
        label_title.grid(row=0, column=0, columnspan=2, sticky="w")
        
        label_quantity = tkinter.Label(frame, text=quantity, bg="#F7F7F7", font=("Arial", 14, "bold"))
        label_quantity.grid(row=0, column=3, sticky="e")
        
        bnt_add = tkinter.Button(frame, image=img_more, command=partial(add_product_list_buy, name_product))
        bnt_add.grid(row=1, column=0, sticky="w")
        
        bnt_delete_product = tkinter.Button(frame, image=img_less, highlightbackground="#F7F7F7", command=partial(less_product_list_buy, name_product, frame))
        bnt_delete_product.grid(row=1, column=1, padx=10, sticky="w")
                
        label_remove = tkinter.Label(frame, text="Retirer", bg="#F7F7F7", fg="red", font=("Arial", 14))
        label_remove.bind("<Button-1>", partial(del_product, name_product))
        label_remove.grid(row=1, column=3)
        i += 1
        

# event
def del_error(event):
    label_error_connection.config(fg="#F7F7F7")    
 
 
def refresh(event):
    list_product_favoris()
    list_product()
    

window = tkinter.Tk()   
window.geometry("1147x720")
window.resizable(False, False)
window.title("POPO FOOD")
window.config(bg=style_admin.main_color)

# Img
img_add = Image.open(f"{folder_img + '/' + 'ajouter-au-panier.png'}").resize((50, 50))
img_add_product = ImageTk.PhotoImage(img_add)

img_add_two = Image.open(f"{folder_img + '/' + 'ajouter-au-panier.png'}").resize((25, 25))
img_more = ImageTk.PhotoImage(img_add_two)

img_del = Image.open(f"{folder_img + '/' + 'icons_moins.png'}").resize((25, 25))
img_less = ImageTk.PhotoImage(img_del)

# frame connection ou inscription
frame_choice = tkinter.Frame(window, bg=style_admin.main_color)
frame_choice.place(x=200, y=150)

bnt_connection = tkinter.Button(frame_choice, text="Se connecter", command=display_connection)
bnt_connection.grid(row=0, column=0, sticky="we")

bnt_recording = tkinter.Button(frame_choice, text="S'inscrire", command=display_recording)
bnt_recording.grid(row=1, column=0, pady=10, sticky="we")

# frame connection
frame_container_connection = tkinter.Frame(window, bg="#F7F7F7")

frame_navbar_connection = tkinter.Frame(frame_container_connection, bg=style_admin.main_color)
frame_navbar_connection.grid(row=0, column=0)

label_title_connection = tkinter.Label(frame_navbar_connection, text="POPO FOOD", font=style_add_produt.font_title, bg=style_admin.main_color, justify="left", width=70, fg="white")
label_title_connection.grid(row=0, column=0)

frame_connection = tkinter.Frame(frame_container_connection, bg="#F7F7F7")
frame_connection.grid(row=1, column=0, sticky='w', pady=25, padx=60)

label_user_name = tkinter.Label(frame_connection, text="Nom d'utilisateur", bg="#F7F7F7", font=style_client.font)
label_user_name.grid(row=0, column=0, sticky="w", pady=4)
enter_user_name = tkinter.Entry(frame_connection, highlightbackground="white")
enter_user_name.bind("<Key>", del_error)
enter_user_name.grid(row=1, column=0, sticky="we", pady=4)

label_password = tkinter.Label(frame_connection, text="Mot de passe", bg="#F7F7F7", font=style_client.font)
label_password.grid(row=2, column=0, sticky="w", pady=4)
enter_password_connection = tkinter.Entry(frame_connection, highlightbackground="white")
enter_password_connection.bind("<Key>", del_error)
enter_password_connection.grid(row=3, column=0, sticky="we", pady=4)

label_error_connection = tkinter.Label(frame_connection, text="Une erreur est survenue lors de la connection", fg="#F7F7F7", bg="#F7F7F7", font=style_client.font)
label_error_connection.grid(row=4, column=0, sticky="w", pady=10)

bnt_valided_connection = tkinter.Button(frame_connection, text="Se connecter", highlightbackground="white", command=check_connection, font=("Roboto", 12, "bold"))
bnt_valided_connection.grid(row=5, column=0, sticky="we", pady=4, ipadx=3, ipady=2)

bnt_cancel_connection = tkinter.Button(frame_connection, text="Retour", font=("Roboto", 12, "bold"), command=cancel_connection)
bnt_cancel_connection.grid(row=6, column=0, sticky="we", pady=10, ipadx=3, ipady=2)

# frame enregistrement
frame_container_recording = tkinter.Frame(window, bg="#F7F7F7")

frame_navbar_recording = tkinter.Frame(frame_container_recording, bg=style_admin.main_color, width=500)
frame_navbar_recording.grid(row=0, column=0)

label_title_recording = tkinter.Label(frame_navbar_recording, text="POPO FOOD", font=style_add_produt.font_title, bg=style_admin.main_color, justify="left", width=70, fg="white")
label_title_recording.grid(row=0, column=0)

frame_recording = tkinter.Frame(frame_container_recording, bg="#F7F7F7")
frame_recording.grid(row=1, column=0, sticky='w', pady=25, padx=60)

label_last_name = tkinter.Label(frame_recording, text="Nom", bg="#F7F7F7", font=style_client.font)
label_last_name.grid(row=0, column=0, sticky="w", pady=4)
enter_last_name = tkinter.Entry(frame_recording, highlightbackground="white")
enter_last_name.grid(row=1, column=0, sticky="we", pady=4)

label_first_name = tkinter.Label(frame_recording, text="Prénom", bg="#F7F7F7", font=style_client.font)
label_first_name.grid(row=2, column=0, sticky="w", pady=4)
enter_first_name = tkinter.Entry(frame_recording, highlightbackground="white")
enter_first_name.grid(row=3, column=0, sticky="we", pady=4)

label_user = tkinter.Label(frame_recording, text="Nom d'utilisateur", bg="#F7F7F7", font=style_client.font)
label_user.grid(row=4, column=0, sticky="w", pady=4)
enter_user = tkinter.Entry(frame_recording, highlightbackground="white")
enter_user.grid(row=5, column=0, sticky="we", pady=4)

label_email = tkinter.Label(frame_recording, text="Email", bg="#F7F7F7", font=style_client.font)
label_email.grid(row=6, column=0, sticky="w", pady=4)
enter_email = tkinter.Entry(frame_recording, highlightbackground="white")
enter_email.grid(row=7, column=0, sticky="we", pady=4)

label_number_phone = tkinter.Label(frame_recording, text="Numéro de téléphone", bg="#F7F7F7", font=style_client.font)
label_number_phone.grid(row=8, column=0, sticky="w", pady=4)
enter_number_phone = tkinter.Entry(frame_recording, highlightbackground="white")
enter_number_phone.grid(row=9, column=0, sticky="we", pady=4)

sex = ["Homme", "Femme"]
label_genre_sex = tkinter.Label(frame_recording, text="Genre", bg="#F7F7F7", font=style_client.font)
label_genre_sex.grid(row=10, column=0, sticky="w", pady=4)
enter_genre_sexe = ttk.Combobox(frame_recording, values=sex)
enter_genre_sexe.current(0)
enter_genre_sexe.grid(row=11, column=0, sticky="we", pady=4)

label_password = tkinter.Label(frame_recording, text="Mot de passe", bg="#F7F7F7", font=style_client.font)
label_password.grid(row=12, column=0, sticky="w", pady=4)
enter_password = tkinter.Entry(frame_recording, highlightbackground="white")
enter_password.grid(row=13, column=0, sticky="we", pady=4)            
                 
label_check_password = tkinter.Label(frame_recording, text="Confirmer le mot de passe", bg="#F7F7F7", font=style_client.font)
label_check_password.grid(row=14, column=0, sticky="w", pady=4)
enter_check_password = tkinter.Entry(frame_recording, highlightbackground="white")
enter_check_password.grid(row=15, column=0, sticky="we", pady=4)

label_error_recording = tkinter.Label(frame_recording, text="Une erreur est survenue lors de l'enregistrement", fg="#F7F7F7", bg="#F7F7F7", font=style_client.font)
label_error_recording.grid(row=16, column=0, sticky="w", pady=10)

bnt_valided_recording = tkinter.Button(frame_recording, text="S'inscrire", highlightbackground="white", command=check_recording, font=("Roboto", 12, "bold"))
bnt_valided_recording.grid(row=17, column=0, sticky="we", pady=4, ipadx=3, ipady=2)

bnt_cancel_recording = tkinter.Button(frame_recording, text="Retour", font=("Roboto", 12, "bold"), command=cancel_recording)
bnt_cancel_recording.grid(row=18, column=0, sticky="we", pady=4, ipadx=3, ipady=10)

# frame menu
frame_main = tkinter.Frame(window, bg="#F7F7F7", bd=2, relief="solid")

frame_nav_menu = tkinter.Frame(frame_main, bg=style_admin.main_color, height=80)
frame_nav_menu.grid(row=0, column=0, ipadx=570)

label_logo = tkinter.Label(frame_nav_menu, text='POPO FOOD', fg="black", bg=style_admin.main_color, font=style_add_produt.font_title)
label_logo.bind("<Button-1>", refresh)
label_logo.place(x=40, y=15)

enter_search = tkinter.Entry(frame_nav_menu)
enter_search.place(x=500, y=25)

label_search = tkinter.Label(frame_nav_menu, text="Rechecher", fg="white", bg=style_admin.main_color, font=("roboto", 14))
label_search.place(x=620, y=20)

label_name = tkinter.Label(frame_nav_menu, text="XXXXX", fg="white", bg=style_admin.main_color, font=("roboto", 14, "bold"))
label_name.bind("<Button-1>", popup)
label_name.place(x=980, y=12)

# popup
frame_pupop = tkinter.Frame(frame_nav_menu, bg=style_admin.main_color)

label_count = tkinter.Label(frame_pupop, text="Mon compte",  bg=style_admin.main_color)
label_count.grid(row=1, column=0, sticky="w")

label_connection = tkinter.Label(frame_pupop, text="Déconnection",  bg=style_admin.main_color)
label_connection.grid(row=1, column=0, sticky="w")

# frame produtuit favoris
frame_product_favoris = tkinter.Frame(frame_main, bg="#F7F7F7")
frame_product_favoris.grid(row=2, column=0, sticky="w")

label_top = tkinter.Label(frame_product_favoris, text="Top des ventes", bg="#F7F7F7", font=("Roboto", 14))
label_top.grid(row=0, column=0, pady=30, sticky="w", padx=20)

# frame product
frame_product = tkinter.Frame(frame_main, bg="#F7F7F7")
frame_product.grid(row=3, column=0, pady=30, padx=25, sticky="w")

label_menu = tkinter.Label(frame_product, text="Menu", font=("Roboto", 14))
label_menu.grid(row=0, column=0, sticky="w")

# frame panier
list_product_buy = []
frame_price = tkinter.Frame(window, bg="#F7F7F7", bd=1, relief="solid")

label_achet = tkinter.Label(frame_price, justify="left", text="Top des ventes", font=("Roboto", 14), bg="#F7F7F7")
label_achet.grid(row=0, column=0)

list_product_favoris()
list_product()

window.mainloop()