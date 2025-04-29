import customtkinter as ctk

ctk.set_appearance_mode("System")  # Pode ser "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue")  # Temas disponíveis: "blue", "green", "dark-blue"

root = ctk.CTk()
root.title("Login")
root.geometry("400x350")

# Frame principal
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=40, fill="both", expand=True)

# Título
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
btn_login = ctk.CTkButton(master=frame, text="Entrar")
btn_login.pack(pady=20, padx=10)

# Checkbox para lembrar usuário (opcional)
check_lembrar = ctk.CTkCheckBox(master=frame, text="Lembrar usuário")
check_lembrar.pack(pady=5, padx=10)

root.mainloop()