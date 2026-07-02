import customtkinter as ctk


class ExportDialog(ctk.CTkToplevel):

    def __init__(self, parent):

        super().__init__(parent)

        self.title("Export Report")

        self.geometry("350x250")

        self.resizable(False, False)

        self.grab_set()

        self.export_type = ctk.StringVar(value="Excel")

        title = ctk.CTkLabel(
            self,
            text="Choose Export Format",
            font=("Segoe UI", 20, "bold")
        )

        title.pack(pady=(20, 15))

        self.csv = ctk.CTkRadioButton(
            self,
            text="CSV",
            variable=self.export_type,
            value="CSV"
        )

        self.csv.pack(pady=5)

        self.excel = ctk.CTkRadioButton(
            self,
            text="Excel",
            variable=self.export_type,
            value="Excel"
        )

        self.excel.pack(pady=5)

        self.pdf = ctk.CTkRadioButton(
            self,
            text="PDF",
            variable=self.export_type,
            value="PDF"
        )

        self.pdf.pack(pady=5)

        self.export_btn = ctk.CTkButton(
            self,
            text="Export"
        )

        self.export_btn.pack(
            pady=20
        )