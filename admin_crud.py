# Importação das bibliotecas necessárias
import customtkinter as ctk
from tkinter import messagebox

# Importação dos módulos CRUD (cada um com sua função abrir)
from crud_usuario import abrir as abrir_crud_usuario
from crud_fornecedor import abrir as abrir_crud_fornecedor
from crud_produto import abrir as abrir_crud_produto
from crud_funcionario import abrir as abrir_crud_funcionario

class AdminMenu:
    def __init__(self):
        # Criação da janela principal do painel administrativo
        self.janela = ctk.CTk()
        self.janela.title("Painel Administrativo")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)  # Impede redimensionamento
        
        # Configuração do tema visual
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variáveis de controle
        self.fechando = False            # Marca se a janela está sendo fechada
        self.after_ids = []             # Lista para armazenar IDs de callbacks 'after'
        
        # Frame principal que conterá todos os widgets
        self.main_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Chama o método para criar a interface visual
        self.criar_interface()
        
        # Configura o protocolo de fechamento da janela
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
    
    def fechar_janela(self):
        """Método para fechar a janela corretamente"""
        self.fechando = True
        
        # Cancela todos os callbacks pendentes para evitar erros
        for after_id in self.after_ids:
            self.janela.after_cancel(after_id)
        
        # Fecha a janela
        self.janela.destroy()
    
    def logout(self):
        """Método para realizar logout e voltar à tela de login"""
        if messagebox.askyesno("Logout", "Deseja realmente sair do sistema?"):
            self.fechar_janela()
            
            # Importação feita aqui para evitar importação circular
            from login import App
            login_app = App()
            login_app.mainloop()
    
    def criar_interface(self):
        """Método que monta os elementos visuais da tela"""
        
        # Título do painel
        ctk.CTkLabel(
            self.main_frame, 
            text="Painel Administrativo", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 20))
        
        # Frame para os botões principais (CRUD)
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40)
        
        # Lista de botões com textos, comandos e cores
        botoes = [
            {
                "texto": "👥 Gerenciar Usuários",
                "comando": self.abrir_crud_usuario,
                "cor": "#2aa745"
            },
            {
                "texto": "🏢 Gerenciar Fornecedores",
                "comando": self.abrir_crud_fornecedor,
                "cor": "#17a2b8"
            },
            {
                "texto": "📦 Gerenciar Produtos",
                "comando": self.abrir_crud_produto,
                "cor": "#6f42c1"
            },
            {
                "texto": "👨‍💼 Gerenciar Funcionários",
                "comando": self.abrir_crud_funcionario,
                "cor": "#fd7e14"
            }
        ]
        
        # Criação e empacotamento dos botões CRUD
        for btn_info in botoes:
            btn = ctk.CTkButton(
                btn_frame,
                text=btn_info["texto"],
                command=btn_info["comando"],
                height=45,
                font=("Arial", 14, "bold"),
                corner_radius=8,
                fg_color=btn_info["cor"],
                hover_color=self.escurecer_cor(btn_info["cor"])  # Cor ao passar o mouse
            )
            btn.pack(pady=10, fill="x")
        
        # Frame para os botões de saída (logout e fechar)
        exit_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        exit_frame.pack(pady=(10, 0), padx=40, fill="x")
        
        # Botão de logout
        ctk.CTkButton(
            exit_frame,
            text="🔒 Logout",
            command=self.logout,
            fg_color="transparent",
            border_width=2,
            border_color="#6c757d",
            text_color="#6c757d",
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            hover_color="#f8f9fa"
        ).pack(side="left", fill="x", expand=True, padx=5)
        
        # Botão de sair do sistema
        ctk.CTkButton(
            exit_frame,
            text="🚪 Sair do Sistema",
            command=self.fechar_janela,
            fg_color="transparent",
            border_width=2,
            border_color="#dc3545",
            text_color="#dc3545",
            height=40,
            font=("Arial", 14),
            corner_radius=8,
            hover_color="#f8f9fa"
        ).pack(side="right", fill="x", expand=True, padx=5)
    
    def escurecer_cor(self, cor_hex, fator=0.8):
        """Escurece uma cor HEX aplicando um fator (para efeito hover)"""
        rgb = tuple(int(cor_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        escuro = tuple(int(c * fator) for c in rgb)
        return f"#{escuro[0]:02x}{escuro[1]:02x}{escuro[2]:02x}"
    
    # Métodos para abrir cada módulo CRUD (e esconder o menu enquanto isso)
    def abrir_crud_usuario(self):
        if not self.fechando:
            self.janela.withdraw()
            abrir_crud_usuario(self)
    
    def abrir_crud_fornecedor(self):
        if not self.fechando:
            self.janela.withdraw()
            abrir_crud_fornecedor(self)
    
    def abrir_crud_produto(self):
        if not self.fechando:
            self.janela.withdraw()
            abrir_crud_produto(self)
    
    def abrir_crud_funcionario(self):
        if not self.fechando:
            self.janela.withdraw()
            abrir_crud_funcionario(self)
    
    def on_child_close(self, child_window):
        """Método chamado quando uma janela filha é fechada"""
        if hasattr(child_window, 'fechando'):
            child_window.fechando = True
        
        if hasattr(child_window, 'after_ids'):
            for after_id in child_window.after_ids:
                child_window.root.after_cancel(after_id)
        
        # Fecha a janela filha e reexibe o menu admin
        child_window.root.destroy()
        self.janela.deiconify()

def abrir_menu_admin():
    """Função para iniciar o menu administrativo"""
    app = AdminMenu()
    app.janela.mainloop()

# Ponto de entrada principal
if __name__ == "__main__":
    abrir_menu_admin()
