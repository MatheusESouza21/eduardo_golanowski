import customtkinter as ctk
from db_config import conectar
from CTkMessagebox import CTkMessagebox
import re  # Para validação de CPF

class FuncionarioCRUD:
    def __init__(self):
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Funcionário")
        self.janela.geometry("1000x800")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.abrir()
        self.listar_funcionarios()
    
    def abrir(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # Título
        ctk.CTkLabel(
            self.form_frame, 
            text="Cadastro de Funcionários", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        # Campos do formulário
        self.criar_campos_formulario()
        
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        # Botões de ação
        ctk.CTkButton(
            self.btn_frame, 
            text="Cadastrar", 
            command=self.inserir_funcionario,
            width=120
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Limpar", 
            command=self.limpar_campos,
            fg_color="gray",
            hover_color="darkgray",
            width=120
        ).pack(side="left", padx=5)
        
        # Área de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.list_frame, 
            text="Lista de Funcionários", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)

        # Textbox com scrollbar para exibição
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
        
        # Botão de atualizar
        ctk.CTkButton(
            self.list_frame,
            text="Atualizar Lista",
            command=self.listar_funcionarios
        ).pack(pady=5)
    
    def criar_campos_formulario(self):
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(pady=10, padx=10, fill="x")
        
        # Dicionário para armazenar os campos
        self.campos = {}
        
        # Configuração dos campos
        campos_config = [
            ("nome", "Nome Completo:", 300),
            ("cargo", "Cargo:", 300),
            ("cpf", "CPF:", 150, "000.000.000-00"),
            ("salario", "Salário (R$):", 150, "0.00")
        ]
        
        for idx, (nome, label, largura, *placeholder) in enumerate(campos_config):
            ctk.CTkLabel(campos_frame, text=label).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            
            placeholder_text = placeholder[0] if placeholder else ""
            self.campos[nome] = ctk.CTkEntry(
                campos_frame, 
                width=largura,
                placeholder_text=placeholder_text
            )
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
    
    def validar_cpf(self, cpf):
        # Remove caracteres não numéricos
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Verifica se tem 11 dígitos
        if len(cpf) != 11:
            return False
        
        # Verifica se todos os dígitos são iguais
        if cpf == cpf[0] * 11:
            return False
        
        # Cálculo do primeiro dígito verificador
        soma = 0
        for i in range(9):
            soma += int(cpf[i]) * (10 - i)
        resto = 11 - (soma % 11)
        digito1 = resto if resto < 10 else 0
        
        # Cálculo do segundo dígito verificador
        soma = 0
        for i in range(10):
            soma += int(cpf[i]) * (11 - i)
        resto = 11 - (soma % 11)
        digito2 = resto if resto < 10 else 0
        
        # Verifica se os dígitos calculados conferem
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
    
    def validar_campos(self):
        # Verifica campos obrigatórios
        if not all([
            self.campos["nome"].get(),
            self.campos["cargo"].get(),
            self.campos["cpf"].get(),
            self.campos["salario"].get()
        ]):
            CTkMessagebox(title="Erro", message="Preencha todos os campos obrigatórios!", icon="cancel")
            return False
    
        # Valida CPF
        cpf = self.campos["cpf"].get()
        if not self.validar_cpf(cpf):
            CTkMessagebox(title="Erro", message="CPF inválido!", icon="cancel")
            return False
    
        # Valida salário
        try:
            salario_str = self.campos["salario"].get().replace(",", ".")
            salario = float(salario_str)
            if salario <= 0:
                CTkMessagebox(title="Erro", message="Salário deve ser maior que zero!", icon="cancel")
                return False
        except ValueError:
            CTkMessagebox(title="Erro", message="Salário deve ser um número válido!", icon="cancel")
            return False
    
        return True
    
    def formatar_cpf(self, cpf):
        # Remove tudo que não é dígito
        cpf = re.sub(r'[^0-9]', '', cpf)
        
        # Formata com pontos e traço
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def limpar_campos(self):
        for campo in self.campos.values():
            campo.delete(0, ctk.END)
    
    def listar_funcionarios(self):
        self.textbox.delete("1.0", ctk.END)
    
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
        
            cursor.execute("""
                SELECT id_funcionario, nome, cargo, cpf, salario 
                FROM funcionario
                ORDER BY id_funcionario
            """)
        
            # Cabeçalho
            self.textbox.insert(ctk.END, "ID  | NOME                 | CARGO              | CPF           | SALÁRIO\n")
            self.textbox.insert(ctk.END, "-"*80 + "\n")
        
            # Dados
            for funcionario in cursor.fetchall():
                cpf_formatado = self.formatar_cpf(funcionario[3])
                self.textbox.insert(ctk.END, 
                    f"{funcionario[0]:<4}| {funcionario[1][:20]:<20}| {funcionario[2][:20]:<20}| "
                    f"{cpf_formatado:<14}| R${funcionario[4]:<10.2f}\n"
            )
            
        except Exception as e:
            CTkMessagebox(title="Erro", message="Falha ao carregar funcionários")
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_funcionario(self):
        if not self.validar_campos():
            return
            
        conn = conectar()
        cursor = conn.cursor()
        try:
            # Formata CPF (remove máscara para armazenar)
            cpf = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
            
            cursor.execute("""
                INSERT INTO funcionario (nome, cargo, cpf, salario)
                VALUES (%s, %s, %s, %s)
            """, (
                self.campos["nome"].get(),
                self.campos["cargo"].get(),
                cpf,
                float(self.campos["salario"].get().replace(",", "."))
            ))
            conn.commit()
            CTkMessagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
            
            self.limpar_campos()
            self.listar_funcionarios()
        except Exception as e:
            CTkMessagebox(title="Erro", message="Falha ao inserir funcionário")
        finally:
            conn.close()

def abrir():
    app = FuncionarioCRUD()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()