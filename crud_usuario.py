import customtkinter as ctk
from db_config import conectar

# Configuração do tema
ctk.set_appearance_mode("System")  # Pode ser "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue")  # Temas disponíveis: "blue", "green", "dark-blue"

def abrir():
    janela = ctk.CTkToplevel()
    janela.title("CRUD - Usuário")
    janela.geometry("600x500")
    
    # Frame principal
    frame = ctk.CTkFrame(master=janela)
    frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Frame de formulário
    form_frame = ctk.CTkFrame(master=frame)
    form_frame.pack(pady=10, padx=10, fill="x")

    def listar():
        lista.delete(0, ctk.END)
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT id, nome, status FROM usuario")
        for linha in cursor.fetchall():
            lista.insert(ctk.END, f"ID: {linha[0]} - Nome: {linha[1]} - Status: {linha[2]}")
        conn.close()

    def inserir():
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO usuario (nome, senha, status) VALUES (%s, %s, %s)",
                         (entry_nome.get(), entry_senha.get(), combo_status.get()))
            conn.commit()
            ctk.CTkMessagebox(title="Sucesso", message="Usuário cadastrado com sucesso!", icon="check")
            listar()
            # Limpa os campos após inserção
            entry_nome.delete(0, ctk.END)
            entry_senha.delete(0, ctk.END)
            combo_status.set("comum")
        except Exception as e:
            ctk.CTkMessagebox(title="Erro", message=f"Falha ao inserir usuário: {str(e)}", icon="cancel")
        finally:
            conn.close()

    # Campos do formulário
    ctk.CTkLabel(form_frame, text="Nome:").pack(pady=(5, 0))
    entry_nome = ctk.CTkEntry(form_frame, placeholder_text="Digite o nome do usuário")
    entry_nome.pack(pady=5, padx=10, fill="x")

    ctk.CTkLabel(form_frame, text="Senha:").pack(pady=(5, 0))
    entry_senha = ctk.CTkEntry(form_frame, placeholder_text="Digite a senha", show="*")
    entry_senha.pack(pady=5, padx=10, fill="x")

    ctk.CTkLabel(form_frame, text="Status:").pack(pady=(5, 0))
    combo_status = ctk.CTkComboBox(form_frame, values=["comum", "administrador"])
    combo_status.set("comum")
    combo_status.pack(pady=5, padx=10, fill="x")

    # Botões de ação
    btn_frame = ctk.CTkFrame(master=frame, fg_color="transparent")
    btn_frame.pack(pady=10)
    
    ctk.CTkButton(btn_frame, text="Inserir", command=inserir).pack(side="left", padx=5)
    
    # Lista de usuários
    lista_frame = ctk.CTkFrame(master=frame)
    lista_frame.pack(pady=10, padx=10, fill="both", expand=True)
    
    scrollbar = ctk.CTkScrollbar(lista_frame)
    scrollbar.pack(side="right", fill="y")
    
    lista = ctk.CTkTextbox(lista_frame, yscrollcommand=scrollbar.set, wrap="none")
    lista.pack(pady=5, padx=5, fill="both", expand=True)
    
    scrollbar.configure(command=lista.yview)
    
    # Carrega a lista inicial
    listar()
