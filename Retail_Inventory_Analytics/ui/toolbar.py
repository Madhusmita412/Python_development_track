import customtkinter as ctk


class Toolbar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            height=90,
            corner_radius=20,
            fg_color="#1E293B"
        )

        self.pack_propagate(False)

        self.create_toolbar()

    
    # Toolbar
    
    def create_toolbar(self):

        #Left Section

        left_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        left_frame.pack(
            side="left",
            padx=20,
            pady=20
        )

        # Search Box

        self.search = ctk.CTkEntry(
            left_frame,
            width=320,
            height=42,
            placeholder_text="🔍 Search by Product ID, Name or Supplier..."
        )

        self.search.pack(
            side="left",
            padx=(0, 12)
        )

        # Category Filter

        self.category = ctk.CTkOptionMenu(
            left_frame,
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
            width=170,
            height=40
        )

        self.category.set("All Categories")

        self.category.pack(
            side="left",
            padx=8
        )

        # Status Filter

        self.status = ctk.CTkOptionMenu(
            left_frame,
            values=[
                "All Status",
                "In Stock",
                "Low Stock",
                "Out of Stock"
            ],
            width=150,
            height=40
        )

        self.status.set("All Status")

        self.status.pack(
            side="left",
            padx=8
        )

        #Right Section

        right_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        right_frame.pack(
            side="right",
            padx=20,
            pady=20
        )

        # Refresh Button

        self.refresh_btn = ctk.CTkButton(
            right_frame,
            text="🔄 Refresh",
            width=110,
            fg_color="#475569",
            hover_color="#334155"
        )
        

        self.refresh_btn.pack(
            side="right",
            padx=5
        )

        # Export Button

        self.export_btn = ctk.CTkButton(
            right_frame,
            text="📤 Export",
            width=110,
            fg_color="#F59E0B",
            hover_color="#D97706"
        )

        self.export_btn.pack(
            side="right",
            padx=5
        )

        # Analyze Button

        self.analyze_btn = ctk.CTkButton(
            right_frame,
            text="📊 Analyze",
            width=110,
            fg_color="#10B981",
            hover_color="#059669"
        )

        self.analyze_btn.pack(
            side="right",
            padx=5
        )

        # Clean Button

        self.clean_btn = ctk.CTkButton(
            right_frame,
            text="🧹 Clean",
            width=110,
            fg_color="#EF4444",
            hover_color="#DC2626"
        )

        self.clean_btn.pack(
            side="right",
            padx=5
        )

        # Upload Button

        self.upload_btn = ctk.CTkButton(
            right_frame,
            text="📂 Upload CSV",
            width=130,
            fg_color="#2563EB",
            hover_color="#1D4ED8"
        )

        self.upload_btn.pack(
            side="right",
            padx=5
        )