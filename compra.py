import customtkinter as ctk
from db_config import conectar
from tkinter import ttk
from CTkMessagebox import CTkMessagebox

class SistemaCompras:
    def __init__(self):
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Compras")
        self.janela.geometry("1000x700")
        
        # Configuração do tema
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("green")
        
        # Variáveis de estado
        self.carrinho = []
        self.total_compra = 0.0
        
        self.criar_interface()
    
    def criar_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Produtos Disponíveis", 
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        # Frame da lista de produtos
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Treeview para produtos (usando ttk.Treeview por ser mais completo)
        self.produtos_tree = ttk.Treeview(
            self.list_frame,
            columns=("id", "nome", "descricao", "preco", "estoque"),
            show="headings",
            height=15
        )
        
        # Configurar colunas
        colunas = [
            ("ID", 50),
            ("Produto", 150),
            ("Descrição", 300),
            ("Preço", 80),
            ("Estoque", 80)
        ]
        
        for col, width in colunas:
            self.produtos_tree.heading(col.lower(), text=col)
            self.produtos_tree.column(col.lower(), width=width, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.produtos_tree.yview)
        self.produtos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.produtos_tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Frame de compra
        compra_frame = ctk.CTkFrame(self.main_frame)
        compra_frame.pack(pady=10, fill="x")
        
        ctk.CTkLabel(compra_frame, text="Quantidade:").pack(side="left", padx=5)
        self.quantidade_entry = ctk.CTkEntry(compra_frame, width=80)
        self.quantidade_entry.pack(side="left", padx=5)
        
        btn_comprar = ctk.CTkButton(
            compra_frame, 
            text="Adicionar ao Carrinho",
            command=self.adicionar_carrinho
        )
        btn_comprar.pack(side="left", padx=10)
        
        # Frame do carrinho
        carrinho_frame = ctk.CTkFrame(self.main_frame)
        carrinho_frame.pack(pady=10, fill="both", expand=True)
        
        ctk.CTkLabel(carrinho_frame, text="Seu Carrinho", font=("Arial", 14)).pack()
        
        # Treeview para carrinho
        self.carrinho_tree = ttk.Treeview(
            carrinho_frame,
            columns=("produto", "quantidade", "subtotal"),
            show="headings",
            height=5
        )
        
        for col, width in [("Produto", 300), ("Quantidade", 100), ("Subtotal", 100)]:
            self.carrinho_tree.heading(col.lower(), text=col)
            self.carrinho_tree.column(col.lower(), width=width, anchor="center")
        
        self.carrinho_tree.pack(pady=5, fill="both", expand=True)
        
        # Total da compra
        total_frame = ctk.CTkFrame(self.main_frame)
        total_frame.pack(pady=5, fill="x")
        
        ctk.CTkLabel(total_frame, text="Total da Compra:").pack(side="left", padx=5)
        self.total_label = ctk.CTkLabel(total_frame, text="R$ 0,00", font=("Arial", 14, "bold"))
        self.total_label.pack(side="left")
        
        # Botões de ação
        btn_frame = ctk.CTkFrame(self.main_frame)
        btn_frame.pack(pady=10, fill="x")
        
        ctk.CTkButton(
            btn_frame,
            text="Limpar Carrinho",
            command=self.limpar_carrinho,
            fg_color="gray",
            hover_color="darkgray"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="Finalizar Compra",
            command=self.finalizar_compra
        ).pack(side="right", padx=5)
        
        # Carregar produtos inicialmente
        self.carregar_produtos()
    
    def carregar_produtos(self):
        # Limpar treeview
        for item in self.produtos_tree.get_children():
            self.produtos_tree.delete(item)
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nome, descricao, preco, quantidade 
                FROM produto 
                WHERE quantidade > 0
                ORDER BY nome
            """)
            
            for produto in cursor.fetchall():
                self.produtos_tree.insert("", "end", values=(
                    produto[0],
                    produto[1],
                    produto[2],
                    f"{produto[3]:.2f}",
                    produto[4]
                ))
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao carregar produtos: {str(e)}", icon="cancel")
        finally:
            conn.close()
    
    def adicionar_carrinho(self):
        item_selecionado = self.produtos_tree.selection()
        if not item_selecionado:
            CTkMessagebox(title="Aviso", message="Selecione um produto primeiro!", icon="warning")
            return
        
        try:
            quantidade = int(self.quantidade_entry.get())
            if quantidade <= 0:
                raise ValueError
            
            # Verificar estoque
            valores = self.produtos_tree.item(item_selecionado, "values")
            estoque = int(valores[4])
            if quantidade > estoque:
                CTkMessagebox(title="Aviso", message="Quantidade indisponível em estoque!", icon="warning")
                return
            
            # Adicionar ao carrinho
            produto_id = valores[0]
            nome_produto = valores[1]
            preco = float(valores[3])
            subtotal = preco * quantidade
            
            # Verificar se produto já está no carrinho
            for item in self.carrinho_tree.get_children():
                item_values = self.carrinho_tree.item(item, "values")
                if item_values[0] == nome_produto:
                    nova_quantidade = int(item_values[1]) + quantidade
                    novo_subtotal = float(item_values[2]) + subtotal
                    self.carrinho_tree.item(item, values=(
                        nome_produto,
                        nova_quantidade,
                        f"{novo_subtotal:.2f}"
                    ))
                    break
            else:
                self.carrinho_tree.insert("", "end", values=(
                    nome_produto,
                    quantidade,
                    f"{subtotal:.2f}"
                ))
            
            # Atualizar total
            self.total_compra += subtotal
            self.total_label.configure(text=f"R$ {self.total_compra:.2f}")
            
            # Limpar campo de quantidade
            self.quantidade_entry.delete(0, "end")
            
        except ValueError:
            CTkMessagebox(title="Erro", message="Quantidade inválida! Digite um número positivo.", icon="cancel")
    
    def limpar_carrinho(self):
        for item in self.carrinho_tree.get_children():
            self.carrinho_tree.delete(item)
        self.total_compra = 0.0
        self.total_label.configure(text="R$ 0,00")
    
    def finalizar_compra(self):
        if not self.carrinho_tree.get_children():
            CTkMessagebox(title="Aviso", message="Carrinho vazio!", icon="warning")
            return
        
        resposta = CTkMessagebox(
            title="Confirmar Compra",
            message="Deseja finalizar a compra?",
            icon="question",
            option_1="Cancelar",
            option_2="Confirmar"
        )
        
        if resposta.get() == "Confirmar":
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # Registrar venda no banco de dados
                for item in self.carrinho_tree.get_children():
                    valores = self.carrinho_tree.item(item, "values")
                    nome_produto = valores[0]
                    quantidade = int(valores[1])
                    
                    # Atualizar estoque
                    cursor.execute("""
                        UPDATE produto 
                        SET quantidade = quantidade - %s 
                        WHERE nome = %s
                    """, (quantidade, nome_produto))
                
                conn.commit()
                CTkMessagebox(title="Sucesso", message="Compra realizada com sucesso!", icon="check")
                self.limpar_carrinho()
                self.carregar_produtos()  # Atualizar lista de produtos
                
            except Exception as e:
                CTkMessagebox(title="Erro", message=f"Falha ao registrar compra: {str(e)}", icon="cancel")
            finally:
                conn.close()

def abrir_tela_compra():
    app = SistemaCompras()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir_tela_compra()