import customtkinter as ctk


class Toolbar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=90,
            corner_radius=15,
            fg_color="#1E293B"
        )

        self.pack_propagate(False)

        self.create_toolbar()

    def create_toolbar(self):

        # Search Box

        self.search = ctk.CTkEntry(
            self,
            width=320,
            height=40,
            placeholder_text="🔍 Search Product..."
        )

        self.search.pack(
            side="left",
            padx=20
        )

        # Category Dropdown

        self.category = ctk.CTkOptionMenu(
            self,
            values=[
                "All Categories",
                "Electronics",
                "Accessories",
                "Office",
                "Furniture",
                "Networking",
                "Storage",
                "Components"
            ],
            width=180
        )

        self.category.pack(
            side="left",
            padx=10
        )

        # Status Dropdown

        self.status = ctk.CTkOptionMenu(
            self,
            values=[
                "All Status",
                "In Stock",
                "Low Stock",
                "Out of Stock"
            ],
            width=150
        )

        self.status.pack(
            side="left",
            padx=10
        )

        # Upload Button

        self.upload_btn = ctk.CTkButton(
            self,
            text="📂 Upload CSV",
            width=140
        )

        self.upload_btn.pack(
            side="right",
            padx=8
        )

        # Analyze Button

        self.analyze_btn = ctk.CTkButton(
            self,
            text="📊 Analyze",
            width=120
        )

        self.analyze_btn.pack(
            side="right",
            padx=8
        )

        # Export Button

        self.export_btn = ctk.CTkButton(
            self,
            text="📤 Export",
            width=120
        )

        self.export_btn.pack(
            side="right",
            padx=8
        )