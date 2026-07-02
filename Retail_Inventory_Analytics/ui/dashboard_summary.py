import customtkinter as ctk


class SummaryCard(ctk.CTkFrame):

    def __init__(self, parent, icon, title, color):

        super().__init__(
            parent,
            fg_color="#1E293B",
            corner_radius=15
        )

        self.configure(width=250, height=120)

        self.pack_propagate(False)

        icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 30)
        )

        icon_label.pack(pady=(10, 0))

        title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 14)
        )

        title_label.pack()

        self.value = ctk.CTkLabel(
            self,
            text="0",
            font=("Segoe UI", 24, "bold"),
            text_color=color
        )

        self.value.pack()

    def update(self, value):

        self.value.configure(text=value)