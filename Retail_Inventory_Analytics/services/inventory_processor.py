import pandas as pd


class InventoryProcessor:

    def __init__(self):

        # Initialize an empty DataFrame
        self.df = pd.DataFrame()

    
    # Load CSV
    

    def load_csv(self, file_path):

        self.df = pd.read_csv(file_path)

        return self.df

    
    # Clean Data
    

    def clean_data(self):

        if self.df.empty:
            return self.df

        # Remove duplicate rows
        self.df.drop_duplicates(inplace=True)

        # Remove rows where all values are missing
        self.df.dropna(how="all", inplace=True)

        # Fill missing values
        self.df.fillna({

            "Product Name": "Unknown Product",

            "Category": "Unknown",

            "Supplier": "Unknown",

            "Stock": 0,

            "Price": 0,

            "Reorder Level": 0,

            "Status": "Unknown"

        }, inplace=True)

        # Convert numeric columns
        numeric_columns = [

            "Stock",

            "Price",

            "Reorder Level"

        ]

        for column in numeric_columns:

            self.df[column] = pd.to_numeric(
                self.df[column],
                errors="coerce"
            ).fillna(0)

        return self.df

    
    # Dashboard KPIs
    

    def calculate_kpis(self):

        if self.df.empty:

            return {

                "products": 0,

                "inventory_value": 0,

                "low_stock": 0,

                "suppliers": 0

            }

        total_products = len(self.df)

        inventory_value = (

            self.df["Stock"] *

            self.df["Price"]

        ).sum()

        low_stock = len(

            self.df[
                self.df["Stock"] <=
                self.df["Reorder Level"]
            ]

        )

        suppliers = self.df["Supplier"].nunique()

        return {

            "products": total_products,

            "inventory_value": inventory_value,

            "low_stock": low_stock,

            "suppliers": suppliers

        }

    
    # Search Products
    

    def search(self, keyword):

        if self.df.empty:
            return self.df

        keyword = keyword.lower()

        return self.df[

            self.df["Product Name"]
            .astype(str)
            .str.lower()
            .str.contains(keyword)

            |

            self.df["Product ID"]
            .astype(str)
            .str.lower()
            .str.contains(keyword)

            |

            self.df["Supplier"]
            .astype(str)
            .str.lower()
            .str.contains(keyword)

            |

            self.df["Category"]
            .astype(str)
            .str.lower()
            .str.contains(keyword)

        ]

    
    # Filter Category
    

    def filter_category(self, category):

        if self.df.empty:
            return self.df

        if category == "All Categories":
            return self.df

        return self.df[
            self.df["Category"] == category
        ]

    
    # Filter Status
    

    def filter_status(self, status):

        if self.df.empty:
            return self.df

        if status == "All Status":
            return self.df

        return self.df[
            self.df["Status"] == status
        ]

    
    # Total Inventory Value
    

    def total_inventory_value(self):

        if self.df.empty:
            return 0

        return (

            self.df["Stock"] *

            self.df["Price"]

        ).sum()

    
    # Get Categories
    

    def get_categories(self):

        if self.df.empty:
            return ["All Categories"]

        categories = sorted(

            self.df["Category"]
            .dropna()
            .unique()
            .tolist()

        )

        return ["All Categories"] + categories

    
    # Get Suppliers
    

    def get_suppliers(self):

        if self.df.empty:
            return []

        return sorted(

            self.df["Supplier"]
            .dropna()
            .unique()
            .tolist()

        )

    
    # Refresh Data
    

    def refresh(self):

        self.df = self.df.copy()

        return self.df