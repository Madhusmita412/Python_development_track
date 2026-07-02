import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardCharts(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=20
        )

        self.pack_propagate(False)
        self.figures = {}
        self.axes = {}
        self.canvases = {}
        self.create_layout()

    # ==========================================
    # Create Layout
    # ==========================================

    def create_layout(self):

        title = ctk.CTkLabel(
            self,
            text="Business Analytics Dashboard",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20,10)
        )

        charts_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        charts_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0,20)
        )

        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        charts_frame.grid_rowconfigure(0, weight=1)
        charts_frame.grid_rowconfigure(1, weight=1)

        # Chart 1
        self.chart1 = self.create_chart_frame(
            charts_frame,
            "Inventory Value by Category"
        )
        self.chart1.grid(row=0,column=0,padx=10,pady=10,sticky="nsew")

        # Chart 2
        self.chart2 = self.create_chart_frame(
            charts_frame,
            "Stock Distribution"
        )
        self.chart2.grid(row=0,column=1,padx=10,pady=10,sticky="nsew")

        # Chart 3
        self.chart3 = self.create_chart_frame(
            charts_frame,
            "Products per Supplier"
        )
        self.chart3.grid(row=1,column=0,padx=10,pady=10,sticky="nsew")

        # Chart 4
        self.chart4 = self.create_chart_frame(
            charts_frame,
            "Low Stock Products"
        )
        self.chart4.grid(row=1,column=1,padx=10,pady=10,sticky="nsew")

        # ==========================================
    # Create Individual Chart Frame
    # ==========================================

    def create_chart_frame(self, parent, title):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#0F172A",
            corner_radius=15
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 16, "bold")
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(12, 5)
        )

        figure = Figure(
            figsize=(5, 3),
            dpi=100
        )

        figure.patch.set_facecolor("#0F172A")

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0F172A")

        # Axis Styling

        ax.tick_params(
            colors="white"
        )

        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_color("#0F172A")
        ax.spines["right"].set_color("#0F172A")

        canvas = FigureCanvasTkAgg(
            figure,
            master=frame
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # Save references

        self.figures[title] = figure
        self.axes[title] = ax
        self.canvases[title] = canvas
        return frame    
            

        # ==========================================
    # Update All Charts
    # ==========================================

    def update_dashboard(self, dataframe):

        self.plot_inventory_value(dataframe)
        self.plot_stock_distribution(dataframe)
        self.plot_supplier_products(dataframe)
        self.plot_low_stock(dataframe)

    # ==========================================
    # Chart 1 - Inventory Value by Category
    # ==========================================

    def plot_inventory_value(self, dataframe):

        ax = self.axes["Inventory Value by Category"]
        ax.clear()

        values = (
            dataframe.groupby("Category")
            .apply(lambda x: (x["Stock"] * x["Price"]).sum())
            .sort_values(ascending=False)
        )

        ax.bar(
            values.index,
            values.values
        )

        ax.set_title("Inventory Value", color="white")

        ax.tick_params(axis="x", rotation=25, colors="white")
        ax.tick_params(axis="y", colors="white")

        ax.set_facecolor("#0F172A")

        self.canvases["Inventory Value by Category"].draw()

    # ==========================================
    # Chart 2 - Stock Distribution
    # ==========================================

    def plot_stock_distribution(self, dataframe):

        ax = self.axes["Stock Distribution"]
        ax.clear()

        stock = dataframe.groupby("Category")["Stock"].sum()

        ax.pie(
            stock.values,
            labels=stock.index,
            autopct="%1.1f%%",
            startangle=90
        )

        ax.set_title("Stock Distribution")

        self.canvases["Stock Distribution"].draw()

    # ==========================================
    # Chart 3 - Products per Supplier
    # ==========================================

    def plot_supplier_products(self, dataframe):

        ax = self.axes["Products per Supplier"]

        ax.clear()

        suppliers = dataframe.groupby("Supplier").size()

        ax.plot(
            suppliers.index,
            suppliers.values,
            marker="o",
            linewidth=2
        )

        ax.set_title(
            "Products per Supplier",
            color="white"
        )

        ax.tick_params(
            axis="x",
            rotation=25,
            colors="white"
        )

        ax.tick_params(
            axis="y",
            colors="white"
        )

        ax.set_facecolor("#0F172A")

        self.canvases["Products per Supplier"].draw()

    # ==========================================
    # Chart 4 - Low Stock Products
    # ==========================================

    def plot_low_stock(self, dataframe):

        ax = self.axes["Low Stock Products"]

        ax.clear()

        low = dataframe[
            dataframe["Stock"] <= dataframe["Reorder Level"]
        ]

        if not low.empty:

            ax.barh(
                low["Product Name"],
                low["Stock"]
            )

        ax.set_title(
            "Low Stock Products",
            color="white"
        )

        ax.tick_params(
            axis="x",
            colors="white"
        )

        ax.tick_params(
            axis="y",
            colors="white"
        )

        ax.set_facecolor("#0F172A")

        self.canvases["Low Stock Products"].draw()