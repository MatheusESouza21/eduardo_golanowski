import tkinter as tk
from db_config import conectar

def abrir():
    janela = tk.Toplevel()
    janela.title("CRUD - Usuário")

    def listar():
        lista.delete(0, tk.END)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuario")
        for linha in cursor.fetchall():
            lista.insert(tk.END, linha)
        conn.close()

    def inserir():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO usuario (nome, senha, status) VALUES (%s, %s, %s)",
                       (entry_nome.get(), entry_senha.get(), entry_status.get()))
        conn.commit()
        conn.close()
        listar()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Senha").pack()
    entry_senha = tk.Entry(janela)
    entry_senha.pack()

    tk.Label(janela, text="Status").pack()
    entry_status = tk.Entry(janela)
    entry_status.pack()

    tk.Button(janela, text="Inserir", command=inserir).pack()
    lista = tk.Listbox(janela, width=50)
    lista.pack()

    listar()
