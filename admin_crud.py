import customtkinter as ctk
import crud_usuario
import crud_fornecedor
import crud_produto
import crud_funcionario

def abrir_menu_admin():
    # Configuração da janela principal
    janela = ctk.CTk()
    janela.title("Painel Administrativo")
    janela.geometry("500x400")
    
    # Configurar tema
    ctk.set_appearance_mode("dark")  # Pode ser "light", "dark" ou "system"
    ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
    
    # Frame principal
    main_frame = ctk.CTkFrame(janela, fg_color="transparent")
    main_frame.pack(pady=40, padx=40, fill="both", expand=True)
    
    # Título
    ctk.CTkLabel(
        main_frame, 
        text="Menu Administrativo", 
        font=("Arial", 20, "bold")
    ).pack(pady=(0, 30))
    
    # Frame dos botões
    btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
    btn_frame.pack(fill="x")
    
    # Botões de CRUD
    botoes = [
        ("CRUD Usuários", crud_usuario.abrir),
        ("CRUD Fornecedores", crud_fornecedor.abrir),
        ("CRUD Produtos", crud_produto.abrir),
        ("CRUD Funcionários", crud_funcionario.abrir)
    ]
    
    for texto, comando in botoes:
        btn = ctk.CTkButton(
            btn_frame,
            text=texto,
            command=comando,
            height=40,
            font=("Arial", 14)
        )
        btn.pack(pady=10, fill="x")
    
    # Botão de sair
    ctk.CTkButton(
        main_frame,
        text="Sair",
        command=janela.destroy,
        fg_color="transparent",
        border_width=2,
        text_color=("gray10", "#DCE4EE"),
        height=40
    ).pack(pady=(20, 0), fill="x")
    
    janela.mainloop()