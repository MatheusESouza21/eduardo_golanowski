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
        self.geometry("400x400")
        self.resizable(False, False)
        
        # Container principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Elementos da interface
        self.criar_interface_login()

    def criar_interface_login(self):
        label_titulo = ctk.CTkLabel(self.container, text="Login", font=("Roboto", 24))
        label_titulo.pack(pady=20)
        
        # Campo de usuário
        ctk.CTkLabel(self.container, text="Usuário", font=("Roboto", 12)).pack()
        self.entry_usuario = ctk.CTkEntry(self.container, width=200)
        self.entry_usuario.pack(pady=5)
        
        # Campo de senha
        ctk.CTkLabel(self.container, text="Senha", font=("Roboto", 12)).pack()
        self.entry_senha = ctk.CTkEntry(self.container, width=200, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botão de login
        ctk.CTkButton(self.container, text="Entrar", command=self.verificar_login).pack(pady=20)

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
            messagebox.showerror("Erro", f"Falha ao conectar com o banco de dados: {str(e)}")
        finally:
            conn.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()