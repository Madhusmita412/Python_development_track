import pandas as pd


class InventoryAnalytics:

    def __init__(self, dataframe: pd.DataFrame):

        self.df = dataframe

   
    # Inventory Value by Category
   

    def inventory_value_by_category(self):

        if self.df.empty:
            return pd.Series(dtype=float)

        category_value = self.df.copy()

        category_value["Inventory Value"] = (
            category_value["Stock"] *
            category_value["Price"]
        )

        return category_value.groupby(
            "Category"
        )["Inventory Value"].sum()

   
    # Stock Status Count
   

    def stock_status_distribution(self):

        if self.df.empty:
            return pd.Series(dtype=int)

        return self.df["Status"].value_counts()

   
    # Supplier Distribution
   

    def supplier_distribution(self):

        if self.df.empty:
            return pd.Series(dtype=int)

        return self.df["Supplier"].value_counts()

   
    # Top 10 Highest Value Products
   

    def top_inventory_products(self):

        if self.df.empty:
            return pd.DataFrame()

        temp = self.df.copy()

        temp["Inventory Value"] = (
            temp["Stock"] *
            temp["Price"]
        )

        return temp.sort_values(
            by="Inventory Value",
            ascending=False
        ).head(10)

   
    # Low Stock Products
   

    def low_stock_products(self):

        if self.df.empty:
            return pd.DataFrame()

        return self.df[
            self.df["Stock"] <=
            self.df["Reorder Level"]
        ]

   
    # Total Inventory Value
   

    def total_inventory_value(self):

        if self.df.empty:
            return 0

        return (
            self.df["Stock"] *
            self.df["Price"]
        ).sum()

   
    # Total Products
   

    def total_products(self):

        return len(self.df)

   
    # Total Suppliers
   

    def total_suppliers(self):

        if self.df.empty:
            return 0

        return self.df["Supplier"].nunique()

   
    # Low Stock Count
   

    def low_stock_count(self):

        if self.df.empty:
            return 0

        return len(
            self.df[
                self.df["Stock"] <=
                self.df["Reorder Level"]
            ]
        )

   
    # Category Summary
   

    def category_summary(self):

        if self.df.empty:
            return pd.DataFrame()

        return self.df.groupby("Category").agg({

            "Stock": "sum",

            "Price": "mean"

        })

   
    # Supplier Summary
   

    def supplier_summary(self):

        if self.df.empty:
            return pd.DataFrame()

        return self.df.groupby("Supplier").agg({

            "Stock": "sum",

            "Price": "mean"

        })