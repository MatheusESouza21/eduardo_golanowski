import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox
import re

# Configuração do tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CrudProduto:
    def __init__(self):
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Produto")
        self.janela.geometry("1000x800")
        
        # Configurar grid principal
        self.janela.grid_columnconfigure(0, weight=1)
        self.janela.grid_rowconfigure(1, weight=1)
        
        self.criar_widgets()
        self.listar_produtos()
    
    def criar_widgets(self):
        # Frame do formulário
        form_frame = ctk.CTkFrame(self.janela)
        form_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")
        
        # Título
        ctk.CTkLabel(form_frame, text="Cadastro de Produtos", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=10)
        
        # Campos do formulário
        campos = [
            ("Nome", "entry_nome", 300),
            ("Descrição", "entry_descricao", 300),
            ("Quantidade", "entry_quantidade", 100),
            ("Preço (R$)", "entry_preco", 100),
            ("ID Fornecedor", "entry_id_fornecedor", 100)
        ]
        
        for i, (label, attr, width) in enumerate(campos, start=1):
            ctk.CTkLabel(form_frame, text=label).grid(row=i, column=0, padx=5, pady=5, sticky="e")
            entry = ctk.CTkEntry(form_frame, width=width)
            entry.grid(row=i, column=1, padx=5, pady=5, sticky="w")
            setattr(self, attr, entry)
            
            # Adicionar validação para campos numéricos
            if label in ["Quantidade", "ID Fornecedor"]:
                entry.configure(validate="key", validatecommand=(self.janela.register(self.validar_inteiro), '%P'))
            elif label == "Preço (R$)":
                entry.configure(validate="key", validatecommand=(self.janela.register(self.validar_decimal), '%P'))
        
        # Botões
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=len(campos)+1, column=0, columnspan=2, pady=10)
        
        ctk.CTkButton(btn_frame, text="Inserir", command=self.inserir_produto).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Limpar", command=self.limpar_campos).pack(side="left", padx=5)
        
        # Frame da lista
        list_frame = ctk.CTkFrame(self.janela)
        list_frame.grid(row=1, column=0, padx=20, pady=(0, 20), sticky="nsew")
        
        # Treeview para exibição dos dados
        self.tree = ctk.CTkTreeview(list_frame, columns=("ID", "Nome", "Descrição", "Quantidade", "Preço", "Fornecedor"), show="headings")
        
        # Configurar colunas
        colunas = [
            ("ID", 50),
            ("Nome", 150),
            ("Descrição", 200),
            ("Quantidade", 80),
            ("Preço", 80),
            ("Fornecedor", 100)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # Scrollbar
        scrollbar = ctk.CTkScrollbar(list_frame, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bind para seleção
        self.tree.bind("<ButtonRelease-1>", self.selecionar_produto)
    
    def validar_inteiro(self, valor):
        return valor.isdigit() or valor == ""
    
    def validar_decimal(self, valor):
        return bool(re.match(r'^\d*\.?\d*$', valor)) or valor == ""
    
    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_descricao.delete(0, ctk.END)
        self.entry_quantidade.delete(0, ctk.END)
        self.entry_preco.delete(0, ctk.END)
        self.entry_id_fornecedor.delete(0, ctk.END)
    
    def listar_produtos(self):
        # Limpar treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.id, p.nome, p.descricao, p.quantidade, 
                       p.preco, COALESCE(f.nome, 'N/D') as fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON p.id_fornecedor = f.id
                ORDER BY p.nome
            """)
            
            for produto in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    produto[0],
                    produto[1],
                    produto[2],
                    produto[3],
                    f"R$ {produto[4]:.2f}",
                    produto[5]
                ))
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
        finally:
            conn.close()
    
    def inserir_produto(self):
        # Validação dos campos
        if not all([
            self.entry_nome.get(),
            self.entry_quantidade.get(),
            self.entry_preco.get(),
            self.entry_id_fornecedor.get()
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return
        
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO produto (nome, descricao, quantidade, preco, id_fornecedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.entry_nome.get(),
                self.entry_descricao.get(),
                int(self.entry_quantidade.get()),
                float(self.entry_preco.get()),
                int(self.entry_id_fornecedor.get())
            ))
            
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            self.limpar_campos()
            self.listar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir produto: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def selecionar_produto(self, event):
        item = self.tree.selection()
        if item:
            valores = self.tree.item(item, "values")
            # Aqui você pode implementar a edição/exclusão
            # Exemplo: preencher os campos para edição
            pass

def abrir():
    CrudProduto()