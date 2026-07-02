import customtkinter as ctk

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DashboardCharts(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=20,
            height=650
        )

        self.figures = {}
        self.axes = {}
        self.canvases = {}

        self.create_layout()

    # =====================================================
    # Create Layout
    # =====================================================

    def create_layout(self):

        title = ctk.CTkLabel(
            self,
            text="Business Analytics Dashboard",
            font=("Segoe UI", 22, "bold")
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        charts_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        charts_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        charts_frame.grid_columnconfigure(0, weight=1)
        charts_frame.grid_columnconfigure(1, weight=1)
        charts_frame.grid_rowconfigure(
            0,
            weight=1,
            minsize=260
        )

        charts_frame.grid_rowconfigure(
            1,
            weight=1,
            minsize=260
        )

        self.create_chart_frame(
            charts_frame,
            "Inventory Value by Category"
        ).grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.create_chart_frame(
            charts_frame,
            "Stock Distribution"
        ).grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.create_chart_frame(
            charts_frame,
            "Products per Supplier"
        ).grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.create_chart_frame(
            charts_frame,
            "Low Stock Products"
        ).grid(row=1, column=1, padx=10, pady=10, sticky="nsew")

    # =====================================================
    # Create Single Chart
    # =====================================================

    def create_chart_frame(self, parent, chart_name):
        frame = ctk.CTkFrame(
            parent,
            fg_color="#0F172A",
            corner_radius=15,
            height=260
        )

        frame.grid_propagate(False)
        frame.pack_propagate(False)

        label = ctk.CTkLabel(
            frame,
            text=chart_name,
            font=("Segoe UI", 16, "bold")
        )

        label.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )

        figure = Figure(
            figsize=(5,3.8),
            dpi=100
        )

        figure.patch.set_facecolor("#0F172A")

        ax = figure.add_subplot(111)

        ax.set_facecolor("#0F172A")

        ax.tick_params(colors="white")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")

        canvas = FigureCanvasTkAgg(
            figure,
            master=frame
        )

        canvas.draw()

        canvas_widget = canvas.get_tk_widget()

        canvas_widget.configure(
            height=170
        )

        canvas_widget.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(5,10)
        )

        self.figures[chart_name] = figure
        self.axes[chart_name] = ax
        self.canvases[chart_name] = canvas

        return frame

    # =====================================================
    # Update Dashboard
    # =====================================================

    def update_dashboard(self, dataframe):

        if dataframe.empty:
            return

        self.plot_inventory_value(dataframe)
        self.plot_stock_distribution(dataframe)
        self.plot_supplier_products(dataframe)
        self.plot_low_stock(dataframe)

        self.update_idletasks()

    # =====================================================
    # Inventory Value Chart
    # =====================================================

    def plot_inventory_value(self, dataframe):

        ax = self.axes["Inventory Value by Category"]

        ax.clear()

        values = (
            dataframe.groupby("Category")
            .apply(lambda x: (x["Stock"] * x["Price"]).sum())
        )

        ax.bar(
            values.index,
            values.values
        )

        ax.set_title(
            "Inventory Value",
            color="white"
        )

        ax.tick_params(
            axis="x",
            rotation=20,
            colors="white"
        )

        ax.tick_params(
            axis="y",
            colors="white"
        )

        ax.set_facecolor("#0F172A")

        self.canvases["Inventory Value by Category"].draw()

    # =====================================================
    # Stock Distribution
    # =====================================================

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

    # =====================================================
    # Supplier Chart
    # =====================================================

    def plot_supplier_products(self, dataframe):

        ax = self.axes["Products per Supplier"]

        ax.clear()

        suppliers = dataframe.groupby("Supplier").size()

        ax.plot(
            suppliers.index,
            suppliers.values,
            marker="o"
        )

        ax.set_title(
            "Products per Supplier",
            color="white"
        )

        ax.tick_params(
            axis="x",
            rotation=20,
            colors="white"
        )

        ax.tick_params(
            axis="y",
            colors="white"
        )

        ax.set_facecolor("#0F172A")

        self.canvases["Products per Supplier"].draw()

    # =====================================================
    # Low Stock Chart
    # =====================================================

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

        ax.tick_params(colors="white")

        ax.set_facecolor("#0F172A")

        self.canvases["Low Stock Products"].draw()