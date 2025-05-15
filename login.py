import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar

# Configuração do tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Login")
        self.geometry("400x340")  # Tamanho reduzido
        self.resizable(False, False)
        
        # Frame principal
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Elementos da interface
        self.criar_interface_login()

    def criar_interface_login(self):
        # Título
        label_titulo = ctk.CTkLabel(self.frame, text="Login", font=("Roboto", 24))
        label_titulo.pack(pady=20)
        
        # Campo de usuário
        ctk.CTkLabel(self.frame, text="Usuário", font=("Roboto", 12)).pack()
        self.entry_usuario = ctk.CTkEntry(self.frame, width=200)
        self.entry_usuario.pack(pady=5)
        
        # Campo de senha
        ctk.CTkLabel(self.frame, text="Senha", font=("Roboto", 12)).pack()
        self.entry_senha = ctk.CTkEntry(self.frame, width=200, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botão de login
        ctk.CTkButton(self.frame, text="Entrar", command=self.verificar_login).pack(pady=20)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT tipo FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
            resultado = cursor.fetchone()
            
            if resultado:
                tipo = resultado[0]
                self.destroy()  # Fecha a janela de login
                
                if tipo == "comum":
                    from compra import abrir_tela_compra
                    abrir_tela_compra()
                elif tipo == "administrador":
                    from admin_crud import abrir_menu_admin
                    abrir_menu_admin()
            else:
                messagebox.showerror("Erro", "Usuário ou senha inválidos")
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha na conexão: {str(e)}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()
