import customtkinter as ctk
from tkinter import messagebox
from db_config import conectar
from compra import abrir_tela_compra
from admin_crud import abrir_menu_admin

# Configuração do tema
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def verificar_login(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT status FROM usuario WHERE nome = %s AND senha = %s", (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

def criar_usuario(nome, senha, status="comum"):
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuario (nome, senha, status) VALUES (%s, %s, %s)", 
                      (nome, senha, status))
        conn.commit()
        return True
    except Exception as e:
        messagebox.showerror("Erro", f"Não foi possível criar usuário: {str(e)}")
        return False
    finally:
        conn.close()

def abrir_janela_cadastro():
    janela_cadastro = ctk.CTkToplevel(root)
    janela_cadastro.title("Criar Nova Conta")
    janela_cadastro.geometry("400x350")
    
    frame_cadastro = ctk.CTkFrame(master=janela_cadastro)
    frame_cadastro.pack(pady=20, padx=40, fill="both", expand=True)
    
    ctk.CTkLabel(frame_cadastro, text="Criar Nova Conta", font=("Roboto", 20)).pack(pady=12)
    
    # Campos do formulário
    ctk.CTkLabel(frame_cadastro, text="Novo Usuário").pack(pady=(5, 0))
    novo_usuario = ctk.CTkEntry(frame_cadastro)
    novo_usuario.pack(pady=5)
    
    ctk.CTkLabel(frame_cadastro, text="Senha").pack(pady=(5, 0))
    nova_senha = ctk.CTkEntry(frame_cadastro, show="*")
    nova_senha.pack(pady=5)
    
    ctk.CTkLabel(frame_cadastro, text="Confirmar Senha").pack(pady=(5, 0))
    confirmar_senha = ctk.CTkEntry(frame_cadastro, show="*")
    confirmar_senha.pack(pady=5)
    
    def finalizar_cadastro():
        if nova_senha.get() != confirmar_senha.get():
            messagebox.showerror("Erro", "As senhas não coincidem!")
            return
            
        if criar_usuario(novo_usuario.get(), nova_senha.get()):
            messagebox.showinfo("Sucesso", "Conta criada com sucesso!")
            janela_cadastro.destroy()
    
    ctk.CTkButton(frame_cadastro, text="Criar Conta", command=finalizar_cadastro).pack(pady=20)

def login():
    usuario = entry_usuario.get()
    senha = entry_senha.get()
    status = verificar_login(usuario, senha)

    if status == "comum":
        root.destroy()
        abrir_tela_compra()
    elif status == "administrador":
        root.destroy()
        abrir_menu_admin()
    else:
        messagebox.showerror("Erro", "Usuário ou senha inválidos")

root = ctk.CTk()
root.title("Login")
root.geometry("400x400")  # Aumentei a altura para acomodar o novo botão

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=40, fill="both", expand=True)

label_titulo = ctk.CTkLabel(master=frame, text="Sistema de Login", font=("Roboto", 24))
label_titulo.pack(pady=12, padx=10)

# Campo de usuário
label_usuario = ctk.CTkLabel(master=frame, text="Usuário", font=("Roboto", 12))
label_usuario.pack(pady=(10, 0))
entry_usuario = ctk.CTkEntry(master=frame, placeholder_text="Digite seu usuário")
entry_usuario.pack(pady=5, padx=10)

# Campo de senha
label_senha = ctk.CTkLabel(master=frame, text="Senha", font=("Roboto", 12))
label_senha.pack(pady=(10, 0))
entry_senha = ctk.CTkEntry(master=frame, placeholder_text="Digite sua senha", show="*")
entry_senha.pack(pady=5, padx=10)

# Botão de login
btn_login = ctk.CTkButton(master=frame, text="Entrar", command=login)
btn_login.pack(pady=10, padx=10)

# Botão de criar conta
btn_criar_conta = ctk.CTkButton(master=frame, text="Criar Nova Conta", 
                               fg_color="transparent", border_width=2,
                               text_color=("gray10", "#DCE4EE"),
                               command=abrir_janela_cadastro)
btn_criar_conta.pack(pady=5, padx=10)

# Checkbox para lembrar usuário
check_lembrar = ctk.CTkCheckBox(master=frame, text="Lembrar usuário")
check_lembrar.pack(pady=5, padx=10)

root.mainloop()