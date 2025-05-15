import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox
<<<<<<< HEAD
from admin_crud import abrir_menu_admin
=======
from tkinter import ttk

>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
class ProdutoCRUD:
    def __init__(self, janela_principal=None):
        self.janela_principal = janela_principal  # Armazena a referência à janela principal
        
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Produto")
        self.janela.geometry("1000x750")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
<<<<<<< HEAD
        # Configurar comportamento ao fechar a janela
        self.janela.protocol("WM_DELETE_WINDOW", self.fechar_janela)
=======
        # Variável para controle da ordenação
        self.ordenacao = {
            'coluna': 'p.id',
            'direcao': 'ASC'
        }
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
        
        self.criar_interface()
        self.carregar_fornecedores()
        self.listar_produtos()
    
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
        
<<<<<<< HEAD
        # Frame de botões (formulário)
        self.btn_form_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_form_frame.pack(pady=10)
=======
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=15)
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
        
        # Botões de ação do formulário
        ctk.CTkButton(
<<<<<<< HEAD
            self.btn_form_frame, 
            text="Inserir", 
=======
            self.btn_frame, 
            text="Cadastrar", 
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
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
            self.btn_form_frame, 
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
            ("ID", 50, "center", "p.id"),
            ("Nome", 200, "w", "p.nome"),
            ("Descrição", 200, "w", "p.descricao"),
            ("Quantidade", 80, "center", "p.quantidade"),
            ("Preço", 100, "center", "p.preco"),
            ("Fornecedor", 150, "w", "f.nome")
        ]
        
<<<<<<< HEAD
        # Frame de botões (listagem)
        self.btn_list_frame = ctk.CTkFrame(self.list_frame, fg_color="transparent")
        self.btn_list_frame.pack(pady=5, fill="x")
        
        # Botão de atualizar
=======
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
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
        ctk.CTkButton(
            self.btn_list_frame,
            text="Atualizar Lista",
            command=self.listar_produtos,
            width=120
<<<<<<< HEAD
        ).pack(side="left", padx=5)
        
        # Botão de voltar
        ctk.CTkButton(
            self.btn_list_frame,
            text="⬅️ Voltar",
            command=self.voltar,
            fg_color="transparent",
            border_width=1,
            text_color=("gray10", "#DCE4EE"),
            width=120
        ).pack(side="right", padx=5)
    
    def voltar(self):
        """Volta para a janela principal"""
        self.janela.destroy()
        abrir_menu_admin()
    
    def fechar_janela(self):
        """Lida com o fechamento da janela"""
        self.voltar()
=======
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
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
    
    def criar_campos_formulario(self):
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(fill="x", padx=10, pady=5)
        
        # Dicionário para armazenar os campos
        self.campos = {}
        
        # Configuração dos campos
        campos_config = [
            ("id_produto", "ID Produto:", 100),
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
        
        # Desabilitar campo ID (auto-incremento)
        self.campos["id_produto"].configure(state="disabled")
    
    def carregar_fornecedores(self):
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
<<<<<<< HEAD
            cursor.execute("SELECT id_produto, nome FROM fornecedor ORDER BY nome")
=======
            cursor.execute("SELECT id_fornecedor, nome FROM fornecedor ORDER BY nome")
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
            
            fornecedores = cursor.fetchall()
            valores = [f"{id_produto} - {nome}" for id_produto, nome in fornecedores]
            
            self.campos["id_produto"].configure(values=valores)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {str(e)}")
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
            self.campos["id_produto"].get() != "Selecione..."
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return False
        
        # Valida quantidade
        try:
            quantidade = int(self.campos["quantidade"].get())
            if quantidade < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro positivo!")
            return False
        
        # Valida preço
        try:
            preco = float(self.campos["preco"].get().replace(",", "."))
            if preco <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Erro", "Preço deve ser um número positivo!")
            return False
        
        return True
    
    def limpar_campos(self):
        for nome, campo in self.campos.items():
            if isinstance(campo, ctk.CTkEntry):
                if nome != "id_produto":
                    campo.delete(0, "end")
            elif isinstance(campo, ctk.CTkComboBox):
                campo.set("Selecione...")
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, "values")
            
            # Atualiza os campos com os dados selecionados
            self.limpar_campos()
            
            # ID Produto (se necessário)
            # self.campos["id_produto"].configure(state="normal")
            # self.campos["id_produto"].delete(0, "end")
            # self.campos["id_produto"].insert(0, values[0])
            # self.campos["id_produto"].configure(state="disabled")
            
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
            messagebox.showerror("Erro", f"Falha ao carregar produtos:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_produto(self):
        if not self.validar_campos():
            return
<<<<<<< HEAD
            
        # Extrai ID do fornecedor (formato "ID - Nome")
        fornecedor = self.campos["id_produto"].get()
        id_fornecedor = int(fornecedor.split(" - ")[0])
=======
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
        
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
                INSERT INTO produto (nome, descricao, quantidade, preco, id_produto)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.campos["nome"].get().strip(),
                self.campos["descricao"].get().strip(),
                int(self.campos["quantidade"].get()),
                float(self.campos["preco"].get().replace(",", ".")),
                id_fornecedor
            ))
            
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            self.limpar_campos()
            self.listar_produtos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao cadastrar produto:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def atualizar_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto para atualizar!")
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
<<<<<<< HEAD
                SELECT p.id_produto, p.nome, p.descricao, p.quantidade, 
                       p.preco, f.nome as fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON p.id_fornecedor = f.id_produto
                ORDER BY p.id_produto
            """)
=======
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
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
            
            conn.commit()
            
            messagebox.showinfo("Sucesso", "Produto atualizado com sucesso!")
            
            self.listar_produtos()
            
<<<<<<< HEAD
            # Dados formatados
            for id_produto in cursor.fetchall():
                self.textbox.insert(ctk.END, 
                    f"{id_produto[0]:<4}| {id_produto[1][:20]:<20}| {id_produto[2][:20]:<20}| "
                    f"{id_produto[3]:<5}| R${id_produto[4]:<8.2f}| {id_produto[5] or 'N/D'}\n"
                )
                
=======
>>>>>>> b2923b8996208e87258bc8b3570e8be4497ed7a4
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao atualizar produto:\n{str(e)}")
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def excluir_produto(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir!")
            return
        
        # Confirmação da exclusão
        confirmacao = messagebox.askyesno(
            "Confirmação", 
            f"Tem certeza que deseja excluir o produto {self.tree.item(selected, 'values')[1]}?"
        )
        
        if confirmacao:
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
                
                messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
                
                self.limpar_campos()
                self.listar_produtos()
                
            except Exception as e:
                messagebox.showerror("Erro", f"Falha ao excluir produto:\n{str(e)}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

def abrir(janela_principal=None):
    app = ProdutoCRUD(janela_principal)
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()