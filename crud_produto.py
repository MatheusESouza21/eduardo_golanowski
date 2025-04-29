import tkinter as tk
from db_config import conectar

def abrir():
    janela = tk.Toplevel()
    janela.title("CRUD - Produto")

    def listar():
        lista.delete(0, tk.END)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM produto")
        for linha in cursor.fetchall():
            lista.insert(tk.END, linha)
        conn.close()

    def inserir():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO produto (nome, descricao, quantidade, preco, id_fornecedor)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            entry_nome.get(),
            entry_descricao.get(),
            int(entry_quantidade.get()),
            float(entry_preco.get()),
            int(entry_id_fornecedor.get())
        ))
        conn.commit()
        conn.close()
        listar()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Descrição").pack()
    entry_descricao = tk.Entry(janela)
    entry_descricao.pack()

    tk.Label(janela, text="Quantidade").pack()
    entry_quantidade = tk.Entry(janela)
    entry_quantidade.pack()

    tk.Label(janela, text="Preço").pack()
    entry_preco = tk.Entry(janela)
    entry_preco.pack()

    tk.Label(janela, text="ID Fornecedor").pack()
    entry_id_fornecedor = tk.Entry(janela)
    entry_id_fornecedor.pack()

    tk.Button(janela, text="Inserir", command=inserir).pack()
    lista = tk.Listbox(janela, width=100)
    lista.pack()

    listar()
