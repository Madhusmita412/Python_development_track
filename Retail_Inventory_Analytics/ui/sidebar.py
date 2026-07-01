import customtkinter as ctk


class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=240,
            corner_radius=0,
            fg_color="#111827"
        )

        self.pack_propagate(False)

        self.create_logo()

        self.create_menu()

    # Logo

    def create_logo(self):

        logo = ctk.CTkLabel(
            self,
            text="🏪 Inventory Pro",
            font=("Segoe UI", 30, "bold")
        )

        logo.pack(
            pady=(30, 40)
        )

    # Sidebar Menu

    def create_menu(self):

        menus = [

            ("📊", "Dashboard"),

            ("📦", "Inventory"),

            ("📈", "Analytics"),

            ("📄", "Reports"),

            ("⚙", "Settings")

        ]

        self.buttons = {}

        for icon, name in menus:

            button = ctk.CTkButton(

                self,

                text=f"{icon}  {name}",

                height=48,

                width=200,

                fg_color="transparent",

                hover_color="#2563EB",

                anchor="w",

                font=("Segoe UI", 16)

            )

            button.pack(
                padx=18,
                pady=6,
                fill="x"
            )

            self.buttons[name] = button

        self.highlight("Dashboard")

    # Active Button

    def highlight(self, menu):

        for button in self.buttons.values():

            button.configure(
                fg_color="transparent"
            )

        self.buttons[menu].configure(
            fg_color="#2563EB"
        )