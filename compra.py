import customtkinter as ctk
from db_config import conectar

def abrir_tela_compra():
    # Configuração da janela principal
    janela = ctk.CTk()
    janela.title("Sistema de Compras")
    janela.geometry("900x600")
    
    # Configurar tema
    ctk.set_appearance_mode("light")
    ctk.set_default_color_theme("green")
    
    # Frame principal
    main_frame = ctk.CTkFrame(janela)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Título
    ctk.CTkLabel(main_frame, text="Produtos Disponíveis", font=("Arial", 18, "bold")).pack(pady=10)
    
    # Frame da lista de produtos
    list_frame = ctk.CTkFrame(main_frame)
    list_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    # Treeview para exibição dos produtos
    colunas = ["ID", "Produto", "Descrição", "Preço", "Estoque", "Ação"]
    tree = ctk.CTkTreeview(list_frame, columns=colunas, show="headings", height=15)
    
    # Configurar colunas
    larguras = [50, 150, 300, 80, 80, 100]
    for col, larg in zip(colunas, larguras):
        tree.heading(col, text=col)
        tree.column(col, width=larg, anchor="center")
    
    # Scrollbar
    scrollbar = ctk.CTkScrollbar(list_frame, command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Layout
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Carregar produtos
    carregar_produtos(tree)
    
    # Frame de compra
    compra_frame = ctk.CTkFrame(main_frame)
    compra_frame.pack(pady=10, fill="x")
    
    ctk.CTkLabel(compra_frame, text="Quantidade:").pack(side="left", padx=5)
    quantidade_entry = ctk.CTkEntry(compra_frame, width=80)
    quantidade_entry.pack(side="left", padx=5)
    
    btn_comprar = ctk.CTkButton(
        compra_frame, 
        text="Adicionar ao Carrinho",
        command=lambda: adicionar_carrinho(tree, quantidade_entry)
    )
    btn_comprar.pack(side="left", padx=10)
    
    # Frame do carrinho
    carrinho_frame = ctk.CTkFrame(main_frame)
    carrinho_frame.pack(pady=10, fill="both", expand=True)
    
    ctk.CTkLabel(carrinho_frame, text="Seu Carrinho", font=("Arial", 14)).pack()
    
    carrinho_tree = ctk.CTkTreeview(carrinho_frame, columns=("Produto", "Quantidade", "Subtotal"), show="headings", height=5)
    for col in ["Produto", "Quantidade", "Subtotal"]:
        carrinho_tree.heading(col, text=col)
        carrinho_tree.column(col, width=200, anchor="center")
    
    carrinho_tree.pack(pady=5, fill="both", expand=True)
    
    # Total da compra
    total_frame = ctk.CTkFrame(main_frame)
    total_frame.pack(pady=5, fill="x")
    
    ctk.CTkLabel(total_frame, text="Total da Compra:").pack(side="left", padx=5)
    total_label = ctk.CTkLabel(total_frame, text="R$ 0,00", font=("Arial", 14, "bold"))
    total_label.pack(side="left")
    
    btn_finalizar = ctk.CTkButton(
        main_frame, 
        text="Finalizar Compra",
        command=lambda: finalizar_compra(carrinho_tree)
    )
    btn_finalizar.pack(pady=10)
    
    janela.mainloop()

def carregar_produtos(tree):
    # Limpar treeview
    for item in tree.get_children():
        tree.delete(item)
    
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
            tree.insert("", "end", values=(
                produto[0],
                produto[1],
                produto[2],
                f"R$ {produto[3]:.2f}",
                produto[4],
                "Comprar"
            ))
    except Exception as e:
        ctk.CTkMessagebox(title="Erro", message=f"Falha ao carregar produtos: {str(e)}", icon="cancel")
    finally:
        conn.close()

def adicionar_carrinho(tree, quantidade_entry):
    item_selecionado = tree.selection()
    if not item_selecionado:
        ctk.CTkMessagebox(title="Aviso", message="Selecione um produto primeiro!", icon="warning")
        return
    
    try:
        quantidade = int(quantidade_entry.get())
        if quantidade <= 0:
            raise ValueError
    except ValueError:
        ctk.CTkMessagebox(title="Erro", message="Quantidade inválida!", icon="cancel")
        return
    
    # Aqui você implementaria a lógica para adicionar ao carrinho
    # Esta é uma implementação básica - você precisará adaptar
    
    # Obter dados do produto selecionado
    valores = tree.item(item_selecionado, "values")
    nome_produto = valores[1]
    preco = float(valores[3].replace("R$ ", ""))
    subtotal = preco * quantidade
    
    # Adicionar ao treeview do carrinho (implementação simplificada)
    carrinho_tree = tree.master.master.master.children["!ctkframe3"].children["!ctktreeview2"]  # Ajuste conforme sua estrutura
    carrinho_tree.insert("", "end", values=(nome_produto, quantidade, f"R$ {subtotal:.2f}"))
    
    # Atualizar total (implementação simplificada)
    total = 0.0
    for item in carrinho_tree.get_children():
        subtotal = float(carrinho_tree.item(item, "values")[2].replace("R$ ", ""))
        total += subtotal
    
    total_label = tree.master.master.master.children["!ctkframe4"].children["!ctklabel3"]  # Ajuste conforme sua estrutura
    total_label.configure(text=f"R$ {total:.2f}")
    
    quantidade_entry.delete(0, "end")

def finalizar_compra(carrinho_tree):
    if not carrinho_tree.get_children():
        ctk.CTkMessagebox(title="Aviso", message="Carrinho vazio!", icon="warning")
        return
    
    # Aqui você implementaria a lógica para finalizar a compra
    # Esta é uma implementação básica - você precisará adaptar
    
    resposta = ctk.CTkMessagebox(
        title="Confirmar Compra",
        message="Deseja finalizar a compra?",
        icon="question",
        option_1="Cancelar",
        option_2="Confirmar"
    )
    
    if resposta.get() == "Confirmar":
        ctk.CTkMessagebox(title="Sucesso", message="Compra realizada com sucesso!", icon="check")
        # Limpar carrinho
        for item in carrinho_tree.get_children():
            carrinho_tree.delete(item)
        # Atualizar total
        total_label = carrinho_tree.master.master.children["!ctkframe4"].children["!ctklabel3"]
        total_label.configure(text="R$ 0,00")
        # Atualizar lista de produtos
        tree = carrinho_tree.master.master.children["!ctkframe2"].children["!ctktreeview1"]
        carregar_produtos(tree)