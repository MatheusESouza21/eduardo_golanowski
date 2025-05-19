import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import mysql.connector
from datetime import datetime

class DashboardApp:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Gestão Comercial - Dashboard Premium")
        self.root.geometry("1600x900")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Conexão com o MySQL
        self.db = mysql.connector.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='',
            database='matheuseduardodb_sa'
        )
        self.cursor = self.db.cursor()
        
        # Configurações de estilo
        self.setup_styles()
        self.setup_ui()
    
    def setup_styles(self):
        """Configura estilos personalizados"""
        self.font_title = ctk.CTkFont(size=24, weight="bold")
        self.font_subtitle = ctk.CTkFont(size=16, weight="bold")
        self.font_body = ctk.CTkFont(size=14)
        self.font_small = ctk.CTkFont(size=12)
        
        # Cores personalizadas
        self.colors = {
            "primary": "#4e73df",
            "success": "#1cc88a",
            "info": "#36b9cc",
            "warning": "#f6c23e",
            "danger": "#e74a3b",
            "dark": "#5a5c69",
            "light": "#f8f9fc"
        }
        
        # Configuração matplotlib
        plt.rcParams['figure.facecolor'] = '#ffffff'
        plt.rcParams['axes.facecolor'] = '#ffffff'
        plt.rcParams['grid.color'] = '#e3e6f0'
        plt.rcParams['axes.grid'] = True
    
    def fetch_data(self, query, params=None):
        """Executa uma consulta SQL e retorna os resultados"""
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except mysql.connector.Error as err:
            print(f"Erro MySQL: {err}")
            return []
    
    def setup_ui(self):
        """Configura a interface principal"""
        # Layout principal
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        
        # Sidebar
        self.create_sidebar()
        
        # Main content
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0, fg_color="#f8f9fc")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Container principal
        self.content_frame = ctk.CTkFrame(self.main_frame, corner_radius=12)
        self.content_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
        
        self.show_home_page()
    
    def create_sidebar(self):
        """Cria sidebar com visual premium"""
        self.sidebar_frame = ctk.CTkFrame(
            self.root,
            width=280,
            corner_radius=0,
            fg_color="#2c3e50"
        )
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # Logo e título
        logo_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        logo_frame.pack(pady=(30, 20), padx=20, fill="x")
        
        ctk.CTkLabel(
            logo_frame,
            text="⚡",
            font=ctk.CTkFont(size=28),
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkLabel(
            logo_frame,
            text="Gestão Comercial",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#ecf0f1"
        ).pack(side="left")
        
        # Menu de navegação
        nav_buttons = [
            {"text": "📊 Visão Geral", "command": self.show_home_page},
            {"text": "🛒 Compras", "command": self.show_compras_page},
            {"text": "📦 Estoque", "command": self.show_produtos_page},
            {"text": "🏭 Fornecedores", "command": self.show_fornecedores_page},
            {"text": "👔 Funcionários", "command": self.show_funcionarios_page},
        ]
        
        for btn in nav_buttons:
            button = ctk.CTkButton(
                self.sidebar_frame,
                text=btn["text"],
                command=btn["command"],
                anchor="w",
                fg_color="transparent",
                hover_color="#34495e",
                font=self.font_body,
                height=50,
                corner_radius=8,
                text_color="#ecf0f1"
            )
            button.pack(fill="x", padx=15, pady=3)
        
        # Rodapé da sidebar
        footer_frame = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        footer_frame.pack(side="bottom", fill="x", padx=15, pady=20)
        
        # Botão de atualização
        refresh_btn = ctk.CTkButton(
            footer_frame,
            text="🔄 Atualizar Dados",
            command=self.update_all_data,
            fg_color="#3498db",
            hover_color="#2980b9",
            font=self.font_body,
            height=40,
            corner_radius=8
        )
        refresh_btn.pack(fill="x", pady=(0, 15))
    
    def create_card(self, parent, title, value, icon="", color="primary", trend=""):
        """Cria um card de KPI estilizado"""
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            border_width=1,
            border_color="#e3e6f0",
            fg_color="#ffffff"
        )
        
        # Header do card
        header_frame = ctk.CTkFrame(card, fg_color="transparent")
        header_frame.pack(fill="x", padx=15, pady=(15, 0))
        
        ctk.CTkLabel(
            header_frame,
            text=title,
            font=self.font_small,
            text_color="#5a5c69"
        ).pack(side="left")
        
        if icon:
            icon_label = ctk.CTkLabel(
                header_frame,
                text=icon,
                font=self.font_body
            )
            icon_label.pack(side="right")
        
        # Valor principal
        ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=self.colors[color]
        ).pack(pady=(5, 0))
        
        # Trend (opcional)
        if trend:
            trend_frame = ctk.CTkFrame(card, fg_color="transparent")
            trend_frame.pack(pady=(0, 15), padx=15)
            
            trend_color = "#1cc88a" if trend.startswith("+") else "#e74a3b"
            
            ctk.CTkLabel(
                trend_frame,
                text="▲" if trend.startswith("+") else "▼",
                text_color=trend_color,
                font=self.font_small
            ).pack(side="left")
            
            ctk.CTkLabel(
                trend_frame,
                text=trend,
                text_color=trend_color,
                font=self.font_small
            ).pack(side="left", padx=5)
        
        return card
    
    def update_all_data(self):
        """Atualiza todos os dados do banco"""
        if hasattr(self, 'current_page'):
            self.current_page()
    
    def clear_main_frame(self):
        """Limpa o frame principal"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def show_home_page(self):
        self.clear_main_frame()
        self.current_page = self.show_home_page
        
        # Container principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Visão Geral do Sistema",
            font=self.font_title,
            text_color="#2d3748"
        ).pack(side="left")
        
        # KPIs
        kpis_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        kpis_frame.grid(row=1, column=0, sticky="nsew")
        
        # Consultas SQL para KPIs
        total_compras = self.fetch_data("SELECT SUM(total) FROM compra")[0][0] or 0
        total_produtos = self.fetch_data("SELECT COUNT(*) FROM produto")[0][0]
        estoque_critico = self.fetch_data("SELECT COUNT(*) FROM produto WHERE quantidade < 5")[0][0]
        total_fornecedores = self.fetch_data("SELECT COUNT(*) FROM fornecedor")[0][0]
        
        # Cards de KPI
        kpi_data = [
            {"title": "Total em Compras", "value": f"R$ {total_compras:,.2f}", "color": "primary", "icon": "💵", "trend": "+12%"},
            {"title": "Produtos Cadastrados", "value": total_produtos, "color": "success", "icon": "📦", "trend": "+5%"},
            {"title": "Estoque Crítico", "value": estoque_critico, "color": "danger" if estoque_critico > 0 else "success", "icon": "⚠️" if estoque_critico > 0 else "✅"},
            {"title": "Fornecedores Ativos", "value": total_fornecedores, "color": "info", "icon": "🏭"},
        ]
        
        for i, kpi in enumerate(kpi_data):
            kpi_frame = ctk.CTkFrame(kpis_frame, fg_color="transparent")
            kpi_frame.grid(row=0, column=i, padx=10, sticky="nsew")
            kpis_frame.grid_columnconfigure(i, weight=1)
            
            card = self.create_card(
                kpi_frame,
                title=kpi["title"],
                value=kpi["value"],
                icon=kpi.get("icon", ""),
                color=kpi["color"],
                trend=kpi.get("trend", "")
            )
            card.pack(fill="both", expand=True)
        
        # Gráficos
        charts_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        charts_frame.grid(row=2, column=0, sticky="nsew", pady=(20, 0))
        
        # Gráfico 1: Compras mensais
        dados_mensais = self.fetch_data("""
            SELECT DATE_FORMAT(data_compra, '%Y-%m') AS mes, 
                   SUM(total) AS total 
            FROM compra 
            GROUP BY mes 
            ORDER BY mes DESC 
            LIMIT 6
        """)
        
        fig1, ax1 = plt.subplots(figsize=(8, 5), facecolor='#ffffff')
        meses = [x[0] for x in dados_mensais][::-1]
        valores = [float(x[1]) for x in dados_mensais][::-1]
        
        ax1.bar(meses, valores, color=self.colors["primary"], alpha=0.7)
        ax1.plot(meses, valores, color=self.colors["primary"], marker='o', linewidth=2)
        
        ax1.set_title('Compras Mensais', pad=20, fontsize=14, fontweight='bold')
        ax1.set_ylabel('Valor (R$)', fontsize=12)
        ax1.grid(axis='y', linestyle='--', alpha=0.4)
        ax1.set_facecolor('#ffffff')
        
        for spine in ax1.spines.values():
            spine.set_edgecolor('#d1d3e2')
        
        # Gráfico 2: Top produtos em estoque
        produtos_estoque = self.fetch_data("""
            SELECT p.nome, p.quantidade 
            FROM produto p 
            ORDER BY p.quantidade DESC 
            LIMIT 5
        """)
        
        fig2, ax2 = plt.subplots(figsize=(8, 5), facecolor='#ffffff')
        produtos = [x[0][:15] + "..." if len(x[0]) > 15 else x[0] for x in produtos_estoque]
        quantidades = [x[1] for x in produtos_estoque]
        
        bars = ax2.barh(produtos, quantidades, color=self.colors["success"], alpha=0.7)
        ax2.bar_label(bars, padding=5, fontsize=10)
        
        ax2.set_title('Top Produtos em Estoque', pad=20, fontsize=14, fontweight='bold')
        ax2.grid(axis='x', linestyle='--', alpha=0.4)
        ax2.set_facecolor('#ffffff')
        
        for spine in ax2.spines.values():
            spine.set_edgecolor('#d1d3e2')
        
        # Adicionando gráficos ao dashboard
        chart_col1 = ctk.CTkFrame(charts_frame, corner_radius=12)
        chart_col1.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        chart_col2 = ctk.CTkFrame(charts_frame, corner_radius=12)
        chart_col2.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        
        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        
        # Canvas dos gráficos
        canvas1 = FigureCanvasTkAgg(fig1, master=chart_col1)
        canvas1.draw()
        canvas1.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas2 = FigureCanvasTkAgg(fig2, master=chart_col2)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill="both", expand=True, padx=10, pady=10)
    
    def show_compras_page(self):
        self.clear_main_frame()
        self.current_page = self.show_compras_page
        
        # Container principal
        main_container = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Cabeçalho
        header_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            header_frame,
            text="Histórico de Compras",
            font=self.font_title,
            text_color="#2d3748"
        ).pack(side="left")
        
        # Filtros
        filter_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        filter_frame.pack(fill="x", pady=(0, 15))
        
        ctk.CTkLabel(
            filter_frame,
            text="Filtrar por período:",
            font=self.font_body
        ).pack(side="left", padx=(0, 10))
        
        date_start = ctk.CTkEntry(filter_frame, placeholder_text="Data Início", width=120)
        date_start.pack(side="left", padx=5)
        
        date_end = ctk.CTkEntry(filter_frame, placeholder_text="Data Fim", width=120)
        date_end.pack(side="left", padx=5)
        
        filter_btn = ctk.CTkButton(
            filter_frame,
            text="Aplicar Filtro",
            width=100,
            fg_color=self.colors["primary"]
        )
        filter_btn.pack(side="left", padx=10)
        
        # Tabela
        table_container = ctk.CTkFrame(main_container, corner_radius=12)
        table_container.pack(fill="both", expand=True)
        
        # Consulta SQL com JOIN
        compras = self.fetch_data("""
            SELECT c.id_compra, c.data_compra, c.total, u.nome as usuario, 
                   GROUP_CONCAT(p.nome SEPARATOR ', ') as produtos
            FROM compra c
            JOIN usuario u ON c.id_usuario = u.id_usuario
            JOIN item_compra ic ON c.id_compra = ic.id_compra
            JOIN produto p ON ic.id_produto = p.id_produto
            GROUP BY c.id_compra
            ORDER BY c.data_compra DESC
            LIMIT 100
        """)
        
        # Treeview com estilo melhorado
        style = ttk.Style()
        style.theme_use("default")
        style.configure(
            "Treeview",
            background="#ffffff",
            foreground="#2d3748",
            rowheight=35,
            fieldbackground="#ffffff",
            bordercolor="#e3e6f0",
            borderwidth=1,
            font=('Segoe UI', 11)
        )
        style.map('Treeview', background=[('selected', '#4e73df')])
        
        style.configure(
            "Treeview.Heading",
            background="#f8f9fc",
            foreground="#4e73df",
            font=('Segoe UI', 12, 'bold'),
            padding=10,
            relief="flat"
        )
        
        columns = ("ID", "Data", "Total (R$)", "Usuário", "Produtos")
        tree = ttk.Treeview(
            table_container,
            columns=columns,
            show="headings",
            height=20,
            style="Treeview"
        )
        
        # Configuração das colunas
        col_widths = [80, 150, 120, 180, 300]
        for col, width in zip(columns, col_widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, anchor="center")
        
        # Adicionando dados
        for compra in compras:
            tree.insert("", tk.END, values=(
                compra[0],
                compra[1].strftime("%d/%m/%Y %H:%M") if isinstance(compra[1], datetime) else compra[1],
                f"{compra[2]:,.2f}",
                compra[3],
                compra[4][:50] + "..." if len(compra[4]) > 50 else compra[4]
            ))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(
            table_container,
            orient="vertical",
            command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Empacotamento
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Botão de exportação
        export_frame = ctk.CTkFrame(main_container, fg_color="transparent")
        export_frame.pack(fill="x", pady=(15, 0))
        
        ctk.CTkButton(
            export_frame,
            text="📄 Exportar para Excel",
            fg_color="#1cc88a",
            hover_color="#17a673",
            font=self.font_body
        ).pack(side="right")

    def show_produtos_page(self):
        self.clear_main_frame()
        self.current_page = self.show_produtos_page
        
        # Layout com abas
        tabview = ctk.CTkTabview(self.content_frame)
        tabview.pack(fill="both", expand=True, padx=20, pady=20)
        
        tabview.add("Estoque")
        tabview.add("Produtos por Fornecedor")
        
        # Aba 1: Estoque
        produtos = self.fetch_data("""
            SELECT p.id_produto, p.nome, p.descricao, p.quantidade, p.preco, f.nome as fornecedor
            FROM produto p
            LEFT JOIN fornecedor f ON p.id_fornecedor = f.id_fornecedor
            ORDER BY p.quantidade ASC
        """)
        
        columns = ("ID", "Nome", "Descrição", "Qtd.", "Preço", "Fornecedor")
        tree = ttk.Treeview(tabview.tab("Estoque"), columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for produto in produtos:
            qtd = produto[3]
            tag = 'critical' if qtd < 5 else ('warning' if qtd < 10 else '')
            
            tree.insert("", tk.END, values=(
                produto[0],
                produto[1],
                produto[2][:30] + "..." if produto[2] and len(produto[2]) > 30 else produto[2] or "",
                qtd,
                f"R$ {produto[4]:,.2f}",
                produto[5] or "N/A"
            ), tags=(tag,))
        
        tree.tag_configure('critical', background='#ffdddd')
        tree.tag_configure('warning', background='#fff3cd')
        
        scrollbar = ttk.Scrollbar(tabview.tab("Estoque"), orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        # Aba 2: Produtos por Fornecedor (Gráfico)
        dados_fornecedor = self.fetch_data("""
            SELECT f.nome, COUNT(p.id_produto) as total_produtos
            FROM fornecedor f
            LEFT JOIN produto p ON f.id_fornecedor = p.id_fornecedor
            GROUP BY f.id_fornecedor
            ORDER BY total_produtos DESC
        """)
        
        fig, ax = plt.subplots(figsize=(8, 6), facecolor='#ffffff')
        fornecedores = [x[0] for x in dados_fornecedor]
        quantidades = [x[1] for x in dados_fornecedor]
        
        ax.bar(fornecedores, quantidades, color=[self.colors["primary"], self.colors["success"], self.colors["info"]])
        ax.set_title('Produtos por Fornecedor', pad=20, fontsize=14, fontweight='bold')
        ax.set_ylabel('Quantidade de Produtos', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.set_facecolor('#ffffff')
        
        for spine in ax.spines.values():
            spine.set_edgecolor('#d1d3e2')
        
        canvas_frame = ctk.CTkFrame(tabview.tab("Produtos por Fornecedor"))
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        canvas = FigureCanvasTkAgg(fig, master=canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
    
    def show_fornecedores_page(self):
        self.clear_main_frame()
        self.current_page = self.show_fornecedores_page
        
        # Consulta SQL
        fornecedores = self.fetch_data("""
            SELECT f.id_fornecedor, f.nome, f.cnpj, f.telefone, 
                   COUNT(p.id_produto) as total_produtos,
                   SUM(ic.subtotal) as total_compras
            FROM fornecedor f
            LEFT JOIN produto p ON f.id_fornecedor = p.id_fornecedor
            LEFT JOIN item_compra ic ON p.id_produto = ic.id_produto
            GROUP BY f.id_fornecedor
        """)
        
        # Tabela
        columns = ("ID", "Nome", "CNPJ", "Telefone", "Produtos", "Total em Compras (R$)")
        tree = ttk.Treeview(self.content_frame, columns=columns, show="headings", height=20)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for fornecedor in fornecedores:
            tree.insert("", tk.END, values=(
                fornecedor[0],
                fornecedor[1],
                f"{fornecedor[2][:2]}.{fornecedor[2][2:5]}.{fornecedor[2][5:8]}/{fornecedor[2][8:12]}-{fornecedor[2][12:14]}",
                fornecedor[3],
                fornecedor[4],
                f"{fornecedor[5]:,.2f}" if fornecedor[5] else "0.00"
            ))
        
        scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_funcionarios_page(self):
        self.clear_main_frame()
        self.current_page = self.show_funcionarios_page
        
        # Consulta SQL
        funcionarios = self.fetch_data("""
            SELECT id_funcionario, nome, cargo, cpf, salario
            FROM funcionario
            ORDER BY salario DESC
        """)
        
        # Layout com gráfico e tabela
        main_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Gráfico de salários
        fig, ax = plt.subplots(figsize=(6, 4), facecolor='#ffffff')
        cargos = [x[2] for x in funcionarios]
        salarios = [float(x[4]) for x in funcionarios]
        
        ax.bar(cargos, salarios, color=self.colors["info"], alpha=0.7)
        ax.set_title('Distribuição de Salários', pad=15, fontsize=14, fontweight='bold')
        ax.set_ylabel('Salário (R$)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        ax.grid(axis='y', linestyle='--', alpha=0.4)
        ax.set_facecolor('#ffffff')
        
        for spine in ax.spines.values():
            spine.set_edgecolor('#d1d3e2')
        
        chart_frame = ctk.CTkFrame(main_frame)
        chart_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        
        canvas = FigureCanvasTkAgg(fig, master=chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        # Tabela
        table_frame = ctk.CTkFrame(main_frame)
        table_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        main_frame.grid_columnconfigure(1, weight=1)
        
        columns = ("ID", "Nome", "Cargo", "CPF", "Salário (R$)")
        tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=10)
        
        for col in columns:
            tree.heading(col, text=col)
        
        for func in funcionarios:
            tree.insert("", tk.END, values=(
                func[0],
                func[1],
                func[2],
                f"{func[3][:3]}.{func[3][3:6]}.{func[3][6:9]}-{func[3][9:11]}",
                f"{func[4]:,.2f}"
            ))
        
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = DashboardApp()
    app.root.mainloop()