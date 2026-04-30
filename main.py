import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import json
import os

# Константы
HISTORY_FILE = "password_history.json"
MIN_LENGTH = 4
MAX_LENGTH = 32

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def generate_password():
    length = length_var.get()
    use_digits = digits_var.get()
    use_letters = letters_var.get()
    use_special = special_var.get()

    if length < MIN_LENGTH or length > MAX_LENGTH:
        messagebox.showerror("Ошибка", f"Длина пароля должна быть от {MIN_LENGTH} до {MAX_LENGTH}")
        return

    if not (use_digits or use_letters or use_special):
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов")
        return

    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special:
        chars += string.punctuation

    password = ''.join(random.choices(chars, k=length))

    # Добавление в историю
    history = load_history()
    history.insert(0, {"password": password, "length": length})
    save_history(history)

    # Обновление таблицы
    update_history_table()

    # Вывод пароля
    password_label.config(text=password)

def update_history_table():
    for i in history_treeview.get_children():
        history_treeview.delete(i)

    history = load_history()
    for item in history:
        history_treeview.insert("", "end", values=(item["password"], item["length"]))

# Создание окна
root = tk.Tk()
root.title("Random Password Generator")
root.geometry("600x500")
root.resizable(False, False)

# Переменные
length_var = tk.IntVar(value=12)
digits_var = tk.BooleanVar(value=True)
letters_var = tk.BooleanVar(value=True)
special_var = tk.BooleanVar(value=True)

# Интерфейс
tk.Label(root, text="Длина пароля:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
length_slider = tk.Scale(root, from_=MIN_LENGTH, to=MAX_LENGTH, orient=tk.HORIZONTAL,
                         variable=length_var, length=200)
length_slider.grid(row=0, column=1, columnspan=2, padx=10, pady=10)

tk.Checkbutton(root, text="Цифры", variable=digits_var).grid(row=1, column=1, sticky="w")
tk.Checkbutton(root, text="Буквы", variable=letters_var).grid(row=2, column=1, sticky="w")
tk.Checkbutton(root, text="Спецсимволы", variable=special_var).grid(row=3, column=1, sticky="w")

generate_btn = tk.Button(root, text="Сгенерировать пароль", command=generate_password)
generate_btn.grid(row=4, column=0, columnspan=3, pady=20)

password_label = tk.Label(root, text="", font=('Courier New', 14), width=40)
password_label.grid(row=5, column=0, columnspan=3, pady=10)

# Таблица истории
history_treeview = ttk.Treeview(root, columns=("Пароль", "Длина"), show="headings")
history_treeview.heading("Пароль", text="Пароль")
history_treeview.heading("Длина", text="Длина")
history_treeview.column("Пароль", width=350)
history_treeview.column("Длина", width=50)
history_treeview.grid(row=6, column=0, columnspan=3, pady=10)

update_history_table()

root.mainloop()
