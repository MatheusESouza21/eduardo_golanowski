import customtkinter as ctk
import crud_usuario
import crud_fornecedor
import crud_produto
import crud_funcionario

class AdminMenu:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ctk.CTk()
        self.janela.title("Painel Administrativo")
        self.janela.geometry("500x450")
        self.janela.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.criar_interface()
    
    def criar_interface(self):
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Menu Administrativo", 
            font=("Arial", 20, "bold")
        ).pack(pady=(10, 20))
        
        # Frame dos botões
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20)
        
        # Botões de CRUD
        botoes = [
            ("👥 Usuários", self.abrir_crud_usuario),
            ("🏢 Fornecedores", self.abrir_crud_fornecedor),
            ("📦 Produtos", self.abrir_crud_produto),
            ("👨‍💼 Funcionários", self.abrir_crud_funcionario)
        ]
        
        for texto, comando in botoes:
            btn = ctk.CTkButton(
                btn_frame,
                text=texto,
                command=comando,
                height=40,
                font=("Arial", 14),
                corner_radius=8
            )
            btn.pack(pady=8, fill="x")
        
        # Botão de sair
        ctk.CTkButton(
            self.main_frame,
            text="🚪 Sair",
            command=self.janela.destroy,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            height=40,
            font=("Arial", 14),
            corner_radius=8
        ).pack(pady=(20, 10), padx=20, fill="x")
    
    def abrir_crud_usuario(self):
        self.janela.withdraw()  # Esconde a janela atual
        crud_usuario.abrir(self.janela)  # Passa a referência da janela principal
    
    def abrir_crud_fornecedor(self):
        self.janela.withdraw()
        crud_fornecedor.abrir(self.janela)
    
    def abrir_crud_produto(self):
        self.janela.withdraw()
        crud_produto.abrir(self.janela)
    
    def abrir_crud_funcionario(self):
        self.janela.withdraw()
        crud_funcionario.abrir(self.janela)

def abrir_menu_admin():
    app = AdminMenu()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir_menu_admin()