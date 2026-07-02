import customtkinter as ctk


class ReportCard(ctk.CTkFrame):

    def __init__(self, parent, title, description, button_text, color):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=18
        )

        self.configure(height=180)

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 20, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 8)
        )

        desc = ctk.CTkLabel(
            self,
            text=description,
            justify="left",
            wraplength=260,
            text_color="gray80",
            font=("Segoe UI", 13)
        )

        desc.pack(
            anchor="w",
            padx=20
        )

        self.button = ctk.CTkButton(
            self,
            text=button_text,
            width=140,
            fg_color=color
        )

        self.button.pack(
            anchor="w",
            padx=20,
            pady=20
        )


class ReportsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )

        self.create_page()

   

    def create_page(self):

        header = ctk.CTkLabel(
            self,
            text="📄 Reports & Export Center",
            font=("Segoe UI", 30, "bold")
        )

        header.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Generate professional business reports for inventory management.",
            font=("Segoe UI", 15),
            text_color="gray80"
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0, 20)
        )

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        for i in range(2):
            container.grid_columnconfigure(i, weight=1)

        # CSV

        self.csv = ReportCard(
            container,
            "📄 CSV Report",
            "Export the complete inventory into a CSV file for Excel or other software.",
            "Export CSV",
            "#2563EB"
        )

        self.csv.grid(
            row=0,
            column=0,
            padx=15,
            pady=15,
            sticky="ew"
        )

        # Excel

        self.excel = ReportCard(
            container,
            "📊 Excel Report",
            "Generate a formatted Excel workbook with all inventory records.",
            "Export Excel",
            "#10B981"
        )

        self.excel.grid(
            row=0,
            column=1,
            padx=15,
            pady=15,
            sticky="ew"
        )

        # PDF

        self.pdf = ReportCard(
            container,
            "📑 PDF Report",
            "Generate a printable professional PDF inventory report.",
            "Export PDF",
            "#EF4444"
        )

        self.pdf.grid(
            row=1,
            column=0,
            padx=15,
            pady=15,
            sticky="ew"
        )

        # Dashboard Summary

        self.summary = ReportCard(
            container,
            "📈 Dashboard Summary",
            "Generate a complete business summary including charts and KPIs.",
            "Generate Report",
            "#8B5CF6"
        )

        self.summary.grid(
            row=1,
            column=1,
            padx=15,
            pady=15,
            sticky="ew"
        )