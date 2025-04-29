import tkinter as tk
from db_config import conectar

def abrir():
    janela = tk.Toplevel()
    janela.title("CRUD - Fornecedor")

    def listar():
        lista.delete(0, tk.END)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM fornecedor")
        for linha in cursor.fetchall():
            lista.insert(tk.END, linha)
        conn.close()

    def inserir():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO fornecedor (nome, cnpj, telefone, endereco)
            VALUES (%s, %s, %s, %s)
        """, (entry_nome.get(), entry_cnpj.get(), entry_telefone.get(), entry_endereco.get()))
        conn.commit()
        conn.close()
        listar()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="CNPJ").pack()
    entry_cnpj = tk.Entry(janela)
    entry_cnpj.pack()

    tk.Label(janela, text="Telefone").pack()
    entry_telefone = tk.Entry(janela)
    entry_telefone.pack()

    tk.Label(janela, text="Endereço").pack()
    entry_endereco = tk.Entry(janela)
    entry_endereco.pack()

    tk.Button(janela, text="Inserir", command=inserir).pack()
    lista = tk.Listbox(janela, width=80)
    lista.pack()

    listar()
