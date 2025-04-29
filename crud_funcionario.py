import tkinter as tk
from db_config import conectar

def abrir():
    janela = tk.Toplevel()
    janela.title("CRUD - Funcionário")

    def listar():
        lista.delete(0, tk.END)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM funcionario")
        for linha in cursor.fetchall():
            lista.insert(tk.END, linha)
        conn.close()

    def inserir():
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO funcionario (nome, cargo, cpf, salario)
            VALUES (%s, %s, %s, %s)
        """, (
            entry_nome.get(),
            entry_cargo.get(),
            entry_cpf.get(),
            float(entry_salario.get())
        ))
        conn.commit()
        conn.close()
        listar()

    tk.Label(janela, text="Nome").pack()
    entry_nome = tk.Entry(janela)
    entry_nome.pack()

    tk.Label(janela, text="Cargo").pack()
    entry_cargo = tk.Entry(janela)
    entry_cargo.pack()

    tk.Label(janela, text="CPF").pack()
    entry_cpf = tk.Entry(janela)
    entry_cpf.pack()

    tk.Label(janela, text="Salário").pack()
    entry_salario = tk.Entry(janela)
    entry_salario.pack()

    tk.Button(janela, text="Inserir", command=inserir).pack()
    lista = tk.Listbox(janela, width=80)
    lista.pack()

    listar()
