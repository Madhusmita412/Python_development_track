import os
import pandas as pd

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle
)


class Exporter:

    def __init__(self):

        self.export_folder = "exports"

        os.makedirs(
            self.export_folder,
            exist_ok=True
        )

    # ==========================================
    # Export CSV
    # ==========================================

    def export_csv(self, dataframe):

        if dataframe.empty:
            return None

        path = os.path.join(
            self.export_folder,
            "inventory_report.csv"
        )

        dataframe.to_csv(
            path,
            index=False
        )

        return path

    # ==========================================
    # Export Excel
    # ==========================================

    def export_excel(self, dataframe):

        if dataframe.empty:
            return None

        path = os.path.join(
            self.export_folder,
            "inventory_report.xlsx"
        )

        dataframe.to_excel(
            path,
            index=False
        )

        return path

    # ==========================================
    # Export PDF
    # ==========================================

    def export_pdf(self, dataframe):

        if dataframe.empty:
            return None

        path = os.path.join(
            self.export_folder,
            "inventory_report.pdf"
        )

        pdf = SimpleDocTemplate(
            path,
            pagesize=A4
        )

        table_data = [dataframe.columns.tolist()]

        table_data.extend(
            dataframe.values.tolist()
        )

        table = Table(table_data)

        table.setStyle(

            TableStyle([

                ("BACKGROUND", (0, 0), (-1, 0), colors.darkblue),

                ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, 0), 10),

                ("ALIGN", (0, 0), (-1, -1), "CENTER")

            ])

        )

        pdf.build([table])

        return path