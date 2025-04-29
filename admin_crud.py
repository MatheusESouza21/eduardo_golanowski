import tkinter as tk
import crud_usuario
import crud_fornecedor
import crud_produto
import crud_funcionario

def abrir_menu_admin():
    janela = tk.Tk()
    janela.title("Admin - Menu de CRUDs")

    tk.Button(janela, text="CRUD Usuário", command=crud_usuario.abrir).pack()
    tk.Button(janela, text="CRUD Fornecedor", command=crud_fornecedor.abrir).pack()
    tk.Button(janela, text="CRUD Produto", command=crud_produto.abrir).pack()
    tk.Button(janela, text="CRUD Funcionário", command=crud_funcionario.abrir).pack()

    janela.mainloop()
