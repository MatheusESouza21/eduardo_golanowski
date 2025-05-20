import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar

# Configuração do tema
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class LoginApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Sistema de Login")
        self.root.geometry("400x340")
        self.root.resizable(False, False)
        self.root.configure(fg_color="#121212")
        
        # Variável para controle de fechamento
        self.fechando = False
        
        # Frame principal
        self.frame = ctk.CTkFrame(
            self.root, 
            fg_color="#121212",
            border_color="#333333",
            border_width=1
        )
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        self.criar_interface_login()
        
        # Configurar o protocolo de fechamento
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)
        
        # Centralizar a janela
        self.centralizar_janela()
    
    def centralizar_janela(self):
        """Centraliza a janela na tela"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def fechar_janela(self):
        """Método para fechar a janela corretamente"""
        self.fechando = True
        self.root.destroy()
    
    def mostrar_tela_login(self):
        """Mostra a tela de login novamente"""
        if not self.fechando:
            self.root.deiconify()
            self.entry_usuario.delete(0, 'end')
            self.entry_senha.delete(0, 'end')
            self.entry_usuario.focus_set()
    
    def criar_interface_login(self):
        # Título
        label_titulo = ctk.CTkLabel(
            self.frame, 
            text="Login", 
            font=("Roboto", 24, "bold"),
            text_color="#FFFFFF"
        )
        label_titulo.pack(pady=(10, 30))
        
        # Campo de usuário
        ctk.CTkLabel(
            self.frame, 
            text="Usuário", 
            font=("Roboto", 12),
            text_color="#CCCCCC"
        ).pack()
        
        self.entry_usuario = ctk.CTkEntry(
            self.frame, 
            width=200,
            fg_color="#333333",
            border_color="#555555",
            text_color="#FFFFFF",
            placeholder_text="Digite seu usuário",
            placeholder_text_color="#888888"
        )
        self.entry_usuario.pack(pady=5)
        self.entry_usuario.bind("<Return>", lambda e: self.entry_senha.focus_set())
        
        # Campo de senha
        ctk.CTkLabel(
            self.frame, 
            text="Senha", 
            font=("Roboto", 12),
            text_color="#CCCCCC"
        ).pack()
        
        self.entry_senha = ctk.CTkEntry(
            self.frame, 
            width=200, 
            show="*",
            fg_color="#333333",
            border_color="#555555",
            text_color="#FFFFFF",
            placeholder_text="Digite sua senha",
            placeholder_text_color="#888888"
        )
        self.entry_senha.pack(pady=5)
        self.entry_senha.bind("<Return>", lambda e: self.verificar_login())
        
        # Botão de login
        login_btn = ctk.CTkButton(
            self.frame,
            text="Entrar",
            command=self.verificar_login,
            width=200,
            height=40,
            font=("Roboto", 14, "bold"),
            fg_color="#1E90FF",
            hover_color="#187BCD",
            text_color="#FFFFFF",
            corner_radius=8
        )
        login_btn.pack(pady=20)
        
        # Versão do sistema
        ctk.CTkLabel(
            self.frame,
            text="v1.0.0",
            text_color="#555555",
            font=("Roboto", 10)
        ).pack(side="bottom", pady=10)
    
    def verificar_login(self):
        if self.fechando:
            return
            
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
    
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        conn = conectar()
        cursor = conn.cursor()
    
        try:
            cursor.execute("SELECT id_usuario, tipo FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
            resultado = cursor.fetchone()
        
            if resultado:
                id_usuario = resultado[0]
                tipo = resultado[1]
                self.root.withdraw()  # Esconde a janela de login
                
                # Importação dinâmica para evitar importação circular
                if tipo == "comum":
                    from compra import abrir_tela_compra
                    abrir_tela_compra(id_usuario, self.mostrar_tela_login)
                elif tipo == "administrador":
                    from admin_crud import abrir_menu_admin
                    abrir_menu_admin(self.mostrar_tela_login)
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos")
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {str(e)}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = LoginApp()
    app.root.mainloop()