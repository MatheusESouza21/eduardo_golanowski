import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class DashboardApp:
    def __init__(self):
        # Configuração da janela principal
        self.root = ctk.CTk()
        self.root.title("Dashboard Administrativo")
        self.root.geometry("1200x700")
        
        # Configuração do tema
        ctk.set_appearance_mode("dark")  # Pode ser "light", "dark" ou "system"
        ctk.set_default_color_theme("blue")  # Temas: "blue", "green", "dark-blue"
        
        # Layout principal
        self.setup_ui()
        
    def setup_ui(self):
        # Criação do frame de navegação (sidebar)
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar_frame.pack(side="left", fill="y")
        self.sidebar_frame.pack_propagate(False)
        
        # Criação do frame de conteúdo principal
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_frame.pack(side="right", expand=True, fill="both")
        
        # Adicionando widgets à sidebar
        self.create_sidebar()
        
        # Página inicial do dashboard
        self.show_home_page()
    
    def create_sidebar(self):
        # Logo ou título
        logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="Dashboard App",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        logo_label.pack(pady=(20, 10), padx=20)
        
        # Botões de navegação
        nav_buttons = [
            {"text": "🏠 Início", "command": self.show_home_page},
            {"text": "📊 Vendas", "command": self.show_sales_page},
            {"text": "📦 Produtos", "command": self.show_products_page},
            {"text": "👥 Clientes", "command": self.show_customers_page},
            {"text": "⚙ Configurações", "command": self.show_settings_page}
        ]
        
        for button in nav_buttons:
            btn = ctk.CTkButton(
                self.sidebar_frame,
                text=button["text"],
                command=button["command"],
                fg_color="transparent",
                anchor="w",
                height=40,
                font=ctk.CTkFont(size=14)
            )
            btn.pack(fill="x", padx=10, pady=5)
        
        # Espaçamento
        ctk.CTkLabel(self.sidebar_frame, text="").pack(pady=5)
        
        # Modo de aparência
        self.appearance_mode = ctk.StringVar(value="dark")
        appearance_menu = ctk.CTkOptionMenu(
            self.sidebar_frame,
            values=["light", "dark", "system"],
            command=self.change_appearance_mode,
            variable=self.appearance_mode
        )
        appearance_menu.pack(pady=(10, 0), padx=20, fill="x")
        
        # Botão de sair
        logout_btn = ctk.CTkButton(
            self.sidebar_frame,
            text="🚪 Sair",
            command=self.root.quit,
            fg_color="#d9534f",
            hover_color="#c9302c"
        )
        logout_btn.pack(side="bottom", pady=20, padx=10, fill="x")
    
    def clear_main_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_home_page(self):
        self.clear_main_frame()
        
        # Título da página
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Visão Geral",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Métricas (KPI cards)
        metrics_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=20, pady=10)
        
        metrics = [
            {"title": "Vendas Totais", "value": "R$ 24.560", "change": "+12%"},
            {"title": "Novos Clientes", "value": "143", "change": "+5%"},
            {"title": "Pedidos", "value": "326", "change": "+8%"},
            {"title": "Satisfação", "value": "92%", "change": "+2%"}
        ]
        
        for i, metric in enumerate(metrics):
            metric_card = ctk.CTkFrame(
                metrics_frame,
                width=200,
                height=120,
                border_width=1,
                border_color="#444"
            )
            metric_card.grid(row=0, column=i, padx=10, pady=5, sticky="nsew")
            metrics_frame.grid_columnconfigure(i, weight=1)
            
            # Conteúdo do card
            ctk.CTkLabel(
                metric_card,
                text=metric["title"],
                font=ctk.CTkFont(size=14)
            ).pack(pady=(10, 0), padx=10, anchor="w")
            
            ctk.CTkLabel(
                metric_card,
                text=metric["value"],
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=5, padx=10, anchor="w")
            
            change_frame = ctk.CTkFrame(metric_card, fg_color="transparent")
            change_frame.pack(pady=(0, 10), padx=10, anchor="w")
            
            # Ícone de aumento/redução (simplificado)
            color = "#28a745" if "+" in metric["change"] else "#dc3545"
            ctk.CTkLabel(
                change_frame,
                text="▲" if "+" in metric["change"] else "▼",
                text_color=color,
                font=ctk.CTkFont(size=12)
            ).pack(side="left")
            
            ctk.CTkLabel(
                change_frame,
                text=metric["change"],
                text_color=color,
                font=ctk.CTkFont(size=12)
            ).pack(side="left", padx=5)
        
        # Gráficos
        charts_frame = ctk.CTkFrame(self.main_frame)
        charts_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Gráfico de linhas (Matplotlib)
        fig, ax = plt.subplots(figsize=(6, 3), dpi=100)
        months = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun']
        sales = [12000, 18000, 15000, 22000, 24500, 19500]
        ax.plot(months, sales, marker='o', color='#007bff')
        ax.set_title('Vendas Mensais', pad=20)
        ax.grid(True, linestyle='--', alpha=0.7)
        fig.tight_layout()
        
        chart_canvas = FigureCanvasTkAgg(fig, master=charts_frame)
        chart_canvas.draw()
        chart_canvas.get_tk_widget().pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Gráfico de pizza
        fig2, ax2 = plt.subplots(figsize=(4, 3), dpi=100)
        categories = ['Eletrônicos', 'Roupas', 'Alimentos', 'Livros']
        values = [45, 30, 15, 10]
        ax2.pie(values, labels=categories, autopct='%1.1f%%', startangle=90)
        ax2.set_title('Categorias de Produtos')
        fig2.tight_layout()
        
        pie_canvas = FigureCanvasTkAgg(fig2, master=charts_frame)
        pie_canvas.draw()
        pie_canvas.get_tk_widget().pack(side="right", fill="both", expand=True, padx=10, pady=10)
    
    def show_sales_page(self):
        self.clear_main_frame()
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Relatório de Vendas",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Adicione aqui o conteúdo específico da página de vendas
        # Por exemplo, uma tabela com dados de vendas
    
    def show_products_page(self):
        self.clear_main_frame()
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Gerenciamento de Produtos",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Adicione aqui o conteúdo específico da página de produtos
    
    def show_customers_page(self):
        self.clear_main_frame()
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Gerenciamento de Clientes",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Adicione aqui o conteúdo específico da página de clientes
    
    def show_settings_page(self):
        self.clear_main_frame()
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="Configurações",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10), padx=20, anchor="w")
        
        # Adicione aqui o conteúdo específico da página de configurações
    
    def change_appearance_mode(self, new_mode):
        ctk.set_appearance_mode(new_mode)

    

if __name__ == "__main__":
    app = DashboardApp()
    app.root.mainloop()