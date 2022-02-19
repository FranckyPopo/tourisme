import tkinter
from tkinter import ttk
from style import style_bouton_connection, style_admin


def display_recording():
    frame_recording.place_forget()
    frame_recording.place(x=200, y=100)
    window.config(bg="#EBEBEB")


def display_connection():
    pass

window = tkinter.Tk()
window.geometry("1126x720")
window.resizable(False, False)
window.title("POPO FOOD")
window.config(bg=style_admin.main_color)

# frame connection ou inscription
frame_choice = tkinter.Frame(window, bg=style_admin.main_color)
frame_choice.place(x=200, y=150)

bnt_connection = tkinter.Button(frame_choice, text="Se connecter", **style_bouton_connection.style_bouton_connection, command=display_connection)
bnt_connection.grid(row=0, column=0, **style_bouton_connection.forme_bouton, sticky="we")

bnt_recording = tkinter.Button(frame_choice, text="S'inscrire", **style_bouton_connection.style_bouton_connection, command=display_recording)
bnt_recording.grid(row=1, column=0, pady=10, sticky="we", **style_bouton_connection.forme_bouton)

# frame enregistrement
frame_recording = tkinter.Frame(window, bg="#EBEBEB")

label_last_name = tkinter.Label(frame_recording, text="Nom", bg="#EBEBEB")
label_last_name.grid(row=0, column=0, sticky="w")
enter_last_name = tkinter.Entry(frame_recording, highlightbackground="white")
enter_last_name.grid(row=1, column=0, sticky="we")

label_first_name = tkinter.Label(frame_recording, text="Prénom", bg="#EBEBEB")
label_first_name.grid(row=2, column=0, sticky="w")
enter_first_name = tkinter.Entry(frame_recording, highlightbackground="white")
enter_first_name.grid(row=3, column=0, sticky="we")

label_email = tkinter.Label(frame_recording, text="Email", bg="#EBEBEB")
label_email.grid(row=4, column=0, sticky="w")
enter_email = tkinter.Entry(frame_recording, highlightbackground="white")
enter_email.grid(row=5, column=0, sticky="we")

sex = ["Homme", "Femme"]
label_genre_sex = tkinter.Label(frame_recording, text="Genre", bg="#EBEBEB")
label_genre_sex.grid(row=6, column=0, sticky="w")
enter_genre_sexe = ttk.Combobox(frame_recording, values=sex)
enter_genre_sexe.grid(row=7, column=0, sticky="we")

label_password = tkinter.Label(frame_recording, text="Mot de passe", bg="#EBEBEB")
label_password.grid(row=8, column=0, sticky="w")
enter_password = tkinter.Entry(frame_recording, highlightbackground="white")
enter_password.grid(row=9, column=0, sticky="we")            
                 
label_password = tkinter.Label(frame_recording, text="Confirmer le mot de passe", bg="#EBEBEB")
label_email.grid(row=10, column=0, sticky="we")
enter_email = tkinter.Entry(frame_recording, highlightbackground="white")
enter_email.grid(row=11, column=0, sticky="we")

label_error_recording = tkinter.Label(frame_recording, text="Une erreur est survenue lors de l'enregistrement")
label_error_recording.grid(row=12, column=0, sticky="w", pady=10)

bnt_valided_recording = tkinter.Button(frame_recording, text="S'inscrire", highlightbackground="white")
bnt_valided_recording.grid(row=13, column=0, sticky="we")

window.mainloop()