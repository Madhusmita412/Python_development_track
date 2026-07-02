import customtkinter as ctk

from ui.header import Header
from ui.toolbar import Toolbar
from ui.inventory_table import InventoryTable
from ui.product_dialog import ProductDialog

class InventoryPage(ctk.CTkFrame):

    def __init__(self, parent,processor):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )
        self.processor = processor
        self.create_page()

    
    # CREATE INVENTORY PAGE
    

    def create_page(self):

        # Header

        self.header = Header(self)

        self.header.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Title Card

        title_card = ctk.CTkFrame(
            self,
            fg_color="#1E293B",
            height=100,
            corner_radius=20
        )

        title_card.pack(
            fill="x",
            padx=25,
            pady=(0,20)
        )

        title_card.pack_propagate(False)

        title = ctk.CTkLabel(
            title_card,
            text="📦 Inventory Management",
            font=("Segoe UI",28,"bold")
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(18,5)
        )

        subtitle = ctk.CTkLabel(
            title_card,
            text="Manage products, stock, suppliers and inventory records.",
            font=("Segoe UI",15),
            text_color="gray80"
        )

        subtitle.pack(
            anchor="w",
            padx=25
        )

        # Quick Action Buttons

        action_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        action_frame.pack(
            fill="x",
            padx=25,
            pady=(0,20)
        )

        self.add_btn = ctk.CTkButton(
            action_frame,
            text="➕ Add Product",
            width=140,
            fg_color="#10B981"
        )

        self.add_btn.pack(
            side="left",
            padx=5
        )

        self.add_btn.configure(
            command=self.add_product
        )

        self.edit_btn = ctk.CTkButton(
            action_frame,
            text="✏ Edit Product",
            width=140,
            fg_color="#F59E0B"
        )

        self.edit_btn.pack(
            side="left",
            padx=5
        )

        self.delete_btn = ctk.CTkButton(
            action_frame,
            text="🗑 Delete Product",
            width=150,
            fg_color="#EF4444"
        )

        self.delete_btn.pack(
            side="left",
            padx=5
        )

        self.import_btn = ctk.CTkButton(
            action_frame,
            text="📂 Import CSV",
            width=140,
            fg_color="#2563EB"
        )

        self.import_btn.pack(
            side="right",
            padx=5
        )

        # Toolbar

        self.toolbar = Toolbar(self)

        self.toolbar.pack(
            fill="x",
            padx=25,
            pady=(0,20)
        )

        # Inventory Table

        self.table = InventoryTable(self)

        self.table.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0,20)
        )

    
    # LOAD DATA

    def load_data(self, dataframe):

        self.table.load_data(dataframe)

   
# Add Product


    def add_product(self):

        dialog = ProductDialog(self)

        self.wait_window(dialog)

        if dialog.result is None:
            return

        self.processor.add_product(
            dialog.result
        )

        self.table.load_data(
            self.processor.df
        )