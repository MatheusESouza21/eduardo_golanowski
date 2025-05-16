import customtkinter as ctk
from tkinter import ttk
from db_config import conectar
from CTkMessagebox import CTkMessagebox

class UsuarioCRUD:
    import customtkinter as ctk
from tkinter import ttk
from db_config import conectar
from CTkMessagebox import CTkMessagebox

class UsuarioCRUD:
    def __init__(self, admin_menu=None):
        self.admin_menu = admin_menu
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Usuário")
        self.janela.geometry("700x650")  # Aumentei a altura para acomodar o botão Voltar
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.criar_interface()
        self.listar_usuarios()
        
        # Configurar o que acontece ao fechar a janela
        self.janela.protocol("WM_DELETE_WINDOW", self.voltar_admin)
    
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
            text="Atualizar", 
            command=self.atualizar_usuario,
            width=100,
            fg_color="#ffc107",
            hover_color="#e0a800"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Excluir", 
            command=self.excluir_usuario,
            width=100,
            fg_color="#dc3545",
            hover_color="#c82333"
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
        
        # Treeview para exibição
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Nome", "Tipo"),
            show="headings",
            height=10,
            style="Custom.Treeview"
        )
        
        # Configurar estilo
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
        
        self.tree.heading("Tipo", text="Tipo")
        self.tree.column("Tipo", width=100, anchor="center")
        
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
        
        # Frame para botões inferiores
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(pady=10, fill="x")
        
        # Botão de atualizar lista
        ctk.CTkButton(
            self.bottom_frame,
            text="Atualizar Lista",
            command=self.listar_usuarios,
            width=120
        ).pack(side="left", padx=5)
        
        # Botão Voltar ao Admin
        ctk.CTkButton(
            self.bottom_frame,
            text="Voltar ao Admin",
            command=self.voltar_admin,
            fg_color="transparent",
            border_width=1,
            border_color="#6c757d",
            text_color="#6c757d",
            hover_color="#f8f9fa",
            width=120
        ).pack(side="right", padx=5)
        
        # Configurar evento de seleção
        self.tree.bind("<<TreeviewSelect>>", self.carregar_dados_selecionados)
    
    def voltar_admin(self):
        """Fecha a janela atual e reabre o menu admin"""
        self.janela.destroy()
        if self.admin_menu:
            self.admin_menu.janela.deiconify()
    
    
    def criar_campos_formulario(self):
        # Campo ID (oculto/invisível)
        self.id_usuario = ctk.StringVar()
        
        # Campo Nome
        ctk.CTkLabel(self.form_frame, text="Nome:").pack(anchor="w")
        self.entry_nome = ctk.CTkEntry(self.form_frame, width=300)
        self.entry_nome.pack(pady=5, fill="x")
        
        # Campo Senha
        ctk.CTkLabel(self.form_frame, text="Senha:").pack(anchor="w")
        self.entry_senha = ctk.CTkEntry(self.form_frame, width=300, show="*")
        self.entry_senha.pack(pady=5, fill="x")
        
        # Campo Tipo
        ctk.CTkLabel(self.form_frame, text="Tipo:").pack(anchor="w")
        self.tipo_var = ctk.StringVar(value="comum")
        self.radio_comum = ctk.CTkRadioButton(
            self.form_frame, 
            text="Comum", 
            variable=self.tipo_var, 
            value="comum"
        )
        self.radio_comum.pack(side="left", padx=5)
        
        self.radio_admin = ctk.CTkRadioButton(
            self.form_frame, 
            text="Administrador", 
            variable=self.tipo_var, 
            value="administrador"
        )
        self.radio_admin.pack(side="left", padx=5)
    
    def listar_usuarios(self):
        # Limpar a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute("SELECT id_usuario, nome, tipo FROM usuario")
            usuarios = cursor.fetchall()
            
            for usuario in usuarios:
                self.tree.insert("", "end", values=usuario)
                
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao carregar usuários: {str(e)}",
                icon="cancel"
            )
        finally:
            if conn:
                conn.close()
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.focus()
        if selected:
            values = self.tree.item(selected, "values")
            if values:
                self.id_usuario.set(values[0])
                self.entry_nome.delete(0, "end")
                self.entry_nome.insert(0, values[1])
                self.entry_senha.delete(0, "end")
                self.tipo_var.set(values[2])
    
    def inserir_usuario(self):
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        tipo = self.tipo_var.get()
        
        if not nome or not senha:
            CTkMessagebox(
                title="Aviso",
                message="Preencha todos os campos!",
                icon="warning"
            )
            return
        
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "INSERT INTO usuario (nome, senha, tipo) VALUES (%s, %s, %s)",
                (nome, senha, tipo)
            )
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso",
                message="Usuário cadastrado com sucesso!",
                icon="check"
            )
            
            self.limpar_campos()
            self.listar_usuarios()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao cadastrar usuário: {str(e)}",
                icon="cancel"
            )
        finally:
            if conn:
                conn.close()
    
    def atualizar_usuario(self):
        id_usuario = self.id_usuario.get()
        nome = self.entry_nome.get()
        senha = self.entry_senha.get()
        tipo = self.tipo_var.get()
        
        if not id_usuario:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um usuário para atualizar!",
                icon="warning"
            )
            return
        
        conn = conectar()
        cursor = conn.cursor()
        
        try:
            cursor.execute(
                "UPDATE usuario SET nome = %s, senha = %s, tipo = %s WHERE id_usuario = %s",
                (nome, senha, tipo, id_usuario)
            )
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso",
                message="Usuário atualizado com sucesso!",
                icon="check"
            )
            
            self.limpar_campos()
            self.listar_usuarios()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao atualizar usuário: {str(e)}",
                icon="cancel"
            )
        finally:
            if conn:
                conn.close()
    
    def excluir_usuario(self):
        id_usuario = self.id_usuario.get()
        
        if not id_usuario:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um usuário para excluir!",
                icon="warning"
            )
            return
        
        msg = CTkMessagebox(
            title="Confirmação",
            message=f"Tem certeza que deseja excluir o usuário {self.entry_nome.get()}?",
            icon="question",
            option_1="Cancelar",
            option_2="Excluir"
        )
        
        if msg.get() == "Excluir":
            conn = conectar()
            cursor = conn.cursor()
            
            try:
                cursor.execute(
                    "DELETE FROM usuario WHERE id_usuario = %s",
                    (id_usuario,)
                )
                conn.commit()
                
                CTkMessagebox(
                    title="Sucesso",
                    message="Usuário excluído com sucesso!",
                    icon="check"
                )
                
                self.limpar_campos()
                self.listar_usuarios()
                
            except Exception as e:
                CTkMessagebox(
                    title="Erro",
                    message=f"Falha ao excluir usuário: {str(e)}",
                    icon="cancel"
                )
            finally:
                if conn:
                    conn.close()
    
    def limpar_campos(self):
        self.id_usuario.set("")
        self.entry_nome.delete(0, "end")
        self.entry_senha.delete(0, "end")
        self.tipo_var.set("comum")
        self.tree.selection_remove(self.tree.selection())

def abrir():
    app = UsuarioCRUD()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()