import customtkinter as ctk
from db_config import conectar
from CTkMessagebox import CTkMessagebox
import re
from tkinter import ttk  # Importação para o Treeview tradicional

class FuncionarioCRUD:
    def __init__(self):
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Funcionário")
        self.janela.geometry("1000x800")
        self.janela.resizable(False, False)
        
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        self.criar_interface()
        self.listar_funcionarios()
    
    def criar_interface(self):
        # Frame principal
        self.main_frame = ctk.CTkFrame(self.janela)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        # Frame do formulário
        self.form_frame = ctk.CTkFrame(self.main_frame)
        self.form_frame.pack(pady=10, padx=10, fill="x")

        # Título
        ctk.CTkLabel(self.form_frame, text="Cadastro de Funcionários", font=("Arial", 14, "bold")).pack(pady=5)

        # Campos do formulário
        self.criar_campos_formulario()
        
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=10)
        
        # Botões de ação
        ctk.CTkButton(self.btn_frame, text="Cadastrar", command=self.inserir_funcionario, width=120).pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="Atualizar", command=self.atualizar_funcionario, width=120, fg_color="#17a2b8").pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="Excluir", command=self.excluir_funcionario, width=120, fg_color="#dc3545").pack(side="left", padx=5)
        ctk.CTkButton(self.btn_frame, text="Limpar", command=self.limpar_campos, width=120, fg_color="#6c757d").pack(side="left", padx=5)
        
        # Área de listagem com Treeview
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(self.list_frame, text="Lista de Funcionários", font=("Arial", 14, "bold")).pack(pady=5)

        # Treeview do ttk
        self.tree = ttk.Treeview(self.list_frame, columns=("ID", "Nome", "Cargo", "CPF", "Salário"), show="headings", height=20)
        
        # Configurar colunas
        colunas = [
            ("ID", 50),
            ("Nome", 200),
            ("Cargo", 150),
            ("CPF", 150),
            ("Salário", 100)
        ]
        
        for col, width in colunas:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=width, anchor="center")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar seleção
        self.tree.bind("<<TreeviewSelect>>", self.carregar_dados_selecionados)
        
        # Estilização do Treeview
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", 
                       background="#2a2d2e",
                       foreground="white",
                       rowheight=25,
                       fieldbackground="#2a2d2e",
                       bordercolor="#343638",
                       borderwidth=0)
        style.map('Treeview', background=[('selected', '#22559b')])
        style.configure("Treeview.Heading",
                       background="#565b5e",
                       foreground="white",
                       relief="flat")
        style.map("Treeview.Heading",
                 background=[('active', '#3484F0')])
        
        # Botão de atualizar
        ctk.CTkButton(self.list_frame, text="Atualizar Lista", command=self.listar_funcionarios).pack(pady=5)
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, "values")
            self.limpar_campos()
            self.campos["nome"].insert(0, values[1])
            self.campos["cargo"].insert(0, values[2])
            self.campos["cpf"].insert(0, values[3])
            self.campos["salario"].insert(0, values[4].replace("R$", "").strip())
    
    def criar_campos_formulario(self):
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(pady=10, padx=10, fill="x")
        
        self.campos = {}
        campos_config = [
            ("nome", "Nome Completo:", 300),
            ("cargo", "Cargo:", 300),
            ("cpf", "CPF:", 150, "000.000.000-00"),
            ("salario", "Salário (R$):", 150, "0.00")
        ]
        
        for idx, (nome, label, largura, *placeholder) in enumerate(campos_config):
            ctk.CTkLabel(campos_frame, text=label).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            placeholder_text = placeholder[0] if placeholder else ""
            self.campos[nome] = ctk.CTkEntry(campos_frame, width=largura, placeholder_text=placeholder_text)
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
    
    def validar_cpf(self, cpf):
        cpf = re.sub(r'[^0-9]', '', cpf)
        if len(cpf) != 11 or cpf == cpf[0] * 11:
            return False
        
        # Cálculo dos dígitos verificadores
        for i in range(9, 11):
            soma = sum(int(cpf[num]) * (i+1-num) for num in range(0, i))
            digito = 11 - (soma % 11)
            if int(cpf[i]) != (0 if digito > 9 else digito):
                return False
        return True
    
    def validar_campos(self):
        if not all([self.campos["nome"].get(), self.campos["cargo"].get(), 
                   self.campos["cpf"].get(), self.campos["salario"].get()]):
            CTkMessagebox(title="Erro", message="Preencha todos os campos!", icon="cancel")
            return False
        
        if not self.validar_cpf(self.campos["cpf"].get()):
            CTkMessagebox(title="Erro", message="CPF inválido!", icon="cancel")
            return False
        
        try:
            salario = float(self.campos["salario"].get().replace(",", "."))
            if salario <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(title="Erro", message="Salário deve ser positivo!", icon="cancel")
            return False
        
        return True
    
    def formatar_cpf(self, cpf):
        cpf = re.sub(r'[^0-9]', '', cpf)
        return f"{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}"
    
    def limpar_campos(self):
        for campo in self.campos.values():
            campo.delete(0, "end")
    
    def listar_funcionarios(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cursor.execute("SELECT id_funcionario, nome, cargo, cpf, salario FROM funcionario ORDER BY nome")
            
            for funcionario in cursor.fetchall():
                self.tree.insert("", "end", values=(
                    funcionario[0],
                    funcionario[1],
                    funcionario[2],
                    self.formatar_cpf(funcionario[3]),
                    f"R$ {funcionario[4]:.2f}"
                ))
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao carregar:\n{str(e)}", icon="cancel")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def get_selected_id(self):
        selected = self.tree.selection()
        return self.tree.item(selected, "values")[0] if selected else None
    
    def inserir_funcionario(self):
        if not self.validar_campos():
            return
            
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
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
            CTkMessagebox(title="Sucesso", message="Funcionário cadastrado!", icon="check")
            self.limpar_campos()
            self.listar_funcionarios()
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao inserir:\n{str(e)}", icon="cancel")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def atualizar_funcionario(self):
        funcionario_id = self.get_selected_id()
        if not funcionario_id:
            CTkMessagebox(title="Aviso", message="Selecione um funcionário!", icon="warning")
            return
            
        if not self.validar_campos():
            return
            
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            cpf = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
            
            cursor.execute("""
                UPDATE funcionario 
                SET nome=%s, cargo=%s, cpf=%s, salario=%s
                WHERE id_funcionario=%s
            """, (
                self.campos["nome"].get(),
                self.campos["cargo"].get(),
                cpf,
                float(self.campos["salario"].get().replace(",", ".")),
                funcionario_id
            ))
            conn.commit()
            CTkMessagebox(title="Sucesso", message="Dados atualizados!", icon="check")
            self.listar_funcionarios()
        except Exception as e:
            CTkMessagebox(title="Erro", message=f"Falha ao atualizar:\n{str(e)}", icon="cancel")
        finally:
            if cursor: cursor.close()
            if conn: conn.close()
    
    def excluir_funcionario(self):
        funcionario_id = self.get_selected_id()
        if not funcionario_id:
            CTkMessagebox(title="Aviso", message="Selecione um funcionário!", icon="warning")
            return
            
        confirm = CTkMessagebox(
            title="Confirmação",
            message=f"Excluir funcionário ID {funcionario_id}?",
            icon="question",
            option_1="Cancelar",
            option_2="Excluir"
        )
        
        if confirm.get() == "Excluir":
            conn = None
            cursor = None
            try:
                conn = conectar()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM funcionario WHERE id_funcionario = %s", (funcionario_id,))
                conn.commit()
                CTkMessagebox(title="Sucesso", message="Funcionário excluído!", icon="check")
                self.limpar_campos()
                self.listar_funcionarios()
            except Exception as e:
                CTkMessagebox(title="Erro", message=f"Falha ao excluir:\n{str(e)}", icon="cancel")
            finally:
                if cursor: cursor.close()
                if conn: conn.close()

def abrir():
    app = FuncionarioCRUD()
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()