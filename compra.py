import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar
from CTkMessagebox import CTkMessagebox
import datetime
import decimal  # Importação adicionada para lidar com decimais

class TelaCompra:
    def __init__(self, id_usuario):
        self.id_usuario = id_usuario  # ID do usuário logado
        self.carrinho = []  # Lista para armazenar os itens do carrinho
        
        # Configuração da janela principal
        self.janela = ctk.CTk()
        self.janela.title("Sistema de Compras")
        self.janela.geometry("1200x800")
        self.janela.resizable(False, False)
        
        # Configurar tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela, fg_color="transparent")
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        self.criar_interface()
    
    def criar_interface(self):
        # Título
        ctk.CTkLabel(
            self.main_frame, 
            text="Sistema de Compras", 
            font=("Arial", 22, "bold")
        ).pack(pady=(10, 20))
        
        # Frame principal com produtos e carrinho
        content_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        content_frame.pack(fill="both", expand=True)
        
        # Frame de produtos (esquerda)
        produtos_frame = ctk.CTkFrame(content_frame, width=700)
        produtos_frame.pack(side="left", fill="both", expand=True, padx=10)
        
        # Frame de carrinho (direita)
        carrinho_frame = ctk.CTkFrame(content_frame, width=400)
        carrinho_frame.pack(side="right", fill="y", padx=10)
        
        # Frame de pesquisa
        filtros_frame = ctk.CTkFrame(produtos_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Campo de pesquisa
        self.entry_pesquisa = ctk.CTkEntry(
            filtros_frame,
            placeholder_text="Pesquisar produtos...",
            width=400
        )
        self.entry_pesquisa.pack(side="left", expand=True, fill="x")
        
        # Botão de pesquisa
        ctk.CTkButton(
            filtros_frame,
            text="🔍 Pesquisar",
            width=100,
            command=self.pesquisar_produtos
        ).pack(side="left", padx=(10, 0))
        
        # Frame da lista de produtos
        lista_frame = ctk.CTkFrame(produtos_frame)
        lista_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Cabeçalho da lista
        cabecalho_frame = ctk.CTkFrame(lista_frame, fg_color="transparent")
        cabecalho_frame.pack(fill="x", pady=(5, 10))
        
        # Configuração das colunas
        colunas = [
            {"text": "Código", "width": 60, "anchor": "center"},
            {"text": "Produto", "width": 180, "anchor": "w"},
            {"text": "Descrição", "width": 150, "anchor": "w"},
            {"text": "Estoque", "width": 70, "anchor": "center"},
            {"text": "Preço", "width": 90, "anchor": "center"},
            {"text": "Ações", "width": 100, "anchor": "center"}
        ]
        
        for col in colunas:
            ctk.CTkLabel(
                cabecalho_frame,
                text=col["text"],
                font=("Arial", 12, "bold"),
                width=col["width"],
                anchor=col["anchor"]
            ).pack(side="left", padx=2)
        
        # Lista de produtos (scrollable)
        self.lista_produtos_frame = ctk.CTkScrollableFrame(lista_frame, height=350)
        self.lista_produtos_frame.pack(fill="both", expand=True)
        
        # Carrinho de compras
        ctk.CTkLabel(
            carrinho_frame,
            text="🛒 Carrinho de Compras",
            font=("Arial", 16, "bold")
        ).pack(pady=(0, 10))
        
        # Frame da lista do carrinho
        self.carrinho_lista_frame = ctk.CTkScrollableFrame(carrinho_frame, height=300)
        self.carrinho_lista_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Frame do total e ações do carrinho
        carrinho_footer_frame = ctk.CTkFrame(carrinho_frame, fg_color="transparent")
        carrinho_footer_frame.pack(fill="x", pady=(10, 0))
        
        # Label do total
        self.label_total = ctk.CTkLabel(
            carrinho_footer_frame,
            text="Total: R$ 0,00",
            font=("Arial", 16, "bold")
        )
        self.label_total.pack(side="left", expand=True, anchor="w")
        
        # Botão de limpar carrinho
        ctk.CTkButton(
            carrinho_footer_frame,
            text="🗑️ Limpar",
            command=self.limpar_carrinho,
            width=80,
            fg_color="#dc3545"
        ).pack(side="right", padx=5)
        
        # Frame de botões principais
        footer_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        footer_frame.pack(fill="x", padx=40, pady=(10, 0))
        
        # Botões
        btn_frame = ctk.CTkFrame(footer_frame, fg_color="transparent")
        btn_frame.pack(side="right")
        
        ctk.CTkButton(
            btn_frame,
            text="🔄 Atualizar",
            command=self.carregar_produtos,
            width=100,
            fg_color="#17a2b8"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="✅ Finalizar Compra",
            command=self.finalizar_compra,
            width=150,
            fg_color="#28a745"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="📊 Histórico",
            command=self.mostrar_historico,
            width=100,
            fg_color="#6f42c1"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            btn_frame,
            text="🚪 Sair",
            command=self.confirmar_saida,
            width=100,
            fg_color="#dc3545"
        ).pack(side="left", padx=5)
        
        # Carregar produtos
        self.carregar_produtos()
    
    def carregar_produtos(self, filtro=None):
        # Limpar lista atual
        for widget in self.lista_produtos_frame.winfo_children():
            widget.destroy()
        
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
            SELECT p.id_produto, p.nome, p.descricao, p.quantidade, p.preco
            FROM produto p
            WHERE p.quantidade > 0
            """
            
            params = []
            
            if filtro:
                query += " AND (p.nome LIKE %s OR p.descricao LIKE %s)"
                params.extend([f"%{filtro}%", f"%{filtro}%"])
            
            query += " ORDER BY p.nome LIMIT 50"
            
            cursor.execute(query, params)
            produtos = cursor.fetchall()
            
            if not produtos:
                ctk.CTkLabel(
                    self.lista_produtos_frame,
                    text="Nenhum produto encontrado",
                    text_color="gray"
                ).pack(pady=20)
                return
            
            for produto in produtos:
                self.adicionar_item_lista(produto)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def adicionar_item_lista(self, produto):
        item_frame = ctk.CTkFrame(self.lista_produtos_frame, fg_color="transparent")
        item_frame.pack(fill="x", pady=2)
        
        # Armazenar dados do produto no frame para uso posterior
        item_frame.produto_data = {
            'id_produto': produto['id_produto'],
            'nome': produto['nome'],
            'descricao': produto['descricao'],
            'preco': float(produto['preco']),  # Convertendo para float
            'quantidade_disponivel': produto['quantidade']
        }
        
        # Código do produto
        ctk.CTkLabel(
            item_frame,
            text=str(produto['id_produto']),
            width=60,
            anchor="center"
        ).pack(side="left", padx=2)
        
        # Nome do produto
        ctk.CTkLabel(
            item_frame,
            text=produto['nome'],
            width=180,
            anchor="w"
        ).pack(side="left", padx=2)
        
        # Descrição
        ctk.CTkLabel(
            item_frame,
            text=produto['descricao'],
            width=150,
            anchor="w"
        ).pack(side="left", padx=2)
        
        # Quantidade em estoque
        ctk.CTkLabel(
            item_frame,
            text=str(produto['quantidade']),
            width=70,
            anchor="center"
        ).pack(side="left", padx=2)
        
        # Preço unitário
        ctk.CTkLabel(
            item_frame,
            text=f"R$ {float(produto['preco']):.2f}",  # Convertendo para float
            width=90,
            anchor="center"
        ).pack(side="left", padx=2)
        
        # Frame de ações
        acoes_frame = ctk.CTkFrame(item_frame, fg_color="transparent", width=100)
        acoes_frame.pack(side="left", padx=2)
        
        # Botão para adicionar ao carrinho
        ctk.CTkButton(
            acoes_frame,
            text="➕ Adicionar",
            width=90,
            height=24,
            font=("Arial", 10),
            command=lambda p=produto: self.adicionar_ao_carrinho(p)
        ).pack(pady=2)
    
    def adicionar_ao_carrinho(self, produto):
        # Verificar se o produto já está no carrinho
        item_existente = next((item for item in self.carrinho if item['id_produto'] == produto['id_produto']), None)
        
        if item_existente:
            # Se já está no carrinho, apenas aumentar a quantidade se houver estoque
            if item_existente['quantidade'] < produto['quantidade']:
                item_existente['quantidade'] += 1
                item_existente['subtotal'] = float(item_existente['quantidade']) * float(item_existente['preco'])
            else:
                messagebox.showwarning("Aviso", "Quantidade indisponível em estoque!")
        else:
            # Adicionar novo item ao carrinho com quantidade 1
            novo_item = {
                'id_produto': produto['id_produto'],
                'nome': produto['nome'],
                'preco': float(produto['preco']),  # Convertendo para float
                'quantidade': 1,
                'subtotal': float(produto['preco']),  # Convertendo para float
                'quantidade_disponivel': produto['quantidade']
            }
            self.carrinho.append(novo_item)
        
        # Atualizar exibição do carrinho
        self.atualizar_carrinho()
    
    def atualizar_carrinho(self):
        # Limpar carrinho atual
        for widget in self.carrinho_lista_frame.winfo_children():
            widget.destroy()
        
        if not self.carrinho:
            ctk.CTkLabel(
                self.carrinho_lista_frame,
                text="Carrinho vazio",
                text_color="gray"
            ).pack(pady=20)
            self.label_total.configure(text="Total: R$ 0,00")
            return
        
        total_geral = 0.0
        
        for item in self.carrinho:
            item_frame = ctk.CTkFrame(self.carrinho_lista_frame, fg_color="transparent")
            item_frame.pack(fill="x", pady=2)
            
            # Nome do produto e quantidade
            ctk.CTkLabel(
                item_frame,
                text=f"{item['nome']} (x{item['quantidade']})",
                width=200,
                anchor="w"
            ).pack(side="left", padx=2)
            
            # Preço unitário
            ctk.CTkLabel(
                item_frame,
                text=f"R$ {float(item['preco']):.2f}",  # Convertendo para float
                width=80,
                anchor="center"
            ).pack(side="left", padx=2)
            
            # Subtotal
            ctk.CTkLabel(
                item_frame,
                text=f"R$ {float(item['subtotal']):.2f}",  # Convertendo para float
                width=80,
                anchor="center"
            ).pack(side="left", padx=2)
            
            # Frame de ações
            acoes_frame = ctk.CTkFrame(item_frame, fg_color="transparent", width=80)
            acoes_frame.pack(side="left", padx=2)
            
            # Botão para aumentar quantidade
            ctk.CTkButton(
                acoes_frame,
                text="➕",
                width=30,
                height=24,
                font=("Arial", 10),
                command=lambda i=item: self.alterar_quantidade_carrinho(i, 1)
            ).pack(side="left", padx=1)
            
            # Botão para diminuir quantidade
            ctk.CTkButton(
                acoes_frame,
                text="➖",
                width=30,
                height=24,
                font=("Arial", 10),
                command=lambda i=item: self.alterar_quantidade_carrinho(i, -1)
            ).pack(side="left", padx=1)
            
            # Botão para remover
            ctk.CTkButton(
                acoes_frame,
                text="❌",
                width=30,
                height=24,
                font=("Arial", 10),
                fg_color="#dc3545",
                hover_color="#c82333",
                command=lambda i=item: self.remover_do_carrinho(i)
            ).pack(side="left", padx=1)
            
            total_geral += float(item['subtotal'])  # Convertendo para float antes de somar
        
        self.label_total.configure(text=f"Total: R$ {total_geral:,.2f}")
    
    def alterar_quantidade_carrinho(self, item, delta):
        nova_quantidade = item['quantidade'] + delta
        
        # Verificar limites
        if nova_quantidade < 1:
            self.remover_do_carrinho(item)
            return
        
        if nova_quantidade > item['quantidade_disponivel']:
            messagebox.showwarning("Aviso", f"Quantidade indisponível! Máximo: {item['quantidade_disponivel']}")
            return
        
        # Atualizar quantidade
        item['quantidade'] = nova_quantidade
        item['subtotal'] = float(nova_quantidade) * float(item['preco'])  # Convertendo para float
        
        # Atualizar carrinho
        self.atualizar_carrinho()
    
    def remover_do_carrinho(self, item):
        self.carrinho.remove(item)
        self.atualizar_carrinho()
    
    def limpar_carrinho(self):
        self.carrinho = []
        self.atualizar_carrinho()
    
    def pesquisar_produtos(self):
        filtro = self.entry_pesquisa.get()
        self.carregar_produtos(filtro)
    
    def finalizar_compra(self):
        if not self.carrinho:
            messagebox.showwarning("Aviso", "O carrinho está vazio!")
            return
        
        total = sum(float(item['subtotal']) for item in self.carrinho)  # Convertendo para float
        
        # Confirmar compra
        msg = CTkMessagebox(
            title="Confirmar Compra",
            message=f"Confirmar compra de {len(self.carrinho)} itens no valor total de R$ {total:,.2f}?",
            icon="question",
            option_1="Cancelar",
            option_2="Confirmar"
        )
        
        if msg.get() == "Confirmar":
            conn = None
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # 1. Registrar o cabeçalho da compra
                cursor.execute(
                    "INSERT INTO compra (data_compra, total, id_usuario) VALUES (%s, %s, %s)",
                    (datetime.datetime.now(), total, self.id_usuario)
                )
                id_compra = cursor.lastrowid
                
                # 2. Registrar os itens da compra
                for item in self.carrinho:
                    cursor.execute(
                        """INSERT INTO item_compra 
                        (id_compra, id_produto, quantidade, preco_unitario, subtotal) 
                        VALUES (%s, %s, %s, %s, %s)""",
                        (id_compra, item['id_produto'], item['quantidade'], float(item['preco']), float(item['subtotal']))
                    )
                    
                    # 3. Atualizar estoque (aumenta estoque para compras)
                    cursor.execute(
                        """UPDATE produto 
                        SET quantidade = quantidade + %s 
                        WHERE id_produto = %s""",
                        (item['quantidade'], item['id_produto'])
                    )
                
                conn.commit()
                
                CTkMessagebox(
                    title="Sucesso",
                    message=f"Compra #{id_compra} registrada com sucesso!",
                    icon="check"
                )
                
                # Limpar carrinho e recarregar produtos
                self.limpar_carrinho()
                self.carregar_produtos()
                
            except Exception as e:
                if conn:
                    conn.rollback()
                messagebox.showerror("Erro", f"Falha ao registrar compra: {str(e)}")
            finally:
                if conn:
                    conn.close()
    
    def mostrar_historico(self):
        # Janela de histórico
        historico_window = ctk.CTkToplevel(self.janela)
        historico_window.title("Histórico de Compras")
        historico_window.geometry("900x600")
        historico_window.resizable(False, False)
        historico_window.grab_set()  # Modal
        
        # Frame principal
        main_frame = ctk.CTkFrame(historico_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="Histórico de Compras",
            font=("Arial", 18, "bold")
        ).pack(pady=10)
        
        # Frame de filtros
        filtros_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        filtros_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Filtro por data
        ctk.CTkLabel(filtros_frame, text="Data inicial:").pack(side="left", padx=5)
        self.data_inicio_entry = ctk.CTkEntry(filtros_frame, width=120, placeholder_text="AAAA-MM-DD")
        self.data_inicio_entry.pack(side="left", padx=5)
        
        ctk.CTkLabel(filtros_frame, text="Data final:").pack(side="left", padx=5)
        self.data_fim_entry = ctk.CTkEntry(filtros_frame, width=120, placeholder_text="AAAA-MM-DD")
        self.data_fim_entry.pack(side="left", padx=5)
        
        ctk.CTkButton(
            filtros_frame,
            text="Filtrar",
            command=self.filtrar_historico,
            width=80
        ).pack(side="left", padx=10)
        
        # Lista de compras (scrollable)
        self.historico_frame = ctk.CTkScrollableFrame(main_frame, height=400)
        self.historico_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Carregar histórico inicial
        self.carregar_historico()
    
    def carregar_historico(self, data_inicio=None, data_fim=None):
        # Limpar histórico atual
        for widget in self.historico_frame.winfo_children():
            widget.destroy()
        
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        try:
            query = """
            SELECT c.id_compra, c.data_compra, c.total, u.nome as usuario
            FROM compra c
            JOIN usuario u ON c.id_usuario = u.id_usuario
            WHERE 1=1
            """
            
            params = []
            
            if data_inicio and data_fim:
                query += " AND c.data_compra BETWEEN %s AND %s"
                params.extend([data_inicio, data_fim])
            
            query += " ORDER BY c.data_compra DESC LIMIT 50"
            
            cursor.execute(query, params)
            compras = cursor.fetchall()
            
            if not compras:
                ctk.CTkLabel(
                    self.historico_frame,
                    text="Nenhuma compra encontrada",
                    text_color="gray"
                ).pack(pady=20)
                return
            
            for compra in compras:
                self.adicionar_item_historico(compra)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar histórico: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def adicionar_item_historico(self, compra):
        item_frame = ctk.CTkFrame(self.historico_frame)
        item_frame.pack(fill="x", pady=5, padx=5)
        
        # Botão de expansão
        btn_expandir = ctk.CTkButton(
            item_frame,
            text="➕",
            width=30,
            command=lambda c=compra: self.mostrar_detalhes_compra(c['id_compra'])
        )
        btn_expandir.pack(side="left", padx=5)
        
        # Informações básicas
        ctk.CTkLabel(
            item_frame,
            text=f"Compra #{compra['id_compra']}",
            width=100,
            anchor="w"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            item_frame,
            text=compra['data_compra'].strftime("%d/%m/%Y %H:%M"),
            width=150,
            anchor="w"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            item_frame,
            text=f"R$ {float(compra['total']):.2f}",  # Convertendo para float
            width=100,
            anchor="center"
        ).pack(side="left", padx=5)
        
        ctk.CTkLabel(
            item_frame,
            text=compra['usuario'],
            width=150,
            anchor="w"
        ).pack(side="left", padx=5)
    
    def mostrar_detalhes_compra(self, id_compra):
        # Janela de detalhes
        detalhes_window = ctk.CTkToplevel(self.janela)
        detalhes_window.title(f"Detalhes da Compra #{id_compra}")
        detalhes_window.geometry("700x500")
        detalhes_window.resizable(False, False)
        detalhes_window.grab_set()  # Modal
        
        # Frame principal
        main_frame = ctk.CTkFrame(detalhes_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text=f"Detalhes da Compra #{id_compra}",
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Lista de itens (scrollable)
        itens_frame = ctk.CTkScrollableFrame(main_frame, height=300)
        itens_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Cabeçalho
        cabecalho_frame = ctk.CTkFrame(itens_frame, fg_color="transparent")
        cabecalho_frame.pack(fill="x", pady=(0, 5))
        
        colunas = [
            {"text": "Produto", "width": 250},
            {"text": "Quantidade", "width": 100},
            {"text": "Preço Unit.", "width": 100},
            {"text": "Subtotal", "width": 100}
        ]
        
        for col in colunas:
            ctk.CTkLabel(
                cabecalho_frame,
                text=col["text"],
                font=("Arial", 12, "bold"),
                width=col["width"],
                anchor="w"
            ).pack(side="left", padx=2)
        
        # Carregar itens da compra
        conn = conectar()
        cursor = conn.cursor(dictionary=True)
        
        try:
            cursor.execute("""
                SELECT ic.quantidade, ic.preco_unitario, 
                       p.nome as produto_nome, ic.subtotal
                FROM item_compra ic
                JOIN produto p ON ic.id_produto = p.id_produto
                WHERE ic.id_compra = %s
            """, (id_compra,))
            
            itens = cursor.fetchall()
            
            if not itens:
                ctk.CTkLabel(
                    itens_frame,
                    text="Nenhum item encontrado para esta compra",
                    text_color="gray"
                ).pack(pady=20)
                return
            
            for item in itens:
                item_frame = ctk.CTkFrame(itens_frame, fg_color="transparent")
                item_frame.pack(fill="x", pady=2)
                
                ctk.CTkLabel(
                    item_frame,
                    text=item['produto_nome'],
                    width=250,
                    anchor="w"
                ).pack(side="left", padx=2)
                
                ctk.CTkLabel(
                    item_frame,
                    text=str(item['quantidade']),
                    width=100,
                    anchor="w"
                ).pack(side="left", padx=2)
                
                ctk.CTkLabel(
                    item_frame,
                    text=f"R$ {float(item['preco_unitario']):.2f}",  # Convertendo para float
                    width=100,
                    anchor="w"
                ).pack(side="left", padx=2)
                
                ctk.CTkLabel(
                    item_frame,
                    text=f"R$ {float(item['subtotal']):.2f}",  # Convertendo para float
                    width=100,
                    anchor="w"
                ).pack(side="left", padx=2)
                
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar itens: {str(e)}")
        finally:
            if conn:
                conn.close()
    
    def filtrar_historico(self):
        data_inicio = self.data_inicio_entry.get()
        data_fim = self.data_fim_entry.get()
        
        # Validação básica das datas
        try:
            if data_inicio:
                datetime.datetime.strptime(data_inicio, "%Y-%m-%d")
            if data_fim:
                datetime.datetime.strptime(data_fim, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido! Use YYYY-MM-DD")
            return
        
        self.carregar_historico(data_inicio, data_fim)
    
    def confirmar_saida(self):
        msg = CTkMessagebox(
            title="Confirmação",
            message="Deseja realmente sair do sistema de compras?",
            icon="question",
            option_1="Cancelar",
            option_2="Sair"
        )
        
        if msg.get() == "Sair":
            self.janela.destroy()

def abrir_tela_compra(id_usuario):
    app = TelaCompra(id_usuario)
    app.janela.mainloop()

if __name__ == "__main__":
    # Para teste, passe um ID de usuário fictício
    abrir_tela_compra(1)