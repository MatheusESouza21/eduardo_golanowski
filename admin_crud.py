import customtkinter as ctk
from tkinter import messagebox
from crud_usuario import abrir as abrir_crud_usuario
from crud_fornecedor import abrir as abrir_crud_fornecedor
from crud_produto import abrir as abrir_crud_produto
from crud_funcionario import abrir as abrir_crud_funcionario

class AdminMenu:
    def __init__(self):
        # Configuração da janela principal
        self.janela = ctk.CTk()
        self.janela.title("Painel Administrativo")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variável para controlar se a janela está sendo fechada
        self.fechando = False
        self.after_ids = []  # Armazenar IDs dos callbacks "after"
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.criar_interface()
        
        # Configurar protocolo de fechamento
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
    
    def fechar_janela(self):
        """Método para fechar a janela corretamente"""
        self.fechando = True
        # Cancelar todos os callbacks "after"
        for after_id in self.after_ids:
            self.janela.after_cancel(after_id)
        self.janela.destroy()
    
    def logout(self):
        """Método para fazer logout e voltar para a tela de login"""
        if messagebox.askyesno("Logout", "Deseja realmente sair do sistema?"):
            self.fechar_janela()
            from login import App  # Importar aqui para evitar importação circular
            login_app = App()
            login_app.mainloop()
    
    def criar_interface(self):
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Painel Administrativo", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 20))
        
        # Frame dos botões
        btn_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        btn_frame.pack(fill="x", padx=40)
        
        # Configuração dos botões
        botoes = [
            {
                "texto": "📊 Dashboard",
                "comando": self.abrir_dashboard,
                "cor": "#007bff"
            },
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
        
        for btn_info in botoes:
            btn = ctk.CTkButton(
                btn_frame,
                text=btn_info["texto"],
                command=btn_info["comando"],
                height=45,
                font=("Arial", 14, "bold"),
                corner_radius=8,
                fg_color=btn_info["cor"],
                hover_color=self.escurecer_cor(btn_info["cor"])
            )
            btn.pack(pady=10, fill="x")
        
        # Frame para botões de saída
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
        
        # Botão de sair
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
        """Escurece uma cor HEX para o efeito hover"""
        rgb = tuple(int(cor_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        escuro = tuple(int(c * fator) for c in rgb)
        return f"#{escuro[0]:02x}{escuro[1]:02x}{escuro[2]:02x}"
    
    def abrir_dashboard(self):
        if not self.fechando:
            self.janela.withdraw()
            from dashboard import DashboardApp
            dashboard_app = DashboardApp()
            # Registrar callbacks "after" para cancelar quando fechar
            if hasattr(dashboard_app, 'after_ids'):
                self.after_ids.extend(dashboard_app.after_ids)
            dashboard_app.root.protocol("WM_DELETE_WINDOW", lambda: self.on_child_close(dashboard_app))
            dashboard_app.root.mainloop()

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
        """Função chamada quando uma janela filha é fechada"""
        if hasattr(child_window, 'fechando'):
            child_window.fechando = True
        if hasattr(child_window, 'after_ids'):
            for after_id in child_window.after_ids:
                child_window.root.after_cancel(after_id)
        child_window.root.destroy()
        self.janela.deiconify()  # Mostra o menu admin novamente

def abrir_menu_admin():
    app = AdminMenu()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir_menu_admin()