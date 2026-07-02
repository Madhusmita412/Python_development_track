import customtkinter as ctk
from tkinter import ttk


class InventoryTable(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=20
        )

        self.configure(height=500)

        self.create_table()

    
    # Inventory Table
    

    def create_table(self):

        # Title

        title = ctk.CTkLabel(
            self,
            text="Inventory Data",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # Table Frame

        table_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        # Treeview Style

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(

            "Treeview",

            background="#1F2937",

            foreground="white",

            fieldbackground="#1F2937",

            rowheight=35,

            font=("Segoe UI", 11)

        )

        style.configure(

            "Treeview.Heading",

            background="#2563EB",

            foreground="white",

            font=("Segoe UI", 12, "bold")

        )

        style.map(

            "Treeview",

            background=[("selected", "#3B82F6")]

        )

        # Columns

        columns = (

            "Product ID",

            "Product Name",

            "Category",

            "Supplier",

            "Stock",

            "Price",

            "Reorder Level",

            "Status"

        )

        self.tree = ttk.Treeview(

            table_frame,

            columns=columns,

            show="headings",

            height=15

        )

        # Headings

        for column in columns:

            self.tree.heading(
                column,
                text=column
            )

            self.tree.column(
                column,
                width=150,
                anchor="center"
            )

        # Scrollbars

        vertical_scroll = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal_scroll = ttk.Scrollbar(
            table_frame,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical_scroll.set,
            xscrollcommand=horizontal_scroll.set
        )

        # Layout

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical_scroll.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal_scroll.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        table_frame.grid_rowconfigure(
            0,
            weight=1
        )

        table_frame.grid_columnconfigure(
            0,
            weight=1
        )

    
    # Load Inventory Data
    

    def load_data(self, dataframe):

    # Clear Existing Data
        self.clear_table()

        if dataframe.empty:
            return

        # Insert New Data
        for _, row in dataframe.iterrows():

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

                    row["Reorder Level"],

                    row["Status"]

                )

    )

    
    # Clear Table
    

    def clear_table(self):

        for row in self.tree.get_children():

            self.tree.delete(row)