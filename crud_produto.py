import customtkinter as ctk
from tkinter import ttk
from db_config import conectar
from CTkMessagebox import CTkMessagebox
import re

class ProdutoCRUD:
    def __init__(self,admin_menu=None):
        self.admin_menu = admin_menu
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Produto")
        self.janela.geometry("1000x750")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variável para controle da ordenação
        self.ordenacao = {
            'coluna': 'p.id_produto',
            'direcao': 'ASC'
        }
        
        self.criar_interface()
        self.carregar_fornecedores()
        self.listar_produtos()
        
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
            text="Cadastro de Produtos", 
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
            command=self.inserir_produto,
            width=120,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Atualizar", 
            command=self.atualizar_produto,
            width=120,
            fg_color="#17a2b8",
            hover_color="#138496"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Excluir", 
            command=self.excluir_produto,
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
        
        # Área de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.list_frame, 
            text="Lista de Produtos", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Treeview para exibição
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Nome", "Descrição", "Quantidade", "Preço", "Fornecedor"),
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        # Configurar colunas com bind para ordenação
        colunas = [
            ("ID", 50, "center", "p.id_produto"),
            ("Nome", 200, "w", "p.nome"),
            ("Descrição", 200, "w", "p.descricao"),
            ("Quantidade", 80, "center", "p.quantidade"),
            ("Preço", 100, "center", "p.preco"),
            ("Fornecedor", 150, "w", "f.nome")
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
        
        # Frame para botões inferiores
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(pady=10, fill="x")
        
        # Botão de atualizar lista
        ctk.CTkButton(
            self.bottom_frame,
            text="Atualizar Lista",
            command=self.listar_produtos,
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
    
    def voltar_admin(self):
        """Fecha a janela atual e reabre o menu admin"""
        self.janela.destroy()
        if self.admin_menu:
            self.admin_menu.janela.deiconify()
    
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
    
        # Configuração dos campos
        campos_config = [
            ("nome", "Nome:", 300),
            ("descricao", "Descrição:", 300),
            ("quantidade", "Quantidade:", 100),
            ("preco", "Preço (R$):", 150),
            ("id_fornecedor", "Fornecedor:", 250)
        ]
    
        # Criar campos dinamicamente
        for idx, (nome, label, largura) in enumerate(campos_config):
            # Label
            ctk.CTkLabel(
                campos_frame, 
                text=label,
                font=("Arial", 12)
            ).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
        
            # Entry ou Combobox
            if nome == "id_fornecedor":
                self.campos[nome] = ctk.CTkComboBox(
                    campos_frame,
                    width=largura,
                    font=("Arial", 12),
                    state="readonly"
                )
                self.campos[nome].set("Selecione...")
            else:
                self.campos[nome] = ctk.CTkEntry(
                    campos_frame,
                    width=largura,
                    font=("Arial", 12)
                )
        
            # Posicionamento
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
    
    # Removida a linha que tentava desabilitar o id_produto que não existe mais
    
    def carregar_fornecedores(self):
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_fornecedor, nome FROM fornecedor ORDER BY nome")
            
            fornecedores = cursor.fetchall()
            valores = [f"{id_} - {nome}" for id_, nome in fornecedores]
            
            self.campos["id_fornecedor"].configure(values=valores)
            
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao carregar fornecedores: {str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def ordenar_por_coluna(self, coluna):
        """Ordena os dados pela coluna clicada"""
        # Alterna a direção se clicar na mesma coluna
        if self.ordenacao['coluna'] == coluna:
            self.ordenacao['direcao'] = 'DESC' if self.ordenacao['direcao'] == 'ASC' else 'ASC'
        else:
            self.ordenacao['coluna'] = coluna
            self.ordenacao['direcao'] = 'ASC'
        
        self.listar_produtos()
    
    def validar_campos(self):
        # Verifica campos obrigatórios
        if not all([
            self.campos["nome"].get(),
            self.campos["quantidade"].get(),
            self.campos["preco"].get(),
            self.campos["id_fornecedor"].get() != "Selecione..."
        ]):
            CTkMessagebox(
                title="Erro",
                message="Preencha todos os campos obrigatórios!",
                icon="cancel"
            )
            return False
        
        # Valida quantidade
        try:
            quantidade = int(self.campos["quantidade"].get())
            if quantidade < 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erro",
                message="Quantidade deve ser um número inteiro positivo!",
                icon="cancel"
            )
            return False
        
        # Valida preço
        try:
            preco = float(self.campos["preco"].get().replace(",", "."))
            if preco <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erro",
                message="Preço deve ser um número positivo!",
                icon="cancel"
            )
            return False
        
        return True
    
    def limpar_campos(self):
        for nome, campo in self.campos.items():
            if isinstance(campo, ctk.CTkEntry):
                campo.delete(0, "end")
            elif isinstance(campo, ctk.CTkComboBox):
                campo.set("Selecione...")
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, "values")
        
            # Atualiza os campos com os dados selecionados
            self.limpar_campos()
        
            self.campos["nome"].insert(0, values[1])
            self.campos["descricao"].insert(0, values[2])
            self.campos["quantidade"].insert(0, values[3])
        
            # Formata o preço (remove "R$")
            preco = values[4].replace("R$", "").strip()
            self.campos["preco"].insert(0, preco)
        
            # Seleciona o fornecedor correspondente
            fornecedor = values[5]
            if fornecedor != "N/D":
                # Procura o fornecedor na lista de valores
                valores = self.campos["id_fornecedor"]._values
                for valor in valores:
                    if fornecedor in valor:
                        self.campos["id_fornecedor"].set(valor)
                        break
    
    def listar_produtos(self):
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
                SELECT p.id_produto, p.nome, p.descricao, p.quantidade, 
                       p.preco, f.nome as fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON p.id_fornecedor = f.id_fornecedor
                ORDER BY {self.ordenacao['coluna']} {self.ordenacao['direcao']}
            """
            
            cursor.execute(query)
            
            for produto in cursor.fetchall():
                # Formata os valores para exibição
                preco_formatado = f"R$ {produto[4]:.2f}"
                fornecedor = produto[5] if produto[5] else "N/D"
                
                self.tree.insert("", "end", values=(
                    produto[0],  # ID
                    produto[1],  # Nome
                    produto[2],  # Descrição
                    produto[3],  # Quantidade
                    preco_formatado,  # Preço formatado
                    fornecedor  # Fornecedor ou "N/D"
                ))
                
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao carregar produtos:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_produto(self):
        if not self.validar_campos():
            return
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Extrai ID do fornecedor (formato "ID - Nome")
            fornecedor = self.campos["id_fornecedor"].get()
            id_fornecedor = int(fornecedor.split(" - ")[0])
            
            # Executa a inserção
            cursor.execute("""
                INSERT INTO produto (nome, descricao, quantidade, preco, id_fornecedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.campos["nome"].get().strip(),
                self.campos["descricao"].get().strip(),
                int(self.campos["quantidade"].get()),
                float(self.campos["preco"].get().replace(",", ".")),
                id_fornecedor
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso",
                message="Produto cadastrado com sucesso!",
                icon="check"
            )
            
            self.limpar_campos()
            self.listar_produtos()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao cadastrar produto:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def atualizar_produto(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um produto para atualizar!",
                icon="warning"
            )
            return
            
        if not self.validar_campos():
            return
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Obtém o ID do produto selecionado
            produto_id = self.tree.item(selected, "values")[0]
            
            # Extrai ID do fornecedor (formato "ID - Nome")
            fornecedor = self.campos["id_fornecedor"].get()
            id_fornecedor = int(fornecedor.split(" - ")[0])
            
            # Executa a atualização
            cursor.execute("""
                UPDATE produto 
                SET nome = %s, descricao = %s, quantidade = %s, 
                    preco = %s, id_fornecedor = %s
                WHERE id_produto = %s
            """, (
                self.campos["nome"].get().strip(),
                self.campos["descricao"].get().strip(),
                int(self.campos["quantidade"].get()),
                float(self.campos["preco"].get().replace(",", ".")),
                id_fornecedor,
                produto_id
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso",
                message="Produto atualizado com sucesso!",
                icon="check"
            )
            
            self.listar_produtos()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro",
                message=f"Falha ao atualizar produto:\n{str(e)}",
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def excluir_produto(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso",
                message="Selecione um produto para excluir!",
                icon="warning"
            )
            return
        
        # Confirmação da exclusão
        confirmacao = CTkMessagebox(
            title="Confirmação", 
            message=f"Tem certeza que deseja excluir o produto {self.tree.item(selected, 'values')[1]}?",
            icon="question", 
            option_1="Cancelar", 
            option_2="Excluir"
        )
        
        if confirmacao.get() == "Excluir":
            conn = None
            cursor = None
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # Obtém o ID do produto selecionado
                produto_id = self.tree.item(selected, "values")[0]
                
                # Executa a exclusão
                cursor.execute("""
                    DELETE FROM produto 
                    WHERE id_produto = %s
                """, (produto_id,))
                
                conn.commit()
                
                CTkMessagebox(
                    title="Sucesso",
                    message="Produto excluído com sucesso!",
                    icon="check"
                )
                
                self.limpar_campos()
                self.listar_produtos()
                
            except Exception as e:
                CTkMessagebox(
                    title="Erro",
                    message=f"Falha ao excluir produto:\n{str(e)}",
                    icon="cancel"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

def abrir(admin_menu=None):
    app = ProdutoCRUD(admin_menu)
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()