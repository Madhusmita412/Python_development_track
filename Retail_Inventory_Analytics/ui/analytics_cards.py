import customtkinter as ctk

from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

class AnalyticsCharts(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.figures = {}
        self.axes = {}
        self.canvases = {}

        self.create_layout()

    
    # MAIN LAYOUT
    

    def create_layout(self):

        title = ctk.CTkLabel(
            self,
            text="📊 Business Intelligence Charts",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(
            anchor="w",
            padx=10,
            pady=(10,20)
        )

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True
        )

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)
        container.grid_columnconfigure(2, weight=1)

        container.grid_rowconfigure(0, weight=1)
        container.grid_rowconfigure(1, weight=1)

        # -----------------------------

        self.create_chart(
            container,
            "Inventory Value",
            0,
            0
        )

        self.create_chart(
            container,
            "Stock Distribution",
            0,
            1
        )

        self.create_chart(
            container,
            "Revenue Trend",
            0,
            2
        )

        self.create_chart(
            container,
            "Supplier Comparison",
            1,
            0
        )

        self.create_chart(
            container,
            "Stock Trend",
            1,
            1
        )

        self.create_chart(
            container,
            "Category Share",
            1,
            2
        )

    
    # CREATE SINGLE CHART
    

    def create_chart(
        self,
        parent,
        title,
        row,
        column
    ):

        frame = ctk.CTkFrame(
            parent,
            fg_color="#1E293B",
            corner_radius=18
        )

        frame.grid(
            row=row,
            column=column,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        frame.grid_rowconfigure(
            1,
            weight=1
        )

        frame.grid_columnconfigure(
            0,
            weight=1
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI",16,"bold")
        )

        label.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=15
        )

        figure = Figure(
            figsize=(4,3),
            dpi=100
        )

        figure.patch.set_facecolor("#1E293B")

        ax = figure.add_subplot(111)

        ax.set_facecolor("#1E293B")

        ax.tick_params(
            colors="white"
        )

        ax.spines["bottom"].set_color("white")
        ax.spines["left"].set_color("white")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        canvas = FigureCanvasTkAgg(
            figure,
            frame
        )

        canvas.draw()

        canvas.get_tk_widget().grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=10,
            pady=(0,10)
        )

        self.figures[title] = figure
        self.axes[title] = ax
        self.canvases[title] = canvas

    
    # UPDATE ALL CHARTS
    

    def update_charts(self, dataframe):

        if dataframe.empty:
            return

            self.plot_inventory_value(dataframe)

            self.plot_stock_distribution(dataframe)

            self.plot_revenue_trend(dataframe)

            self.plot_supplier_comparison(dataframe)

            self.plot_stock_trend(dataframe)

            self.plot_category_share(dataframe)


   
    # INVENTORY VALUE BY CATEGORY
   

    def plot_inventory_value(self, dataframe):

        ax = self.axes["Inventory Value"]

        ax.clear()

        values = (
            dataframe.groupby("Category")
            .apply(
                lambda x: (x["Stock"] * x["Price"]).sum()
            )
            .sort_values(ascending=False)
        )

        bars = ax.bar(
            values.index,
            values.values,
            color=[
                "#3B82F6",
                "#10B981",
                "#F59E0B",
                "#EF4444",
                "#8B5CF6",
                "#06B6D4",
                "#EC4899",
                "#F97316"
            ]
        )

        ax.set_title(
            "Inventory Value by Category",
            fontsize=12,
            color="white",
            pad=12
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

        ax.set_facecolor("#1E293B")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        # Value labels

        for bar in bars:

            height = bar.get_height()

            ax.text(
                bar.get_x() + bar.get_width()/2,
                height,
                f"₹{height:,.0f}",
                ha="center",
                va="bottom",
                fontsize=8,
                color="white"
            )

        self.canvases["Inventory Value"].draw()

   
    # CATEGORY SHARE (DONUT CHART)
   

    def plot_category_share(self, dataframe):

        ax = self.axes["Category Share"]

        ax.clear()

        category_stock = (
            dataframe.groupby("Category")["Stock"]
            .sum()
            .sort_values(ascending=False)
        )

        colors = [

            "#3B82F6",

            "#10B981",

            "#F59E0B",

            "#EF4444",

            "#8B5CF6",

            "#06B6D4",

            "#EC4899",

            "#F97316"

        ]

        wedges, texts, autotexts = ax.pie(

            category_stock,

            labels=category_stock.index,

            colors=colors[:len(category_stock)],

            autopct="%1.1f%%",

            startangle=90,

            pctdistance=0.82

        )

        # Create donut

        centre_circle = ax.figure.add_artist(

            ax.figure.add_axes([0,0,0,0]).patch

        )

        ax.add_artist(

            plt.Circle(

                (0,0),

                0.60,

                color="#1E293B"

            )

        )

        ax.set_title(

            "Category Share",

            fontsize=12,

            color="white",

            pad=12

        )

        for text in texts:

            text.set_color("white")

            text.set_fontsize(8)

        for autotext in autotexts:

            autotext.set_color("white")

            autotext.set_fontsize(8)

        self.canvases["Category Share"].draw()


   
    # REVENUE TREND (LINE CHART)
   

    def plot_revenue_trend(self, dataframe):

        ax = self.axes["Revenue Trend"]

        ax.clear()

        revenue = (
            dataframe.groupby("Category")
            .apply(lambda x: (x["Stock"] * x["Price"]).sum())
            .sort_values(ascending=False)
        )

        ax.plot(
            revenue.index,
            revenue.values,
            color="#10B981",
            linewidth=3,
            marker="o",
            markersize=8
        )

        ax.fill_between(
            range(len(revenue)),
            revenue.values,
            alpha=0.25,
            color="#10B981"
        )

        ax.set_title(
            "Revenue Trend",
            fontsize=12,
            color="white",
            pad=10
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

        ax.set_facecolor("#1E293B")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.canvases["Revenue Trend"].draw()

   
    # SUPPLIER COMPARISON (HORIZONTAL BAR)
   

    def plot_supplier_comparison(self, dataframe):

        ax = self.axes["Supplier Comparison"]

        ax.clear()

        suppliers = (
            dataframe.groupby("Supplier")
            .size()
            .sort_values(ascending=False)
            .head(8)
        )

        colors = [

            "#3B82F6",

            "#10B981",

            "#F59E0B",

            "#EF4444",

            "#8B5CF6",

            "#06B6D4",

            "#EC4899",

            "#F97316"

        ]

        bars = ax.barh(

            suppliers.index,

            suppliers.values,

            color=colors[:len(suppliers)]

        )

        ax.invert_yaxis()

        ax.set_title(

            "Products per Supplier",

            fontsize=12,

            color="white",

            pad=10

        )

        ax.tick_params(

            axis="x",

            colors="white"

        )

        ax.tick_params(

            axis="y",

            colors="white"

        )

        ax.set_facecolor("#1E293B")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        for bar in bars:

            width = bar.get_width()

            ax.text(

                width + 0.1,

                bar.get_y() + bar.get_height()/2,

                str(int(width)),

                va="center",

                color="white",

                fontsize=9

            )

        self.canvases["Supplier Comparison"].draw()


           
    # STOCK TREND (LINE CHART)
   

    def plot_stock_trend(self, dataframe):

        ax = self.axes["Stock Trend"]

        ax.clear()

        stock = (
            dataframe.groupby("Category")["Stock"]
            .sum()
            .sort_values(ascending=False)
        )

        ax.plot(
            stock.index,
            stock.values,
            marker="o",
            linewidth=3,
            markersize=8,
            color="#3B82F6"
        )

        ax.fill_between(
            range(len(stock)),
            stock.values,
            alpha=0.30,
            color="#3B82F6"
        )

        ax.set_title(
            "Stock Trend",
            fontsize=12,
            color="white",
            pad=10
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

        ax.set_facecolor("#1E293B")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        self.canvases["Stock Trend"].draw()


   
    # STOCK DISTRIBUTION (PIE CHART)
   

    def plot_stock_distribution(self, dataframe):

        ax = self.axes["Stock Distribution"]

        ax.clear()

        stock = (
            dataframe.groupby("Category")["Stock"]
            .sum()
        )

        colors = [

            "#3B82F6",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#06B6D4",
            "#EC4899",
            "#F97316"

        ]

        ax.pie(

            stock.values,

            labels=stock.index,

            autopct="%1.1f%%",

            startangle=90,

            colors=colors[:len(stock)]

        )

        ax.set_title(

            "Stock Distribution",

            fontsize=12,

            color="white",

            pad=10

        )

        self.canvases["Stock Distribution"].draw()


   
    # REFRESH DASHBOARD
   

    
    def refresh(self):

        for canvas in self.canvases.values():

            canvas.draw()

        self.update_idletasks()