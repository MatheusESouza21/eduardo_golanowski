import customtkinter as ctk
from db_config import conectar
from tkinter import messagebox

# Configuração do tema
ctk.set_appearance_mode("System")  # "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

def abrir():
    janela = ctk.CTkToplevel()
    janela.title("CRUD - Produto")
    janela.geometry("800x700")
    
    # Frame principal
    main_frame = ctk.CTkFrame(master=janela)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Frame do formulário
    form_frame = ctk.CTkFrame(master=main_frame)
    form_frame.pack(pady=10, padx=10, fill="x")

    def listar_produtos():
        # Limpa o texto atual
        textbox.delete("1.0", ctk.END)
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT p.id, p.nome, p.descricao, p.quantidade, 
                       p.preco, f.nome as fornecedor
                FROM produto p
                LEFT JOIN fornecedor f ON p.id_fornecedor = f.id
                ORDER BY p.id
            """)
            
            # Cabeçalho
            textbox.insert(ctk.END, "ID  | NOME                | DESCRIÇÃO          | QTD | PREÇO   | FORNECEDOR\n")
            textbox.insert(ctk.END, "-"*90 + "\n")
            
            # Dados
            for produto in cursor.fetchall():
                textbox.insert(ctk.END, 
                    f"{produto[0]:<4}| {produto[1][:20]:<20}| {produto[2][:20]:<20}| "
                    f"{produto[3]:<4}| R${produto[4]:<7.2f}| {produto[5] or 'N/D'}\n"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar produtos: {str(e)}")
        finally:
            conn.close()

    def inserir_produto():
        # Validação dos campos
        if not all([
            entry_nome.get(),
            entry_quantidade.get().isdigit(),
            entry_preco.get().replace('.', '').isdigit(),
            entry_id_fornecedor.get().isdigit()
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return
            
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO produto (nome, descricao, quantidade, preco, id_fornecedor)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                entry_nome.get(),
                entry_descricao.get(),
                int(entry_quantidade.get()),
                float(entry_preco.get()),
                int(entry_id_fornecedor.get())
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Produto cadastrado com sucesso!")
            
            # Limpa os campos
            entry_nome.delete(0, ctk.END)
            entry_descricao.delete(0, ctk.END)
            entry_quantidade.delete(0, ctk.END)
            entry_preco.delete(0, ctk.END)
            entry_id_fornecedor.delete(0, ctk.END)
            
            # Atualiza a lista
            listar_produtos()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir produto: {str(e)}")
        finally:
            conn.close()

    # Widgets do formulário
    ctk.CTkLabel(form_frame, text="Cadastro de Produtos", font=("Arial", 14, "bold")).pack(pady=5)

    # Grid de campos
    campos_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    campos_frame.pack(pady=10, padx=10, fill="x")

    # Nome
    ctk.CTkLabel(campos_frame, text="Nome:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nome = ctk.CTkEntry(campos_frame, width=300)
    entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Descrição
    ctk.CTkLabel(campos_frame, text="Descrição:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_descricao = ctk.CTkEntry(campos_frame, width=300)
    entry_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # Quantidade
    ctk.CTkLabel(campos_frame, text="Quantidade:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_quantidade = ctk.CTkEntry(campos_frame, width=100)
    entry_quantidade.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Preço
    ctk.CTkLabel(campos_frame, text="Preço (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_preco = ctk.CTkEntry(campos_frame, width=100)
    entry_preco.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Fornecedor
    ctk.CTkLabel(campos_frame, text="ID Fornecedor:").grid(row=4, column=0, padx=5, pady=5, sticky="e")
    entry_id_fornecedor = ctk.CTkEntry(campos_frame, width=100)
    entry_id_fornecedor.grid(row=4, column=1, padx=5, pady=5, sticky="w")

    # Botão de inserir
    btn_inserir = ctk.CTkButton(form_frame, text="Inserir Produto", command=inserir_produto)
    btn_inserir.pack(pady=10)

    # Área de listagem
    list_frame = ctk.CTkFrame(main_frame)
    list_frame.pack(pady=10, padx=10, fill="both", expand=True)

    ctk.CTkLabel(list_frame, text="Lista de Produtos", font=("Arial", 14, "bold")).pack(pady=5)

    # Textbox com scrollbar para exibição
    scrollbar = ctk.CTkScrollbar(list_frame)
    scrollbar.pack(side="right", fill="y")

    textbox = ctk.CTkTextbox(
        list_frame, 
        yscrollcommand=scrollbar.set,
        font=("Courier New", 12),  # Fonte monoespaçada para alinhamento
        wrap="none"
    )
    textbox.pack(pady=5, padx=5, fill="both", expand=True)

    scrollbar.configure(command=textbox.yview)

    # Carrega os produtos inicialmente
    listar_produtos()