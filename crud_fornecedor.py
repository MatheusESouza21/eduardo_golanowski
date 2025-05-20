import customtkinter as ctk
from db_config import conectar
from tkinter import ttk
import re
from CTkMessagebox import CTkMessagebox

class FornecedorCRUD:
    def __init__(self, admin_menu=None):
        self.admin_menu = admin_menu
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Fornecedor")
        self.janela.geometry("1000x700")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variável para controle da ordenação
        self.ordenacao = {
            'coluna': 'id_fornecedor',
            'direcao': 'ASC'
        }
        
        self.criar_interface()
        self.listar_fornecedores()
    
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
            text="Cadastro de Fornecedores", 
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Campos do formulário
        self.criar_campos_formulario()
        
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=15)
        
        # Botões de ação
        ctk.CTkButton(
            self.btn_frame, 
            text="Cadastrar", 
            command=self.inserir_fornecedor,
            width=120,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Atualizar", 
            command=self.atualizar_fornecedor,
            width=120,
            fg_color="#17a2b8",
            hover_color="#138496"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Excluir", 
            command=self.excluir_fornecedor,
            width=120,
            fg_color="#dc3545",
            hover_color="#c82333"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Limpar", 
            command=self.limpar_campos,
            width=120,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=5)

        # Frame inferior para botão Voltar
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(pady=10, padx=10, fill="x", expand=True)
        
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
        
        # Área de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

    def voltar_admin(self):
        self.janela.destroy()
        if self.admin_menu:
            self.admin_menu.deiconify()
        
        ctk.CTkLabel(
            self.list_frame, 
            text="Lista de Fornecedores", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Treeview para exibição
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Nome", "CNPJ", "Telefone", "Endereço"),
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        # Configurar colunas com bind para ordenação
        colunas = [
            ("ID", 50, "center", "id_fornecedor"),
            ("Nome", 200, "w", "nome"),
            ("CNPJ", 150, "center", "cnpj"),
            ("Telefone", 120, "center", "telefone"),
            ("Endereço", 300, "w", "endereco")
        ]
        
        for col, width, anchor, coluna_db in colunas:
            self.tree.heading(col, text=col, 
                            command=lambda c=coluna_db: self.ordenar_por_coluna(c))
            self.tree.column(col, width=width, anchor=anchor)
        
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
        
        # Configurar seleção
        self.tree.bind("<<TreeviewSelect>>", self.carregar_dados_selecionados)
        
        # Estilização do Treeview
        self.configurar_estilo_treeview()
        
        # Botão de atualizar lista
        ctk.CTkButton(
            self.list_frame,
            text="Atualizar Lista",
            command=self.listar_fornecedores,
            width=120
        ).pack(pady=10)
    
    def configurar_estilo_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=25,
            fieldbackground="#2b2b2b",
            bordercolor="#343638",
            borderwidth=0
        )
        style.map('Treeview', background=[('selected', '#3b8ed0')])
        
        style.configure("Treeview.Heading",
            background="#565b5e",
            foreground="white",
            relief="flat",
            font=('Arial', 10, 'bold')
        )
        style.map("Treeview.Heading",
            background=[('active', '#3484F0')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
    
    def criar_campos_formulario(self):
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(fill="x", padx=10, pady=5)
        
        # Dicionário para armazenar os campos
        self.campos = {}
        
        # Configuração dos campos (removido o campo id_fornecedor)
        campos_config = [
            ("nome", "Nome:", 300),
            ("cnpj", "CNPJ:", 150, "00.000.000/0000-00"),
            ("telefone", "Telefone:", 150, "(00) 0000-0000"),
            ("endereco", "Endereço:", 400)
        ]
        
        # Criar campos dinamicamente
        for idx, (nome, label, largura, *placeholder) in enumerate(campos_config):
            # Label
            ctk.CTkLabel(
                campos_frame, 
                text=label,
                font=("Arial", 12)
            ).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            
            # Entry
            placeholder_text = placeholder[0] if placeholder else ""
            self.campos[nome] = ctk.CTkEntry(
                campos_frame,
                width=largura,
                placeholder_text=placeholder_text,
                font=("Arial", 12)
            )
            
            # Posicionamento
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            
            # Bind para formatação automática
            if nome == "cnpj":
                self.campos[nome].bind("<KeyRelease>", self.formatar_cnpj_digitacao)
            elif nome == "telefone":
                self.campos[nome].bind("<KeyRelease>", self.formatar_telefone_digitacao)
    
    def formatar_cnpj_digitacao(self, event):
        # Pega o texto atual sem formatação
        texto = re.sub(r'[^0-9]', '', self.campos["cnpj"].get())
        
        # Aplica a máscara
        formatado = ""
        if len(texto) > 0:
            formatado = texto[:2]
        if len(texto) > 2:
            formatado += "." + texto[2:5]
        if len(texto) > 5:
            formatado += "." + texto[5:8]
        if len(texto) > 8:
            formatado += "/" + texto[8:12]
        if len(texto) > 12:
            formatado += "-" + texto[12:14]
        
        # Atualiza o campo
        self.campos["cnpj"].delete(0, "end")
        self.campos["cnpj"].insert(0, formatado)
    
    def formatar_telefone_digitacao(self, event):
        # Pega o texto atual sem formatação
        texto = re.sub(r'[^0-9]', '', self.campos["telefone"].get())
        
        # Aplica a máscara
        formatado = ""
        if len(texto) > 0:
            formatado = "(" + texto[:2]
        if len(texto) > 2:
            formatado += ") " + texto[2:6]
        if len(texto) > 6:
            formatado += "-" + texto[6:10]
        
        # Atualiza o campo
        self.campos["telefone"].delete(0, "end")
        self.campos["telefone"].insert(0, formatado)
    
    def ordenar_por_coluna(self, coluna):
        """Ordena os dados pela coluna clicada"""
        # Alterna a direção se clicar na mesma coluna
        if self.ordenacao['coluna'] == coluna:
            self.ordenacao['direcao'] = 'DESC' if self.ordenacao['direcao'] == 'ASC' else 'ASC'
        else:
            self.ordenacao['coluna'] = coluna
            self.ordenacao['direcao'] = 'ASC'
        
        self.listar_fornecedores()
    
    def limpar_campos(self):
        for nome, campo in self.campos.items():
            if isinstance(campo, ctk.CTkEntry):
                campo.delete(0, "end")
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, "values")
            
            # Atualiza os campos com os dados selecionados
            self.limpar_campos()
            
            self.campos["nome"].insert(0, values[1])
            self.campos["cnpj"].insert(0, values[2])
            self.campos["telefone"].insert(0, values[3])
            self.campos["endereco"].insert(0, values[4])
    
    def listar_fornecedores(self):
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Monta a query com ordenação dinâmica
            query = f"""
                SELECT id_fornecedor, nome, cnpj, telefone, endereco
                FROM fornecedor
                ORDER BY {self.ordenacao['coluna']} {self.ordenacao['direcao']}
            """
            
            cursor.execute(query)
            
            for fornecedor in cursor.fetchall():
                # Formata CNPJ
                cnpj = fornecedor[2]
                cnpj_formatado = f"{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}" if cnpj else ""
                
                # Formata telefone
                telefone = fornecedor[3]
                telefone_formatado = f"({telefone[:2]}) {telefone[2:6]}-{telefone[6:]}" if telefone and len(telefone) >= 10 else telefone
                
                self.tree.insert("", "end", values=(
                    fornecedor[0],  # ID
                    fornecedor[1],  # Nome
                    cnpj_formatado, # CNPJ formatado
                    telefone_formatado,  # Telefone formatado
                    fornecedor[4]   # Endereço
                ))
                
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao carregar fornecedores:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_fornecedor(self):
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Prepara os dados
            cnpj = re.sub(r'[^0-9]', '', self.campos["cnpj"].get())
            telefone = re.sub(r'[^0-9]', '', self.campos["telefone"].get())
            
            # Executa a inserção
            cursor.execute("""
                INSERT INTO fornecedor (nome, cnpj, telefone, endereco)
                VALUES (%s, %s, %s, %s)
            """, (
                self.campos["nome"].get().strip(),
                cnpj,
                telefone,
                self.campos["endereco"].get().strip()
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso", 
                message="Fornecedor cadastrado com sucesso!",
                icon="check"
            )
            
            self.limpar_campos()
            self.listar_fornecedores()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao cadastrar fornecedor:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def atualizar_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso", 
                message="Selecione um fornecedor para atualizar!",
                icon="warning"
            )
            return
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Obtém o ID do fornecedor selecionado
            fornecedor_id = self.tree.item(selected, "values")[0]
            
            # Prepara os dados
            cnpj = re.sub(r'[^0-9]', '', self.campos["cnpj"].get())
            telefone = re.sub(r'[^0-9]', '', self.campos["telefone"].get())
            
            # Executa a atualização
            cursor.execute("""
                UPDATE fornecedor 
                SET nome = %s, cnpj = %s, telefone = %s, endereco = %s
                WHERE id_fornecedor = %s
            """, (
                self.campos["nome"].get().strip(),
                cnpj,
                telefone,
                self.campos["endereco"].get().strip(),
                fornecedor_id
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso", 
                message="Fornecedor atualizado com sucesso!",
                icon="check"
            )
            
            self.listar_fornecedores()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao atualizar fornecedor:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def excluir_fornecedor(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso", 
                message="Selecione um fornecedor para excluir!",
                icon="warning"
            )
            return
        
        # Confirmação da exclusão
        confirmacao = CTkMessagebox(
            title="Confirmação", 
            message=f"Tem certeza que deseja excluir o fornecedor {self.tree.item(selected, 'values')[1]}?",
            icon="question", 
            option_1="Cancelar", 
            option_2="Sim"
        )
        
        if confirmacao.get() == "Sim":
            conn = None
            cursor = None
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # Obtém o ID do fornecedor selecionado
                fornecedor_id = self.tree.item(selected, "values")[0]
                
                # Executa a exclusão
                cursor.execute("""
                    DELETE FROM fornecedor 
                    WHERE id_fornecedor = %s
                """, (fornecedor_id,))
                
                conn.commit()
                
                CTkMessagebox(
                    title="Sucesso", 
                    message="Fornecedor excluído com sucesso!",
                    icon="check"
                )
                
                self.limpar_campos()
                self.listar_fornecedores()
                
            except Exception as e:
                CTkMessagebox(
                    title="Erro", 
                    message=f"Existem jogos cadastrados a esse fornecedor!",
                    icon="cancel"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

def abrir(admin_menu=None):
    app = FornecedorCRUD(admin_menu)
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()