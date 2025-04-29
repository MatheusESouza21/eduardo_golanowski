import customtkinter as ctk
from db_config import conectar
import tkinter.messagebox as messagebox

# Configuração do tema
ctk.set_appearance_mode("System")  # "Light", "Dark" ou "System"
ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"

def abrir():
    janela = ctk.CTkToplevel()
    janela.title("CRUD - Funcionário")
    janela.geometry("900x700")
    
    # Frame principal
    main_frame = ctk.CTkFrame(master=janela)
    main_frame.pack(pady=20, padx=20, fill="both", expand=True)
    
    # Frame do formulário
    form_frame = ctk.CTkFrame(master=main_frame)
    form_frame.pack(pady=10, padx=10, fill="x")

    def listar_funcionarios():
        # Limpa o texto atual
        textbox.delete("1.0", ctk.END)
        
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                SELECT id, nome, cargo, cpf, salario 
                FROM funcionario
                ORDER BY nome
            """)
            
            # Cabeçalho
            textbox.insert(ctk.END, "ID  | NOME                 | CARGO              | CPF           | SALÁRIO\n")
            textbox.insert(ctk.END, "-"*80 + "\n")
            
            # Dados
            for funcionario in cursor.fetchall():
                textbox.insert(ctk.END, 
                    f"{funcionario[0]:<4}| {funcionario[1][:20]:<20}| {funcionario[2][:20]:<20}| "
                    f"{funcionario[3]:<14}| R${funcionario[4]:<10.2f}\n"
                )
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao carregar funcionários: {str(e)}")
        finally:
            conn.close()

    def inserir_funcionario():
        # Validação dos campos
        if not all([
            entry_nome.get(),
            entry_cargo.get(),
            entry_cpf.get(),
            entry_salario.get().replace('.', '').isdigit()
        ]):
            messagebox.showerror("Erro", "Preencha todos os campos corretamente!")
            return
            
        conn = conectar()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO funcionario (nome, cargo, cpf, salario)
                VALUES (%s, %s, %s, %s)
            """, (
                entry_nome.get(),
                entry_cargo.get(),
                entry_cpf.get(),
                float(entry_salario.get())
            ))
            conn.commit()
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            
            # Limpa os campos
            entry_nome.delete(0, ctk.END)
            entry_cargo.delete(0, ctk.END)
            entry_cpf.delete(0, ctk.END)
            entry_salario.delete(0, ctk.END)
            
            # Atualiza a lista
            listar_funcionarios()
        except Exception as e:
            messagebox.showerror("Erro", f"Falha ao inserir funcionário: {str(e)}")
        finally:
            conn.close()

    # Widgets do formulário
    ctk.CTkLabel(form_frame, text="Cadastro de Funcionários", font=("Arial", 14, "bold")).pack(pady=5)

    # Grid de campos
    campos_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
    campos_frame.pack(pady=10, padx=10, fill="x")

    # Nome
    ctk.CTkLabel(campos_frame, text="Nome Completo:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
    entry_nome = ctk.CTkEntry(campos_frame, width=300)
    entry_nome.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # Cargo
    ctk.CTkLabel(campos_frame, text="Cargo:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
    entry_cargo = ctk.CTkEntry(campos_frame, width=300)
    entry_cargo.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # CPF
    ctk.CTkLabel(campos_frame, text="CPF:").grid(row=2, column=0, padx=5, pady=5, sticky="e")
    entry_cpf = ctk.CTkEntry(campos_frame, width=150, placeholder_text="000.000.000-00")
    entry_cpf.grid(row=2, column=1, padx=5, pady=5, sticky="w")

    # Salário
    ctk.CTkLabel(campos_frame, text="Salário (R$):").grid(row=3, column=0, padx=5, pady=5, sticky="e")
    entry_salario = ctk.CTkEntry(campos_frame, width=150, placeholder_text="0.00")
    entry_salario.grid(row=3, column=1, padx=5, pady=5, sticky="w")

    # Botão de inserir
    btn_inserir = ctk.CTkButton(form_frame, text="Cadastrar Funcionário", command=inserir_funcionario)
    btn_inserir.pack(pady=10)

    # Área de listagem
    list_frame = ctk.CTkFrame(main_frame)
    list_frame.pack(pady=10, padx=10, fill="both", expand=True)

    ctk.CTkLabel(list_frame, text="Lista de Funcionários", font=("Arial", 14, "bold")).pack(pady=5)

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

    # Carrega os funcionários inicialmente
    listar_funcionarios()