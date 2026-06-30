from turtle import title
from matplotlib.pylab import rint
import pandas as pd
from tkinter import filedialog
import customtkinter as ctk
from tkinter import ttk

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
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=240,
            corner_radius=0,
            fg_color=self.sidebar_color
        )

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

        self.create_sidebar()

        self.create_header()

        # Sidebar
    
    def create_sidebar(self):

        title = ctk.CTkLabel(
            self.sidebar,
            text="🏪 Inventory Pro",
            font=("Segoe UI", 28, "bold")
        )

        title.pack(
            pady=(30, 40)
        )

        menu_items = [

            "📊 Dashboard",

            "📦 Inventory",

            "📈 Analytics",

            "📄 Reports",

            "⚙ Settings"

        ]

        for item in menu_items:

            btn = ctk.CTkButton(

                self.sidebar,

                text=item,

                width=190,

                height=45,

                fg_color="transparent",

                hover_color="#2563EB",

                anchor="w",

                font=("Segoe UI", 15)

            )

            btn.pack(
                pady=8,
                padx=20
            )

        # Header
    
    def create_header(self):

        header = ctk.CTkFrame(
            self.main_frame,
            height=90,
            fg_color=self.card_color,
            corner_radius=15
        )

        header.pack(
            fill="x",
            padx=25,
            pady=20
        )

        left = ctk.CTkFrame(
            header,
            fg_color="transparent"
        )

        left.pack(
            side="left",
            padx=20,
            pady=15
        )

        dashboard_title = ctk.CTkLabel(

            left,

            text="Retail Inventory Analytics Dashboard",

            font=("Segoe UI", 28, "bold")

        )

        dashboard_title.pack(anchor="w")

        subtitle = ctk.CTkLabel(

            left,

            text="Inventory Management & Business Intelligence Platform",

            text_color="lightgray",

            font=("Segoe UI", 15)

        )

        subtitle.pack(anchor="w")

        user = ctk.CTkLabel(

            header,

            text="👤 Admin",

            font=("Segoe UI", 16)

        )

        user.pack(
            side="right",
            padx=25
        )

        # Welcome Card

        welcome = ctk.CTkFrame(
            self.main_frame,
            height=120,
            fg_color=self.card_color
        )

        welcome.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

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

            text="Monitor inventory, analyze stock levels, and generate business insights from one dashboard.",

            font=("Segoe UI", 15),

            text_color="lightgray"

        )

        welcome_text.pack(
            anchor="w",
            padx=25
        )

        self.create_kpi_cards()

        self.create_toolbar()


       
#KPI Cards
    def create_kpi_cards(self):

        cards_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        cards_frame.pack(
            fill="x",
            padx=25,
            pady=(0, 20)
        )

        self.product_card = self.create_card(
            cards_frame,
            "📦",
            "Products",
            "0",
            0
        )

        self.inventory_card = self.create_card(
            cards_frame,
            "💰",
            "Inventory Value",
            "₹0",
            1
        )

        self.low_stock_card = self.create_card(
            cards_frame,
            "⚠",
            "Low Stock",
            "0",
            2
        )

        self.supplier_card = self.create_card(
            cards_frame,
            "🚚",
            "Suppliers",
            "0",
            3
        )
    


# Reusable Dashboard Card
    def create_card(
        self,
       parent,
       icon,
       title,
       value,
       column
    ):
        card = ctk.CTkFrame(
        parent,
        width=250,
        height=140,
        fg_color=self.card_color,
        corner_radius=20,
        border_width=1,
        border_color="#334155"
        )

        card.grid(
            row=0,
            column=column,
            padx=12
        )

        card.grid_propagate(False)

        icon_label = ctk.CTkLabel(
            card,
            text=icon,
            font=("Segoe UI",32)
        )

        icon_label.pack(
            pady=(15,5)
        )

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Segoe UI",16)
        )
    

        title_label.pack()

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Segoe UI",30,"bold")
        )

        value_label.pack(
            pady=(5,10)
       )

        return value_label

# Toolbar


    def create_toolbar(self):
        toolbar = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.card_color,
            corner_radius=20,
            height=110
        )

        toolbar.pack(
            fill="x",
            padx=25,
            pady=(10,20)
        )

        toolbar.pack_propagate(False)

        search = ctk.CTkEntry(
            toolbar,
            width=320,
            height=42,
            placeholder_text="🔍 Search Product..."
        )

        search.pack(
            side="left",
            padx=20
        )

        upload = ctk.CTkButton(
            toolbar,
            text="📂 Upload CSV",
            width=150,
            command=self.upload_csv
        )

        upload.pack(
            side="left",
            padx=10
        )

        clean_btn = ctk.CTkButton(
            toolbar,
            text="🧹 Clean",
            width=150,
            height=42
        )

        clean_btn.pack(
            side="left",
            padx=10
        )

        analyze_btn = ctk.CTkButton(
            toolbar,
            text="📊 Analyze",
            width=150,
            height=42
        )

        analyze_btn.pack(
            side="left",
            padx=10
        )

        export_btn = ctk.CTkButton(
            toolbar,
            text="📤 Export",
            width=150,
            height=42
        )

        export_btn.pack(
            side="left",
            padx=10
        )

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
            "Product",
            "Category",
            "Stock",
            "Price",
            "Supplier",
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

        df = pd.read_csv(file_path)

        print(df)
        for item in self.tree.get_children():

             self.tree.delete(item) 
        
        for index, row in df.iterrows():

            self.tree.insert(

                "",

                "end",

                values=(

                row["Product"],

                row["Category"],

                row["Stock"],

                row["Price"],

                row["Supplier"],

                row["Status"]

                )

            )

    # Run
    
    def run(self):

        self.root.mainloop()