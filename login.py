import tkinter as tk
from tkinter import messagebox
from db_config import conectar
from compra import abrir_tela_compra
from admin_crud import abrir_menu_admin

def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    status = verificar_login(usuario, senha)

    if status == "comum":
        root.destroy()
        abrir_tela_compra()
    elif status == "administrador":
        root.destroy()
        abrir_menu_admin()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos")

root = tk.Tk()
root.title("Login")

tk.Label(root, text="Usuário").pack()
entry_usuario = tk.Entry(root)
entry_usuario.pack()

tk.Label(root, text="Senha").pack()
entry_senha = tk.Entry(root, show="*")
entry_senha.pack()

tk.Button(root, text="Entrar", command=login).pack()

root.mainloop()
