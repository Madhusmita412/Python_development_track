from tkinter import filedialog
import customtkinter as ctk
from ui.export_dialog import ExportDialog
from ui.sidebar import Sidebar
from ui.header import Header
from ui.cards import DashboardCard
from ui.toolbar import Toolbar
from ui.inventory_table import InventoryTable
from ui.charts import DashboardCharts

from services.inventory_processor import InventoryProcessor
from services.analytics import InventoryAnalytics
from services.exporter import Exporter
from ui.dashboard_summary import SummaryCard

class Dashboard:

    def __init__(self):

      
        # Theme
      

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

      
        # Main Window
      

        self.root = ctk.CTk()

        self.root.title("Retail Inventory Analytics Dashboard")
        self.root.geometry("1500x850")
        self.root.minsize(1300, 750)

      
        # Colors
      

        self.bg_color = "#0F172A"
        self.sidebar_color = "#111827"
        self.card_color = "#1E293B"
        self.accent = "#2563EB"

        self.root.configure(fg_color=self.bg_color)

      
        # Backend Services
      

        self.processor = InventoryProcessor()
        self.exporter = Exporter()
        self.analytics = None

      
        # Build UI
      

        self.create_layout()

      
        # Load Default Dataset
      

        try:
            self.load_csv("data/inventory_data.csv")
        except FileNotFoundError:
            pass

  
    # Main Layout
  

    def create_layout(self):

        # Sidebar

        self.sidebar = Sidebar(self.root)

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # Main Content

        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=self.bg_color,
            corner_radius=0
        )

        self.main_frame.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.create_header()

  
    # Header
  

    def create_header(self):

        # Header

        self.header = Header(self.main_frame)

        self.header.pack(
            fill="x",
            padx=25,
            pady=20
        )

      
        # Welcome Card
      

        welcome = ctk.CTkFrame(
            self.main_frame,
            height=120,
            fg_color=self.card_color,
            corner_radius=20
        )

        welcome.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        welcome.pack_propagate(False)

        welcome_title = ctk.CTkLabel(
            welcome,
            text="Welcome Back 👋",
            font=("Segoe UI", 26, "bold")
        )

        welcome_title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        welcome_text = ctk.CTkLabel(
            welcome,
            text="Monitor inventory, analyze stock levels and generate business insights from one dashboard.",
            font=("Segoe UI", 15),
            text_color="lightgray"
        )

        welcome_text.pack(
            anchor="w",
            padx=25
        )

      
        # KPI Cards
        summary = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        summary.pack(
            fill="x",
            padx=25,
            pady=(10,20)
        )

        self.summary1 = SummaryCard(
            summary,
            "💰",
            "Revenue",
            "#10B981"
        )

        self.summary1.pack(
            side="left",
            padx=10
        )

        self.summary2 = SummaryCard(
            summary,
            "📈",
            "Growth",
            "#3B82F6"
        )

        self.summary2.pack(
            side="left",
            padx=10
        )

        self.summary3 = SummaryCard(
            summary,
            "⚠",
            "Alerts",
            "#EF4444"
        )

        self.summary3.pack(
            side="left",
            padx=10
        )

        self.summary4 = SummaryCard(
            summary,
            "🏆",
            "Best Category",
            "#F59E0B"
        )

        self.summary4.pack(
            side="left",
            padx=10
        )

        self.create_cards()

            
                # Toolbar
        revenue = (
            df["Stock"] *
            df["Price"]
        ).sum()

        growth = "18%"

        alerts = len(
            df[
                df["Stock"] <=
                df["Reorder Level"]
            ]
        )

        best = (
            df.assign(
                Value=df["Stock"] * df["Price"]
            )
            .groupby("Category")["Value"]
            .sum()
            .idxmax()
        )

        self.summary1.update(
            f"₹{revenue:,.0f}"
        )

        self.summary2.update(growth)

        self.summary3.update(str(alerts))

        self.summary4.update(best)    

        self.toolbar = Toolbar(self.main_frame)

        self.toolbar.pack(
            fill="x",
            padx=25,
            pady=20
        )

      
        # Toolbar Events
      

        self.toolbar.upload_btn.configure(
            command=self.upload_csv
        )

        self.toolbar.refresh_btn.configure(
            command=self.refresh_table
        )

        self.toolbar.export_btn.configure(
            command=self.export_report
        )

        self.toolbar.search.bind(
            "<KeyRelease>",
            self.search_inventory
        )

        self.toolbar.category.configure(
            command=self.filter_category
        )

        self.toolbar.status.configure(
            command=self.filter_status
        )

        self.toolbar.analyze_btn.configure(
            command=self.show_analytics
        )
        self.toolbar.clean_btn.configure(
            command=self.clean_inventory
        )

        
        # Charts

        self.charts = DashboardCharts(
            self.main_frame
        )
        
        self.charts.pack(
            fill="both",
            padx=25,
            pady=(20, 20)
        )

      
        # Inventory Table
      

        self.create_table()


        
    # Filter Category
    
    def clean_inventory(self):

        if self.processor.df.empty:
            return

        df = self.processor.clean_data()

        self.inventory_table.load_data(df)
        
        self.charts.update_dashboard(df)

        kpis = self.processor.calculate_kpis()

        self.products_card.update_value(
            str(kpis["products"])
        )

        self.inventory_card.update_value(
            f"₹{kpis['inventory_value']:,.0f}"
        )

        self.low_stock_card.update_value(
            str(kpis["low_stock"])
        )

        self.suppliers_card.update_value(
            str(kpis["suppliers"])
        )
    def filter_category(self, category):

        if self.processor.df.empty:
            return

        df = self.processor.filter_category(category)

        self.inventory_table.load_data(df)

        self.charts.update_dashboard(df)
    # Filter Status
    

    def filter_status(self, status):

        if self.processor.df.empty:
            return

        df = self.processor.filter_status(status)

        self.inventory_table.load_data(df)

        self.charts.update_dashboard(df)

    
    # Show Analytics
    

    def show_analytics(self):

        if self.processor.df.empty:
            return

        df = self.processor.df

        inventory_value = (
            df["Stock"] *
            df["Price"]
        ).sum()

        total_products = len(df)

        suppliers = df["Supplier"].nunique()

        low_stock = len(

            df[
                df["Stock"] <=
                df["Reorder Level"]
            ]

        )

        highest_category = (

            df.assign(
                Value=df["Stock"] * df["Price"]
            )

            .groupby("Category")["Value"]

            .sum()

            .idxmax()

        )

        popup = ctk.CTkToplevel(self.root)

        popup.title("Business Analytics")

        popup.geometry("600x500")

        popup.grab_set()

        title = ctk.CTkLabel(

            popup,

            text="📊 Business Analytics Summary",

            font=("Segoe UI",24,"bold")

        )

        title.pack(
            pady=20
        )

        text = f"""

            📦 Total Products : {total_products}

            💰 Inventory Value : ₹{inventory_value:,.0f}

            🚚 Suppliers : {suppliers}

            ⚠ Low Stock : {low_stock}

            🏆 Highest Category :

            {highest_category}

        """

        info = ctk.CTkTextbox(

            popup,

            width=500,

            height=250

        )

        info.pack(
            padx=20,
            pady=20,
            fill="both",
            expand=True
        )

        info.insert("1.0", text)

        info.configure(state="disabled")

        close = ctk.CTkButton(

            popup,

            text="Close",

            command=popup.destroy

        )

        close.pack(
            pady=20
        )

    def create_table(self):

        self.inventory_table = InventoryTable(
            self.main_frame
        )

        self.inventory_table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    
    # Upload CSV
    

    def upload_csv(self):

        file_path = filedialog.askopenfilename(
            title="Select Inventory CSV",
            filetypes=[("CSV Files", "*.csv")]
        )

        if file_path:
            self.load_csv(file_path)

    
    # Load CSV
    

    def load_csv(self, file_path):

        df = self.processor.load_csv(file_path)

        df = self.processor.clean_data()

        self.analytics = InventoryAnalytics(df)

        kpis = self.processor.calculate_kpis()

        self.products_card.update_value(
            str(kpis["products"])
        )

        self.inventory_card.update_value(
            f"₹{kpis['inventory_value']:,.0f}"
        )

        self.low_stock_card.update_value(
            str(kpis["low_stock"])
        )

        self.suppliers_card.update_value(
            str(kpis["suppliers"])
        )

        self.inventory_table.load_data(df)

    
    # Refresh Table
    
    def refresh_table(self):

        if self.processor.df.empty:
            return

        self.inventory_table.load_data(
            self.processor.df
        )

        self.charts.update_dashboard(
            self.processor.df
        )
    

    def export_report(self):

        if self.processor.df.empty:
            return

        self.exporter.export_excel(
            self.processor.df
        )

    
    # Search Inventory
    

    def search_inventory(self, event):

        if self.processor.df.empty:
            return

        keyword = self.toolbar.search.get()

        df = self.processor.search(keyword)

        self.inventory_table.load_data(df)

        self.charts.update_dashboard(df)
            
    # Dashboard KPI Cards
    

    def create_cards(self):

        cards_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.products_card = DashboardCard(
            cards_frame,
            "📦",
            "Products",
            "0"
        )

        self.products_card.grid(
            row=0,
            column=0,
            padx=12
        )

        self.inventory_card = DashboardCard(
            cards_frame,
            "💰",
            "Inventory Value",
            "₹0"
        )

        self.inventory_card.grid(
            row=0,
            column=1,
            padx=12
        )

        self.low_stock_card = DashboardCard(
            cards_frame,
            "⚠️",
            "Low Stock",
            "0"
        )

        self.low_stock_card.grid(
            row=0,
            column=2,
            padx=12
        )

        self.suppliers_card = DashboardCard(
            cards_frame,
            "🚚",
            "Suppliers",
            "0"
        )

        self.suppliers_card.grid(
            row=0,
            column=3,
            padx=12
        )

    # ==========================================
# Success Message
# ==========================================

    def show_message(self, message):

        popup = ctk.CTkToplevel(self.root)

        popup.title("Success")

        popup.geometry("350x150")

        popup.resizable(False, False)

        popup.grab_set()

        label = ctk.CTkLabel(
            popup,
            text=message,
            font=("Segoe UI", 18, "bold")
        )

        label.pack(
            pady=30
        )

        button = ctk.CTkButton(
            popup,
            text="OK",
            command=popup.destroy
        )

        button.pack(
            pady=10
        )
    # Run Application
    

    def run(self):

        self.root.mainloop()