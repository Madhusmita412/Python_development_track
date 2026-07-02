import customtkinter as ctk
from PIL import Image
from pathlib import Path

self.callback = None

class Sidebar(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            width=250,
            corner_radius=0,
            fg_color="#1F434E"
        )

        self.pack_propagate(False)
          # Navigation callback
        self.callback = None

        self.create_sidebar()



        # Path to assets folder
        
        self.base_dir = Path(__file__).resolve().parent.parent
        self.logo_path = self.base_dir / "assets" / "logo.png"

        self.create_logo()
        self.create_menu()

    # Logo Section

    def create_logo(self):

        logo_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        logo_frame.pack(
            pady=(30, 40),
            padx=20,
            fill="x"
        )

        # Load Logo Image
        logo_image = ctk.CTkImage(
            light_image=Image.open(self.logo_path),
            dark_image=Image.open(self.logo_path),
            size=(55, 55)
        )

        logo_label = ctk.CTkLabel(
            logo_frame,
            image=logo_image,
            text=""
        )

        logo_label.pack(side="left")

        title = ctk.CTkLabel(
            logo_frame,
            text="Inventory\nPro",
            justify="left",
            font=("Segoe UI", 20, "bold")
        )

        title.pack(
            side="left",
            padx=12
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

                text=f"{icon}   {name}",

                height=50,

                corner_radius=12,

                fg_color="transparent",

                hover_color="#2563EB",

                anchor="w",

                font=("Segoe UI", 16),

                command=lambda n=name: self.highlight(n)

            )

            button.pack(
                fill="x",
                padx=18,
                pady=6
            )

            self.buttons[name] = button

        self.highlight("Dashboard")

    # Highlight Active Menu

    def highlight(self, selected):

        for name, button in self.buttons.items():

            if name == selected:

                button.configure(
                    fg_color="#2563EB",
                    font=("Segoe UI", 16, "bold")
                )

            else:

                button.configure(
                    fg_color="transparent",
                    font=("Segoe UI", 16)
                )