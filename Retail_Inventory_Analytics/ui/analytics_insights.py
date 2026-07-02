import customtkinter as ctk


class InsightCard(ctk.CTkFrame):

    def __init__(self, parent, title, icon):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=18
        )

        self.configure(height=120)

        title_label = ctk.CTkLabel(
            self,
            text=f"{icon}  {title}",
            font=("Segoe UI", 16, "bold")
        )

        title_label.pack(
            anchor="w",
            padx=15,
            pady=(15, 5)
        )

        self.value = ctk.CTkLabel(
            self,
            text="Loading...",
            justify="left",
            wraplength=300,
            font=("Segoe UI", 13)
        )

        self.value.pack(
            anchor="w",
            padx=15,
            pady=(5, 15)
        )

    def update_text(self, text):

        self.value.configure(
            text=text
        )


class AnalyticsInsights(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.create_layout()

    

    def create_layout(self):

        title = ctk.CTkLabel(
            self,
            text="💡 Business Insights",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10, 20)
        )

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="x",
            expand=True
        )

        for i in range(2):
            container.grid_columnconfigure(i, weight=1)

        # Row 1

        self.inventory = InsightCard(
            container,
            "Inventory Summary",
            "📦"
        )

        self.inventory.grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.category = InsightCard(
            container,
            "Highest Value Category",
            "💰"
        )

        self.category.grid(
            row=0,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

        # Row 2

        self.supplier = InsightCard(
            container,
            "Top Supplier",
            "🚚"
        )

        self.supplier.grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="ew"
        )

        self.recommendation = InsightCard(
            container,
            "Smart Recommendation",
            "💡"
        )

        self.recommendation.grid(
            row=1,
            column=1,
            padx=10,
            pady=10,
            sticky="ew"
        )

    # =====================================================

    def update_insights(self, dataframe):

        if dataframe.empty:
            return

        inventory_value = (
            dataframe["Stock"] *
            dataframe["Price"]
        ).sum()

        total_products = len(dataframe)

        low_stock = len(
            dataframe[
                dataframe["Stock"] <= dataframe["Reorder Level"]
            ]
        )

        highest_category = (
            dataframe.assign(
                Value=dataframe["Stock"] * dataframe["Price"]
            )
            .groupby("Category")["Value"]
            .sum()
            .idxmax()
        )

        top_supplier = (
            dataframe.groupby("Supplier")
            .size()
            .idxmax()
        )

        self.inventory.update(
            f"""Total Products : {total_products}

                    Inventory Value : ₹{inventory_value:,.0f}
                    Low Stock Items : {low_stock}
            """

        )

                self.category.update(

                    f"""Highest Inventory Value

        {highest_category}"""

                )

                self.supplier.update(

                    f"""Most Products Supplied By

        {top_supplier}"""

                )

        if low_stock > 0:

            message = (
                f"{low_stock} products need restocking.\n"
                "Consider placing supplier orders this week."
            )

        else:

            message = (
                "Inventory levels look healthy.\n"
                "No immediate restocking required."
            )

        self.recommendation.update(message)