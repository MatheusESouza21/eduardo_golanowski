import customtkinter as ctk
from tkinter import ttk
from crud_usuario import abrir as abrir_crud_usuario
from crud_fornecedor import abrir as abrir_crud_fornecedor
from crud_produto import abrir as abrir_crud_produto
from crud_funcionario import abrir as abrir_crud_funcionario

class AdminMenu:
    def __init__(self, login_callback=None):
        # Configuração da janela principal
        self.janela = ctk.CTk()
        self.janela.title("Painel Administrativo")
        self.janela.geometry("600x500")
        self.janela.resizable(False, False)
        
        # Callback para retornar à tela de login
        self.login_callback = login_callback
        
        # Configurar tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variável para controlar se a janela está sendo fechada
        self.fechando = False
        self.callbacks = []  # Armazenar callbacks "after"
        
        # Frame superior para o botão de logout
        self.top_frame = ctk.CTkFrame(self.janela, fg_color="transparent", height=40)
        self.top_frame.pack(fill="x", padx=10, pady=5)
        self.top_frame.pack_propagate(False)
        
        # Botão de logout no canto superior direito
        self.logout_btn = ctk.CTkButton(
            self.top_frame,
            text="🔒 Logout",
            command=self.fazer_logout,
            width=100,
            height=30,
            fg_color="transparent",
            border_width=1,
            border_color="#dc3545",
            text_color="#dc3545",
            hover_color="#495057",
            font=("Arial", 12)
        )
        self.logout_btn.pack(side="right", padx=5)
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.main_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        self.criar_interface()
        
        # Configurar protocolo de fechamento
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
        # Variável para controlar subjanelas
        self.subjanelas = []
    
    def fazer_logout(self):
        """Método para fazer logout e voltar para tela de login"""
        if self.fechando:
            return
            
        self.fechando = True
        
        # Cancelar todos os callbacks "after"
        for callback in self.callbacks:
            self.janela.after_cancel(callback)
        
        # Fechar todas as subjanelas primeiro
        for janela in self.subjanelas:
            try:
                janela.destroy()
            except:
                pass
        
        # Fechar a janela atual
        self.janela.destroy()
        
        # Chamar o callback para voltar à tela de login, se existir
        if self.login_callback:
            self.login_callback()
    
    def fechar_janela(self):
        """Método para fechar a janela corretamente"""
        self.fazer_logout()
    
    def registrar_subjanela(self, janela):
        """Registra uma subjanela para fechar corretamente no logout"""
        self.subjanelas.append(janela)
    
    def criar_interface(self):
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Painel Administrativo", 
            font=("Arial", 22, "bold")
        ).pack(pady=(0, 30))
        
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
        
        # Botão de sair
        ctk.CTkButton(
            self.main_frame,
            text="🚪 Sair do Sistema",
            command=self.fazer_logout,
            fg_color="transparent",
            border_width=2,
            border_color="#dc3545",
            text_color="#dc3545",
            height=45,
            font=("Arial", 14),
            corner_radius=8,
            hover_color="#f8f9fa"
        ).pack(pady=(20, 10), padx=40, fill="x")
    
    def escurecer_cor(self, cor_hex, fator=0.8):
        """Escurece uma cor HEX para o efeito hover"""
        rgb = tuple(int(cor_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        escuro = tuple(int(c * fator) for c in rgb)
        return f"#{escuro[0]:02x}{escuro[1]:02x}{escuro[2]:02x}"
    
    def abrir_dashboard(self):
        if not self.fechando:
            self.janela.withdraw()
            from dashboard import DashboardApp
            dashboard = DashboardApp(self)
            self.registrar_subjanela(dashboard.root)
            dashboard.root.mainloop()
    
    def abrir_crud_usuario(self):
        if not self.fechando:
            # Desabilita o botão temporariamente para evitar múltiplos cliques
            self.janela.update_idletasks()
        
            # Cria a janela CRUD de usuário
            janela_crud = abrir_crud_usuario(self, self.login_callback)
        
            # Configura o comportamento ao fechar a janela CRUD
            def on_crud_close():
                if self.janela.winfo_exists():
                    self.janela.deiconify()
                if janela_crud.winfo_exists():
                    janela_crud.destroy()
        
            janela_crud.protocol("WM_DELETE_WINDOW", on_crud_close)
        
            # Esconde a janela principal somente após a CRUD estar pronta
            self.janela.withdraw()
        
            # Mantém referência à janela CRUD
            self.registrar_subjanela(janela_crud)
        
            # Força o foco na nova janela
            janela_crud.focus_force()
            janela_crud.grab_set()

    def abrir_crud_fornecedor(self):
        if not self.fechando:
            self.janela.withdraw()
            janela_crud = abrir_crud_fornecedor(self, self.login_callback)
            self.registrar_subjanela(janela_crud)
    
    def abrir_crud_produto(self):
        if not self.fechando:
            self.janela.withdraw()
            janela_crud = abrir_crud_produto(self, self.login_callback)
            self.registrar_subjanela(janela_crud)
    
    def abrir_crud_funcionario(self):
        if not self.fechando:
            self.janela.withdraw()
            janela_crud = abrir_crud_funcionario(self, self.login_callback)
            self.registrar_subjanela(janela_crud)

def abrir_menu_admin(login_callback=None):
    app = AdminMenu(login_callback)
    app.janela.mainloop()