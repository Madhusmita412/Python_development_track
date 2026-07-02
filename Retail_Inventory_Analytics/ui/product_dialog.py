import customtkinter as ctk


class ProductDialog(ctk.CTkToplevel):

    def __init__(self, parent, title="Add Product"):

        super().__init__(parent)

        self.title(title)

        self.geometry("500x620")

        self.resizable(False, False)

        self.grab_set()

        self.result = None

        self.create_widgets()

    # =====================================

    def create_widgets(self):

        title = ctk.CTkLabel(

            self,

            text="Inventory Product",

            font=("Segoe UI",24,"bold")

        )

        title.pack(

            pady=20

        )

        self.product_id = ctk.CTkEntry(

            self,

            placeholder_text="Product ID"

        )

        self.product_id.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.product_name = ctk.CTkEntry(

            self,

            placeholder_text="Product Name"

        )

        self.product_name.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.category = ctk.CTkEntry(

            self,

            placeholder_text="Category"

        )

        self.category.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.supplier = ctk.CTkEntry(

            self,

            placeholder_text="Supplier"

        )

        self.supplier.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.stock = ctk.CTkEntry(

            self,

            placeholder_text="Stock"

        )

        self.stock.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.price = ctk.CTkEntry(

            self,

            placeholder_text="Price"

        )

        self.price.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.reorder = ctk.CTkEntry(

            self,

            placeholder_text="Reorder Level"

        )

        self.reorder.pack(

            fill="x",

            padx=30,

            pady=8

        )

        self.status = ctk.CTkOptionMenu(

            self,

            values=[

                "In Stock",

                "Low Stock",

                "Out of Stock"

            ]

        )

        self.status.pack(

            fill="x",

            padx=30,

            pady=8

        )

        save = ctk.CTkButton(

            self,

            text="💾 Save Product",

            command=self.save

        )

        save.pack(

            pady=25

        )

    # =====================================

    def save(self):

        self.result = {

            "Product ID": self.product_id.get(),

            "Product Name": self.product_name.get(),

            "Category": self.category.get(),

            "Supplier": self.supplier.get(),

            "Stock": self.stock.get(),

            "Price": self.price.get(),

            "Reorder Level": self.reorder.get(),

            "Status": self.status.get()

        }

        self.destroy()