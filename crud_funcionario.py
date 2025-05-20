import customtkinter as ctk
from tkinter import ttk
from db_config import conectar
from CTkMessagebox import CTkMessagebox
import re

class FuncionarioCRUD:
    def __init__(self, admin_menu=None):
        self.admin_menu = admin_menu
        self.janela = ctk.CTkToplevel()
        self.janela.title("CRUD - Funcionário")
        self.janela.geometry("1000x700")
        self.janela.resizable(False, False)
        
        # Configuração do tema
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")
        
        # Variável para controle da ordenação
        self.ordenacao = {
            'coluna': 'id_funcionario',
            'direcao': 'ASC'
        }
        
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
        ctk.CTkLabel(
            self.form_frame, 
            text="Cadastro de Funcionários", 
            font=("Arial", 16, "bold")
        ).pack(pady=10)
        
        # Campos do formulário
        self.criar_campos_formulario()
        
        # Frame de botões
        self.btn_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        self.btn_frame.pack(pady=15)

        # Frame inferior para o botão Voltar
        self.bottom_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.bottom_frame.pack(pady=5, padx=10, fill="x")
        
        # Botões de ação
        ctk.CTkButton(
            self.btn_frame, 
            text="Cadastrar", 
            command=self.inserir_funcionario,
            width=120,
            fg_color="#28a745",
            hover_color="#218838"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Atualizar", 
            command=self.atualizar_funcionario,
            width=120,
            fg_color="#17a2b8",
            hover_color="#138496"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Excluir", 
            command=self.excluir_funcionario,
            width=120,
            fg_color="#dc3545",
            hover_color="#c82333"
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            self.btn_frame, 
            text="Limpar", 
            command=self.limpar_campos,
            width=120,
            fg_color="#6c757d",
            hover_color="#5a6268"
        ).pack(side="left", padx=5)

        # Botão Voltar ao Admin
        ctk.CTkButton(
            self.bottom_frame,
            text="Voltar ao Admin",
            command=self.voltar_admin,
            fg_color="transparent",
            border_width=1,
            border_color="#6c757d",
            text_color="#6c757d",
            hover_color="#f8f9fa",
            width=120
        ).pack(side="right", padx=5)
        
        # Área de listagem
        self.list_frame = ctk.CTkFrame(self.main_frame)
        self.list_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        ctk.CTkLabel(
            self.list_frame, 
            text="Lista de Funcionários", 
            font=("Arial", 14, "bold")
        ).pack(pady=5)
        
        # Treeview para exibição
        self.tree = ttk.Treeview(
            self.list_frame,
            columns=("ID", "Nome", "Cargo", "CPF", "Salário"),
            show="headings",
            height=15,
            selectmode="browse"
        )
        
        # Configurar colunas com bind para ordenação
        colunas = [
            ("ID", 50, "center", "id_funcionario"),
            ("Nome", 250, "w", "nome"),
            ("Cargo", 150, "w", "cargo"),
            ("CPF", 150, "center", "cpf"),
            ("Salário", 150, "center", "salario")
        ]
        
        for col, width, anchor, coluna_db in colunas:
            self.tree.heading(col, text=col, 
                            command=lambda c=coluna_db: self.ordenar_por_coluna(c))
            self.tree.column(col, width=width, anchor=anchor)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            self.list_frame, 
            orient="vertical", 
            command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Layout
        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Configurar seleção
        self.tree.bind("<<TreeviewSelect>>", self.carregar_dados_selecionados)
        
        # Estilização do Treeview
        self.configurar_estilo_treeview()
        
        # Botão de atualizar lista
        ctk.CTkButton(
            self.list_frame,
            text="Atualizar Lista",
            command=self.listar_funcionarios,
            width=120
        ).pack(pady=10)

    def voltar_admin(self):
        """Fecha a janela atual e reabre o menu admin"""
        self.janela.destroy()
        if self.admin_menu:
            self.admin_menu.janela.deiconify()
    
    def configurar_estilo_treeview(self):
        style = ttk.Style()
        style.theme_use("default")
        
        style.configure("Treeview",
            background="#2b2b2b",
            foreground="white",
            rowheight=25,
            fieldbackground="#2b2b2b",
            bordercolor="#343638",
            borderwidth=0
        )
        style.map('Treeview', background=[('selected', '#3b8ed0')])
        
        style.configure("Treeview.Heading",
            background="#565b5e",
            foreground="white",
            relief="flat",
            font=('Arial', 10, 'bold')
        )
        style.map("Treeview.Heading",
            background=[('active', '#3484F0')],
            relief=[('pressed', 'sunken'), ('!pressed', 'raised')]
        )
    
    def criar_campos_formulario(self):
        # Frame para os campos
        campos_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        campos_frame.pack(fill="x", padx=10, pady=5)
        
        # Dicionário para armazenar os campos
        self.campos = {}
        
        # Configuração dos campos
        campos_config = [
            ("nome", "Nome Completo:", 300),
            ("cargo", "Cargo:", 300),
            ("cpf", "CPF:", 150, "000.000.000-00"),
            ("salario", "Salário (R$):", 150, "0,00")
        ]
        
        # Criar campos dinamicamente
        for idx, (nome, label, largura, *placeholder) in enumerate(campos_config):
            # Label
            ctk.CTkLabel(
                campos_frame, 
                text=label,
                font=("Arial", 12)
            ).grid(row=idx, column=0, padx=5, pady=5, sticky="e")
            
            # Entry
            placeholder_text = placeholder[0] if placeholder else ""
            self.campos[nome] = ctk.CTkEntry(
                campos_frame,
                width=largura,
                placeholder_text=placeholder_text,
                font=("Arial", 12)
            )
            
            # Posicionamento
            self.campos[nome].grid(row=idx, column=1, padx=5, pady=5, sticky="w")
            
            # Bind para formatação automática do CPF
            if nome == "cpf":
                self.campos[nome].bind("<KeyRelease>", self.formatar_cpf_digitacao)
            elif nome == "salario":
                self.campos[nome].bind("<KeyRelease>", self.formatar_salario_digitacao)
    
    def formatar_cpf_digitacao(self, event):
        # Pega o texto atual sem formatação
        texto = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
        
        # Aplica a máscara
        formatado = ""
        if len(texto) > 0:
            formatado = texto[:3]
        if len(texto) > 3:
            formatado += "." + texto[3:6]
        if len(texto) > 6:
            formatado += "." + texto[6:9]
        if len(texto) > 9:
            formatado += "-" + texto[9:11]
        
        # Atualiza o campo
        self.campos["cpf"].delete(0, "end")
        self.campos["cpf"].insert(0, formatado)
    
    def formatar_salario_digitacao(self, event):
        texto = re.sub(r'[^0-9]', '', self.campos["salario"].get())
        
        if texto:
            try:
                # Converte para float e formata com 2 casas decimais
                valor = float(texto) / 100
                formatado = f"{valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                self.campos["salario"].delete(0, "end")
                self.campos["salario"].insert(0, formatado)
            except:
                pass
    
    def ordenar_por_coluna(self, coluna):
        """Ordena os dados pela coluna clicada"""
        # Alterna a direção se clicar na mesma coluna
        if self.ordenacao['coluna'] == coluna:
            self.ordenacao['direcao'] = 'DESC' if self.ordenacao['direcao'] == 'ASC' else 'ASC'
        else:
            self.ordenacao['coluna'] = coluna
            self.ordenacao['direcao'] = 'ASC'
        
        self.listar_funcionarios()
    
    def validar_cpf(self, cpf):
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
        
        # Verifica se os dígitos calculados conferem com os informados
        return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
    
    def validar_campos(self):
        # Verifica campos vazios
        if not all(self.campos[campo].get() for campo in self.campos):
            CTkMessagebox(
                title="Erro", 
                message="Preencha todos os campos!", 
                icon="cancel"
            )
            return False
        
        # Valida CPF
        cpf = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
        if not self.validar_cpf(cpf):
            CTkMessagebox(
                title="Erro", 
                message="CPF inválido!", 
                icon="cancel"
            )
            return False
        
        # Valida salário
        try:
            salario = float(
                self.campos["salario"].get()
                .replace(".", "")
                .replace(",", ".")
            )
            if salario <= 0:
                raise ValueError
        except ValueError:
            CTkMessagebox(
                title="Erro", 
                message="Salário deve ser um valor positivo!", 
                icon="cancel"
            )
            return False
        
        return True
    
    def limpar_campos(self):
        for campo in self.campos.values():
            campo.delete(0, "end")
    
    def carregar_dados_selecionados(self, event):
        selected = self.tree.selection()
        if selected:
            values = self.tree.item(selected, "values")
            self.limpar_campos()
            
            # Preenche os campos com os dados selecionados
            self.campos["nome"].insert(0, values[1])
            self.campos["cargo"].insert(0, values[2])
            
            # Formata o CPF para exibição
            cpf = values[3]
            self.campos["cpf"].insert(0, cpf)
            
            # Remove "R$ " e formata o salário
            salario = values[4].replace("R$ ", "").replace(".", "").replace(",", ".")
            self.campos["salario"].insert(0, salario)
    
    def listar_funcionarios(self):
        # Limpa a treeview
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Monta a query com ordenação dinâmica
            query = f"""
                SELECT id_funcionario, nome, cargo, cpf, salario 
                FROM funcionario 
                ORDER BY {self.ordenacao['coluna']} {self.ordenacao['direcao']}
            """
            
            cursor.execute(query)
            
            for funcionario in cursor.fetchall():
                # Formata os valores para exibição
                cpf_formatado = f"{funcionario[3][:3]}.{funcionario[3][3:6]}.{funcionario[3][6:9]}-{funcionario[3][9:]}"
                salario_formatado = f"R$ {funcionario[4]:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                
                self.tree.insert("", "end", values=(
                    funcionario[0],  # ID
                    funcionario[1],  # Nome
                    funcionario[2],  # Cargo
                    cpf_formatado,   # CPF formatado
                    salario_formatado  # Salário formatado
                ))
                
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao carregar funcionários:\n{str(e)}", 
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def inserir_funcionario(self):
        if not self.validar_campos():
            return
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Prepara os dados
            cpf = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
            salario = float(
                self.campos["salario"].get()
                .replace(".", "")
                .replace(",", ".")
            )
            
            # Executa a inserção
            cursor.execute("""
                INSERT INTO funcionario (nome, cargo, cpf, salario)
                VALUES (%s, %s, %s, %s)
            """, (
                self.campos["nome"].get().strip(),
                self.campos["cargo"].get().strip(),
                cpf,
                salario
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso", 
                message="Funcionário cadastrado com sucesso!", 
                icon="check"
            )
            
            self.limpar_campos()
            self.listar_funcionarios()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao cadastrar funcionário:\n{str(e)}", 
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def atualizar_funcionario(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso", 
                message="Selecione um funcionário para atualizar!", 
                icon="warning"
            )
            return
            
        if not self.validar_campos():
            return
        
        conn = None
        cursor = None
        try:
            conn = conectar()
            cursor = conn.cursor()
            
            # Obtém o ID do funcionário selecionado
            funcionario_id = self.tree.item(selected, "values")[0]
            
            # Prepara os dados
            cpf = re.sub(r'[^0-9]', '', self.campos["cpf"].get())
            salario = float(
                self.campos["salario"].get()
                .replace(".", "")
                .replace(",", ".")
            )
            
            # Executa a atualização
            cursor.execute("""
                UPDATE funcionario 
                SET nome = %s, cargo = %s, cpf = %s, salario = %s
                WHERE id_funcionario = %s
            """, (
                self.campos["nome"].get().strip(),
                self.campos["cargo"].get().strip(),
                cpf,
                salario,
                funcionario_id
            ))
            
            conn.commit()
            
            CTkMessagebox(
                title="Sucesso", 
                message="Dados do funcionário atualizados com sucesso!", 
                icon="check"
            )
            
            self.listar_funcionarios()
            
        except Exception as e:
            CTkMessagebox(
                title="Erro", 
                message=f"Falha ao atualizar funcionário:\n{str(e)}", 
                icon="cancel"
            )
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
    
    def excluir_funcionario(self):
        selected = self.tree.selection()
        if not selected:
            CTkMessagebox(
                title="Aviso", 
                message="Selecione um funcionário para excluir!", 
                icon="warning"
            )
            return
        
        # Confirmação da exclusão
        confirmacao = CTkMessagebox(
            title="Confirmação", 
            message=f"Tem certeza que deseja excluir o funcionário {self.tree.item(selected, 'values')[1]}?", 
            icon="question", 
            option_1="Cancelar", 
            option_2="Excluir"
        )
        
        if confirmacao.get() == "Excluir":
            conn = None
            cursor = None
            try:
                conn = conectar()
                cursor = conn.cursor()
                
                # Obtém o ID do funcionário selecionado
                funcionario_id = self.tree.item(selected, "values")[0]
                
                # Executa a exclusão
                cursor.execute("""
                    DELETE FROM funcionario 
                    WHERE id_funcionario = %s
                """, (funcionario_id,))
                
                conn.commit()
                
                CTkMessagebox(
                    title="Sucesso", 
                    message="Funcionário excluído com sucesso!", 
                    icon="check"
                )
                
                self.limpar_campos()
                self.listar_funcionarios()
                
            except Exception as e:
                CTkMessagebox(
                    title="Erro", 
                    message=f"Falha ao excluir funcionário:\n{str(e)}", 
                    icon="cancel"
                )
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

def abrir(admin_menu=None):
    app = FuncionarioCRUD(admin_menu)
    app.janela.mainloop()

if __name__ == "__main__":
    abrir()