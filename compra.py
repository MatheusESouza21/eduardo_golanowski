import tkinter as tk
from db_config import conectar

def abrir_tela_compra():
    janela = tk.Tk()
    janela.title("Tela de Compras")

    tk.Label(janela, text="Produtos disponíveis:").pack()

    lista = tk.Listbox(janela, width=80)
    lista.pack()

    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT nome, descricao, preco FROM produto WHERE quantidade > 0")
    for nome, desc, preco in cursor.fetchall():
        lista.insert(tk.END, f"{nome} - {desc} - R$ {preco:.2f}")

    conn.close()

    janela.mainloop()
