import customtkinter as ctk


class DashboardCard(ctk.CTkFrame):

    def __init__(self, parent, icon, title, value):

        super().__init__(
            parent,
            width=260,
            height=140,
            corner_radius=18,
            fg_color="#1E293B",
            border_width=1,
            border_color="#334155"
        )

        self.grid_propagate(False)

        #Icon
        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 28)
        )

        self.icon_label.pack(
            pady=(15, 5)
        )

        #Title
        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 16)
        )

        self.title_label.pack()

        #Value
        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 30, "bold")
        )

        self.value_label.pack(
            pady=(8, 15)
        )

    def update_value(self, value):

        self.value_label.configure(
            text=value
        )