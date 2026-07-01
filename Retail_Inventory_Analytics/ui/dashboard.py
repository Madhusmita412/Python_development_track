from turtle import title
from matplotlib.pylab import rint
import pandas as pd
from tkinter import filedialog
import customtkinter as ctk
from tkinter import ttk

from ui.sidebar import Sidebar
from ui.header import Header
from ui.cards import DashboardCard
from ui.toolbar import Toolbar



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

        # Build UI
        self.create_layout()


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

        self.create_cards()

        # Toolbar

        self.toolbar = Toolbar(self.main_frame)

        self.toolbar.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Inventory Table

        self.create_table()


       


    
# Inventory Table

    def create_table(self):

        table_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.card_color,
            corner_radius=20
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

    #Title 

        title = ctk.CTkLabel(
           table_frame,
            text="Inventory Data",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=20
        )

    # Columns

        columns = (

            "Product ID",

            "Product Name",

            "Category",

            "Supplier",

            "Stock",

            "Price",

            "Status"

        )

        self.tree = ttk.Treeview(
        table_frame,
        columns=columns,
        show="headings",
        height=15
        )

    #Headings 

        for column in columns:
            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=170,
                anchor="center"
            )

    #Scrollbar

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(20, 0),
            pady=(0, 20)
        )

        scrollbar.pack(
            side="right",
            fill="y",
            padx=(0, 20),
            pady=(0, 20)
        )

    #Sample Data

        sample_data = [

            (
                "Laptop",
                "Electronics",
                20,
                "₹65000",
                "Dell",
                "In Stock"
            ),

            (
                "Mouse",
                "Accessories",
                120,
                "₹499",
                "Logitech",
                "In Stock"
            ),

            (
                "Keyboard",
                "Accessories",
                10,
                "₹1200",
                "Logitech",
                "Low Stock"
            )

        ]

    #Insert Data

        for row in sample_data:

            self.tree.insert(
                "",
                "end",
                values=row
    
         )
            
    def upload_csv(self):

        file_path = filedialog.askopenfilename(
        title="Select Inventory CSV",
        filetypes=[("CSV Files","*.csv")]

    )

        if file_path:
            self.load_csv(file_path)
    
    def load_csv(self, file_path):

        import pandas as pd

        df = pd.read_csv(file_path)

    # Calculate Dashboard KPIs

        total_products = len(df)

        inventory_value = (df["Stock"] * df["Price"]).sum()

        low_stock = len(df[df["Stock"] <= df["Reorder Level"]])

        total_suppliers = df["Supplier"].nunique()


# Update Dashboard Card=

        self.products_card.update_value(str(total_products))

        self.inventory_card.update_value(f"₹{inventory_value:,.0f}")

        self.low_stock_card.update_value(str(low_stock))

        self.suppliers_card.update_value(str(total_suppliers))


        # Clear Previous Table Data

        for item in self.tree.get_children():
            self.tree.delete(item)

        # Insert CSV Data into Table

        for _, row in df.iterrows():

            self.tree.insert(
                "",
                "end",
                values=(
                    row["Product ID"],

                    row["Product Name"],

                    row["Category"],

                    row["Supplier"],

                    row["Stock"],

                    f"₹{row['Price']}",

                    row["Status"]

                )
        )
            
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
            "⚠",
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
    
    # Run
    
    def run(self):

        self.root.mainloop()