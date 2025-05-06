import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar
# No início do arquivo, adicione os imports:
from admin_crud import abrir_menu_admin
from compra import abrir_tela_compra

# Configuração do tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Login")
        self.geometry("600x400")
        self.resizable(False, False)
        
        # Container principal
        self.container = ctk.CTkFrame(self)
        self.container.pack(fill="both", expand=True)
        
        # Dicionário para armazenar as telas
        self.telas = {}
        
        # Criar todas as telas
        self.criar_tela_login()
        self.criar_tela_cadastro()
        
        # Mostrar a tela inicial
        self.mostrar_tela("login")

    def criar_tela_login(self):
        frame = ctk.CTkFrame(self.container)
        self.telas["login"] = frame
        
        label_titulo = ctk.CTkLabel(frame, text="Login", font=("Roboto", 24))
        label_titulo.pack(pady=20)
        
        # Campo de usuário
        ctk.CTkLabel(frame, text="Usuário", font=("Roboto", 12)).pack()
        self.entry_usuario = ctk.CTkEntry(frame, width=200)
        self.entry_usuario.pack(pady=5)
        
        # Campo de senha
        ctk.CTkLabel(frame, text="Senha", font=("Roboto", 12)).pack()
        self.entry_senha = ctk.CTkEntry(frame, width=200, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botão de login
        ctk.CTkButton(frame, text="Entrar", command=self.verificar_login).pack(pady=15)
        
        # Botão para cadastro
        ctk.CTkButton(frame, text="Criar Nova Conta", command=lambda: self.mostrar_tela("cadastro"),
                     fg_color="transparent", border_width=1).pack(pady=5)

    def criar_tela_cadastro(self):
        frame = ctk.CTkFrame(self.container)
        self.telas["cadastro"] = frame
        
        label_titulo = ctk.CTkLabel(frame, text="Criar Nova Conta", font=("Roboto", 24))
        label_titulo.pack(pady=20)
        
        # Campos do formulário
        ctk.CTkLabel(frame, text="Novo Usuário").pack()
        self.novo_usuario = ctk.CTkEntry(frame, width=200)
        self.novo_usuario.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Senha").pack()
        self.nova_senha = ctk.CTkEntry(frame, width=200, show="*")
        self.nova_senha.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Confirmar Senha").pack()
        self.confirmar_senha = ctk.CTkEntry(frame, width=200, show="*")
        self.confirmar_senha.pack(pady=5)
        
        # Botões
        ctk.CTkButton(frame, text="Criar Conta", command=self.criar_usuario).pack(pady=15)
        ctk.CTkButton(frame, text="Voltar", command=lambda: self.mostrar_tela("login"),
                     fg_color="transparent", border_width=1).pack(pady=5)

    def mostrar_tela(self, nome_tela):
        # Esconde todas as telas
        for tela in self.telas.values():
            tela.pack_forget()
        
        # Mostra a tela solicitada
        self.telas[nome_tela].pack(fill="both", expand=True)

    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
        
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT tipo FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()
        
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

    def criar_usuario(self):
        if self.nova_senha.get() != self.confirmar_senha.get():
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
            
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuario (nome, senha, tipo) VALUES (%s, %s, %s)", 
                         (self.novo_usuario.get(), self.nova_senha.get(), "comum"))
            conn.commit()
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            self.mostrar_tela("login")
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível criar usuário: {str(e)}")
        finally:
            conn.close()


    def verificar_login(self):
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
    
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT tipo FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
        resultado = cursor.fetchone()
        conn.close()
    
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

if __name__ == "__main__":
    app = App()
    app.mainloop()