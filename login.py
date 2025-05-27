# Importação das bibliotecas necessárias
import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar

# Configuração inicial do tema do CustomTkinter
ctk.set_appearance_mode("System")  # Usa o tema do sistema (claro/escuro)
ctk.set_default_color_theme("blue")  # Define o tema de cor azul

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configurações da janela principal
        self.title("Sistema de Login")
        self.geometry("400x340")
        self.resizable(False, False)  # Impede redimensionamento
        
        # Define novamente tema escuro e azul (redundante, mas reforçado)
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Variável de controle para saber se a janela está sendo fechada
        self.fechando = False
        
        # Cria o frame principal que conterá os widgets
        self.frame = ctk.CTkFrame(self)
        self.frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Chama método para criar os elementos da interface de login
        self.criar_interface_login()
        
        # Define o protocolo para capturar o evento de fechar a janela
        self.protocol("WM_DELETE_WINDOW", self.fechar_janela)

    def fechar_janela(self):
        """Método que garante o fechamento correto da janela"""
        self.fechando = True  # Marca que estamos fechando
        self.destroy()        # Fecha a janela

    def criar_interface_login(self):
        """Cria os elementos visuais da tela de login"""
        
        # Título da tela
        label_titulo = ctk.CTkLabel(self.frame, text="Login", font=("Roboto", 24))
        label_titulo.pack(pady=20)
        
        # Label e campo para o nome de usuário
        ctk.CTkLabel(self.frame, text="Usuário", font=("Roboto", 12)).pack()
        self.entry_usuario = ctk.CTkEntry(self.frame, width=200)
        self.entry_usuario.pack(pady=5)
        
        # Label e campo para a senha (com máscara de asteriscos)
        ctk.CTkLabel(self.frame, text="Senha", font=("Roboto", 12)).pack()
        self.entry_senha = ctk.CTkEntry(self.frame, width=200, show="*")
        self.entry_senha.pack(pady=5)
        
        # Botão que chama a verificação de login
        ctk.CTkButton(self.frame, text="Entrar", command=self.verificar_login).pack(pady=20)

    def verificar_login(self):
        """Verifica as credenciais inseridas pelo usuário"""
        
        if self.fechando:
            # Se a janela já está em processo de fechamento, não faz nada
            return
            
        # Recupera os valores digitados nos campos
        usuario = self.entry_usuario.get()
        senha = self.entry_senha.get()
    
        # Verifica se todos os campos foram preenchidos
        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return
            
        # Conecta ao banco de dados usando a função definida no arquivo db_config
        conn = conectar()
        cursor = conn.cursor()
    
        try:
            # Consulta no banco pelo usuário e senha fornecidos
            cursor.execute(
                "SELECT id_usuario, tipo FROM usuario WHERE nome = %s AND senha = %s",
                (usuario, senha)
            )
            resultado = cursor.fetchone()
        
            if resultado:
                # Se encontrou um usuário válido, recupera ID e tipo
                id_usuario = resultado[0]
                tipo = resultado[1]
                
                # Fecha a janela de login
                self.fechando = True
                self.destroy()
            
                # Redireciona para a tela apropriada conforme o tipo do usuário
                if tipo == "comum":
                    from compra import abrir_tela_compra
                    abrir_tela_compra(id_usuario)
                elif tipo == "administrador":
                    from admin_crud import abrir_menu_admin
                    abrir_menu_admin()
            else:
                # Se não encontrou, exibe mensagem de erro
                messagebox.showerror("Erro", "Usuário ou senha inválidos")
            
        except Exception as e:
            # Em caso de erro no banco, exibe mensagem de falha
            messagebox.showerror("Erro", f"Falha na conexão: {str(e)}")
        finally:
            # Fecha a conexão com o banco, se aberta
            if conn:
                conn.close()

# Ponto de entrada principal do programa
if __name__ == "__main__":
    app = App()
    app.mainloop()
