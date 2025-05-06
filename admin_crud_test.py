import customtkinter as ctk
from tkinter import messagebox
from crud_usuario import UsuarioCRUD
from crud_produto import ProdutoCRUD
from crud_funcionario import FuncionarioCRUD

class AdminMenu:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Menu Administrativo")
        self.janela.geometry("600x400")
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        main_frame = ctk.CTkFrame(self.janela)
        main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(
            main_frame, 
            text="Menu Administrativo", 
            font=("Roboto", 24)
        ).pack(pady=20)
        
        # Botões de opções
        botoes = [
            ("Gerenciar Usuários", self.abrir_usuarios),
            ("Gerenciar Produtos", self.abrir_produtos),
            ("Gerenciar Funcionários", self.abrir_funcionarios),
            ("Sair", self.janela.destroy)
        ]
        
        for texto, comando in botoes:
            ctk.CTkButton(
                main_frame,
                text=texto,
                command=comando,
                height=40,
                font=("Roboto", 14)
            ).pack(pady=10, fill="x", padx=50)
    
    def abrir_usuarios(self):
        usuario_crud = UsuarioCRUD()
        usuario_crud.janela.mainloop()
    
    def abrir_produtos(self):
        produto_crud = ProdutoCRUD()
        produto_crud.janela.mainloop()
    
    def abrir_funcionarios(self):
        funcionario_crud = FuncionarioCRUD()
        funcionario_crud.janela.mainloop()

def abrir_menu_admin():
    app = AdminMenu()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir_menu_admin()