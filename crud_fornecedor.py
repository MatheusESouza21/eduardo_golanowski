import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox

# Configuração do tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class CrudProdutos:
    def __init__(self, master):
        self.master = master
        master.title("CRUD - Produto")
        master.geometry("800x700")
        
        self.criar_widgets()
        self.listar_produtos()
    
    def criar_widgets(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(master=self.master)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Frame do formulário
        self.form_frame = ctk.CTkFrame(master=self.main_frame)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # Título
        ctk.CTkLabel(self.form_frame, text="Cadastro de Produtos", font=("Arial", 14, "bold")).pack(pady=5)

        # Grid de campos
        self.campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.campos_frame.pack(pady=10, padx=10, fill="x")

        # Campos de entrada
        self.criar_campos()
        
        # Botões
        self.criar_botoes()
        
        # Área de listagem
        self.criar_listagem()

    def criar_campos(self):
        # Nome
        ctk.CTkLabel(self.campos_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.entry_nome = ctk.CTkEntry(self.campos_frame, width=300)
        self.entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Descrição
        ctk.CTkLabel(self.campos_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.entry_descricao = ctk.CTkEntry(self.campos_frame, width=300)
        self.entry_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Quantidade
        ctk.CTkLabel(self.campos_frame, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.entry_quantidade = ctk.CTkEntry(self.campos_frame, width=100)
        self.entry_quantidade.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Preço
        ctk.CTkLabel(self.campos_frame, text="Preço (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
        self.entry_preco = ctk.CTkEntry(self.campos_frame, width=100)
        self.entry_preco.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # Fornecedor
        ctk.CTkLabel(self.campos_frame, text="ID Fornecedor:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        self.entry_id_fornecedor = ctk.CTkEntry(self.campos_frame, width=100)
        self.entry_id_fornecedor.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    def criar_botoes(self):
        # Frame de botões
        self.botoes_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.botoes_frame.pack(pady=10)

        # Botões
        self.btn_inserir = ctk.CTkButton(self.botoes_frame, text="Inserir", command=self.inserir_produto)
        self.btn_inserir.grid(row=0, column=0, padx=5)

        self.btn_atualizar = ctk.CTkButton(self.botoes_frame, text="Atualizar", command=self.atualizar_produto)
        self.btn_atualizar.grid(row=0, column=1, padx=5)

        self.btn_remover = ctk.CTkButton(self.botoes_frame, text="Remover", command=self.remover_produto)
        self.btn_remover.grid(row=0, column=2, padx=5)

        self.btn_limpar = ctk.CTkButton(self.botoes_frame, text="Limpar", command=self.limpar_campos)
        self.btn_limpar.grid(row=0, column=3, padx=5)

    def criar_listagem(self):
        # Frame de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)

        # Título
        ctk.CTkLabel(self.list_frame, text="Lista de Produtos", font=("Arial", 14, "bold")).pack(pady=5)

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

        # Bind para seleção de produto
        self.textbox.bind("<Button-1>", self.selecionar_produto)

    def listar_produtos(self):
        self.textbox.delete("1.0", ctk.END)
        
        conn = conectar()
        if conn is None:
            messagebox.showerror("Erro", "Não foi possível conectar ao banco de dados")
            return
            
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id_fornecedor, nome, descricao, quantidade, 
                       preco, nome as fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON id_fornecedor = id
                ORDER BY id_produto
            """)
            
            # Cabeçalho
            self.textbox.insert(ctk.END, "ID  | NOME                | DESCRIÇÃO          | QTD | PREÇO   | FORNECEDOR\n")
            self.textbox.insert(ctk.END, "-"*90 + "\n")
            
            # Dados
            for id_produto in cursor.fetchall():
                self.textbox.insert(ctk.END, 
                    f"{id_produto[0]:<4}| {id_produto[1][:20]:<20}| {id_produto[2][:20]:<20}| "
                    f"{id_produto[3]:<4}| R${id_produto[4]:<7.2f}| {id_produto[5] or 'N/D'}\n"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
        finally:
            conn.close()

    def inserir_produto(self):
        # Validação
        if not all([
            self.entry_id_produto.get(),
            self.entry_nome.get(),
            self.entry_quantidade.get().isdigit(),
            self.entry_preco.get().replace('.', '').isdigit(),
            self.entry_id_fornecedor.get().isdigit()
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return
            
        conn = conectar()
        if conn is None:
            return
            
        cursor = conn.cursor()
        try:
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
            conn.close()

    def atualizar_produto(self):
        # Implementação similar à inserção, mas com UPDATE
        pass

    def remover_produto(self):
        # Implementação para deletar produto
        pass

    def limpar_campos(self):
        self.entry_nome.delete(0, ctk.END)
        self.entry_descricao.delete(0, ctk.END)
        self.entry_quantidade.delete(0, ctk.END)
        self.entry_preco.delete(0, ctk.END)
        self.entry_id_fornecedor.delete(0, ctk.END)

    def selecionar_produto(self, event):
        # Implementação para selecionar produto da lista
        pass

def abrir():
    janela = ctk.CTkToplevel()
    app = CrudProdutos(janela)

if __name__ == "__main__":
    root = ctk.CTk()
    app = CrudProdutos(root)
    root.mainloop()