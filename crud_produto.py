import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox

class ProdutoCRUD:
    def __init__(self):
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Produto")
        self.janela.geometry("900x750")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
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
            command=self.inserir_produto,
            width=100
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
            text="Lista de Produtos", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Textbox com scrollbar
        self.scrollbar = ctk.CTkScrollbar(self.list_frame)
        self.scrollbar.pack(side="right", fill="y")
        
        self.textbox = ctk.CTkTextbox(
            self.list_frame, 
            yscrollcommand=self.scrollbar.set,
            font=("Courier New", 12),
            wrap="none"
        )
        self.textbox.pack(pady=5, padx=5, fill="both", expand=True)
        
        self.scrollbar.configure(command=self.textbox.yview)
        
        # Botão de atualizar
        ctk.CTkButton(
            self.list_frame,
            text="Atualizar Lista",
            command=self.listar_produtos
        ).pack(pady=5)
    
    def criar_campos_formulario(self):
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(pady=10, padx=10, fill="x")
        
        # Dicionário para armazenar os campos
        self.campos = {}
        
        # Configuração dos campos
        campos_config = [
            ("nome", "Nome:", 300),
            ("descricao", "Descrição:", 300),
            ("quantidade", "Quantidade:", 100),
            ("preco", "Preço (R$):", 100),
            ("id_fornecedor", "Fornecedor:", 200)
        ]
        
        for idx, (nome, label, largura) in enumerate(campos_config):
            ctk.CTkLabel(campos_frame, text=label).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            
            if nome == "id_fornecedor":
                self.campos[nome] = ctk.CTkComboBox(campos_frame, width=largura)
                self.campos[nome].set("Selecione...")
            else:
                self.campos[nome] = ctk.CTkEntry(campos_frame, width=largura)
                
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
    
    def carregar_fornecedores(self):
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id, nome FROM fornecedor ORDER BY nome")
            
            fornecedores = cursor.fetchall()
            valores = [f"{id_produto} - {nome}" for id_produto, nome in fornecedores]
            
            self.campos["id_fornecedor"].configure(values=valores)
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar fornecedores: {str(e)}")
        finally:
            conn.close()
    
    def validar_campos(self):
        # Verifica se todos os campos obrigatórios estão preenchidos
        if not all([
            self.campos["id_produto"].get(),
            self.campos["nome"].get(),
            self.campos["quantidade"].get(),
            self.campos["preco"].get(),
            self.campos["id_fornecedor"].get() != "Selecione..."
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos obrigatórios!")
            return False
        
        # Valida quantidade
        try:
            quantidade = int(self.campos["quantidade"].get())
            if quantidade <= 0:
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
        for campo in self.campos.values():
            if isinstance(campo, ctk.CTkEntry):
                campo.delete(0, ctk.END)
            elif isinstance(campo, ctk.CTkComboBox):
                campo.set("Selecione...")
    
    def inserir_produto(self):
        if not self.validar_campos():
            return
            
        # Extrai ID do fornecedor (formato "ID - Nome")
        fornecedor = self.campos["id_fornecedor"].get()
        id_fornecedor = int(fornecedor.split(" - ")[0])
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO produto (nome, descricao, quantidade, preco, id_fornecedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                self.campos["nome"].get(),
                self.campos["descricao"].get(),
                int(self.campos["quantidade"].get()),
                float(self.campos["preco"].get().replace(",", ".")),
                id_fornecedor
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            self.limpar_campos()
            self.listar_produtos()
            
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir produto: {str(e)}")
        finally:
            conn.close()
    
    def listar_produtos(self):
        self.textbox.delete("1.0", ctk.END)
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id_produto, nome, descricao, quantidade, 
                       preco, nome as id_fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON id_fornecedor = id_produto
                ORDER BY id_produto
            """)
            
            # Cabeçalho formatado
            self.textbox.insert(ctk.END, 
                "ID  | NOME                | DESCRIÇÃO          | QTD  | PREÇO    | FORNECEDOR\n")
            self.textbox.insert(ctk.END, "-"*95 + "\n")
            
            # Dados formatados
            for id_produto in cursor.fetchall():
                self.textbox.insert(ctk.END, 
                    f"{id_produto[0]:<4}| {id_produto[1][:20]:<20}| {id_produto[2][:20]:<20}| "
                    f"{id_produto[3]:<5}| R${id_produto[4]:<8.2f}| {id_produto[5] or 'N/D'}\n"
                )
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
        finally:
            conn.close()

def abrir():
    app = ProdutoCRUD()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()