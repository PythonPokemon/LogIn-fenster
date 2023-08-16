import os
import sqlite3
import tkinter as tk
from tkinter import messagebox

DB_FOLDER = "user_data"
DB_FILE = "user_accounts.db"
LOGGED_IN_USERS_FILE = "last_logged_in_users.txt"

def initialize_database():
    if not os.path.exists(DB_FOLDER):
        os.makedirs(DB_FOLDER)
    conn = sqlite3.connect(os.path.join(DB_FOLDER, DB_FILE))
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT)''')
    conn.commit()
    conn.close()

def create_account(username, password):
    conn = sqlite3.connect(os.path.join(DB_FOLDER, DB_FILE))
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
    conn.commit()
    conn.close()

def login(username, password):
    conn = sqlite3.connect(os.path.join(DB_FOLDER, DB_FILE))
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user_data = c.fetchone()
    conn.close()
    return user_data is not None

def get_last_logged_in_users(limit=5):
    if os.path.exists(LOGGED_IN_USERS_FILE):
        with open(LOGGED_IN_USERS_FILE, "r") as file:
            return [line.strip() for line in file.readlines()[-limit:]]
    return []

def save_last_logged_in_user(username):
    with open(LOGGED_IN_USERS_FILE, "a") as file:
        file.write(f"{username}\n")

def on_login_clicked():
    username = entry_username.get()
    password = entry_password.get()

    if login(username, password):
        messagebox.showinfo("Erfolgreich eingeloggt", "Erfolgreich eingeloggt!")
        save_last_logged_in_user(username)
        open_user_window(username)
    else:
        messagebox.showerror("Fehler", "Ungültiger Benutzername oder Passwort.")

def on_create_account_clicked():
    username = entry_username.get()
    password = entry_password.get()

    if username and password:
        create_account(username, password)
        messagebox.showinfo("Erfolgreich registriert", "Benutzerkonto erfolgreich erstellt!")
        open_user_window(username)
    else:
        messagebox.showerror("Fehler", "Benutzername und Passwort müssen ausgefüllt sein.")

def open_user_window(username):
    root.withdraw()  # Schließe das Hauptfenster
    user_window = tk.Toplevel()
    user_window.title(f"Willkommen, {username}!")

    label_welcome = tk.Label(user_window, text=f"Willkommen, {username}!")
    label_welcome.pack()

    user_window.mainloop()

def main():
    initialize_database()

    global root
    root = tk.Tk()
    root.title("Benutzer-Login")

    label_username = tk.Label(root, text="Benutzername:")
    label_username.pack()
    entry_username = tk.Entry(root)
    entry_username.pack()

    label_password = tk.Label(root, text="Passwort:")
    label_password.pack()
    entry_password = tk.Entry(root, show="*")
    entry_password.pack()

    button_login = tk.Button(root, text="Einloggen", command=on_login_clicked)
    button_login.pack()

    button_create_account = tk.Button(root, text="Registrieren", command=on_create_account_clicked)
    button_create_account.pack()

    root.mainloop()

if __name__ == "__main__":
    main()
