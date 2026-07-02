import customtkinter as ctk

from ui.analytics_cards import AnalyticsCards
from ui.analytics_charts import AnalyticsCharts
from ui.analytics_tables import AnalyticsTables
from ui.analytics_insights import AnalyticsInsights


class AnalyticsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )

        self.create_page()

    # =====================================================
    # Create Analytics Page
    # =====================================================

    def create_page(self):

        # ---------------- Header ----------------

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            padx=25,
            pady=(20, 10)
        )

        title = ctk.CTkLabel(
            header,
            text="📊 Business Analytics Dashboard",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            side="left"
        )

        subtitle = ctk.CTkLabel(
            header,
            text="Power BI Style Business Intelligence",
            font=("Segoe UI", 15),
            text_color="gray80"
        )

        subtitle.pack(
            side="left",
            padx=20,
            pady=(10, 0)
        )

        # ---------------- KPI Cards ----------------

        self.cards = AnalyticsCards(self)

        self.cards.pack(
            fill="x",
            padx=25,
            pady=(10, 20)
        )

        # ---------------- Charts ----------------

        self.charts = AnalyticsCharts(self)

        self.charts.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # ---------------- Tables ----------------

        self.tables = AnalyticsTables(self)

        self.tables.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        # ---------------- Insights ----------------

        self.insights = AnalyticsInsights(self)

        self.insights.pack(
            fill="x",
            padx=25,
            pady=(0, 25)
        )

    # =====================================================
    # Update Analytics Dashboard
    # =====================================================

    def update_dashboard(self, dataframe):

        self.cards.update_cards(dataframe)

        self.charts.update_charts(dataframe)

        self.tables.update_tables(dataframe)

        self.insights.update_insights(dataframe)