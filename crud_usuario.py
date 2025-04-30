import customtkinter as ctk
from tkinter import ttk  # Importação necessária para o Treeview
from db_config import conectar
from CTkMessagebox import CTkMessagebox

class UsuarioCRUD:
    def __init__(self):
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Usuário")
        self.janela.geometry("700x600")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.criar_interface()
        self.listar_usuarios()
    
    def criar_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.pack(pady=10, padx=10, fill="x")
        
        # Título
        ctk.CTkLabel(
            self.form_frame, 
            text="Cadastro de Usuários", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Campos do formulário
        self.criar_campos_formulario()
        
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        # Botões de ação
        ctk.CTkButton(
            self.btn_frame, 
            text="Inserir", 
            command=self.inserir_usuario,
            width=100
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Limpar", 
            command=self.limpar_campos,
            fg_color="gray",
            hover_color="darkgray",
            width=100
        ).pack(side="left", padx=5)
        
        # Área de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.list_frame, 
            text="Lista de Usuários", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Treeview para exibição (usando ttk.Treeview)
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Nome", "Status"),
            show="headings",
            height=10,
            style="Custom.Treeview"  # Estilo personalizado
        )
        
        # Configurar estilo para combinar com CustomTkinter
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Custom.Treeview", 
                       background="#2b2b2b", 
                       foreground="white",
                       fieldbackground="#2b2b2b",
                       borderwidth=0)
        style.map("Custom.Treeview", background=[("selected", "#3b8ed0")])
        
        # Configurar colunas
        self.tree.heading("ID", text="ID")
        self.tree.column("ID", width=50, anchor="center")
        
        self.tree.heading("Nome", text="Nome")
        self.tree.column("Nome", width=200, anchor="w")
        
        self.tree.heading("Status", text="Status")
        self.tree.column("Status", width=100, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.list_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão de atualizar
        ctk.CTkButton(
            self.list_frame,
            text="Atualizar Lista",
            command=self.listar_usuarios
        ).pack(pady=5)
        
        # Configurar evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.carregar_dados_selecionados)
    
    # ... (restante dos métodos permanece igual ao código anterior)

def abrir():
    app = UsuarioCRUD()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()