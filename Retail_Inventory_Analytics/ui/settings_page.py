import customtkinter as ctk


class SettingsPage(ctk.CTkFrame):

    def __init__(self, parent):

        super().__init__(
            parent,
            fg_color="#0F172A"
        )

        self.create_page()

    # =====================================================
    # CREATE SETTINGS PAGE
    # =====================================================

    def create_page(self):

        # ---------------- Header ----------------

        title = ctk.CTkLabel(
            self,
            text="⚙ Settings",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 5)
        )

        subtitle = ctk.CTkLabel(
            self,
            text="Customize your Inventory Analytics Dashboard",
            font=("Segoe UI", 15),
            text_color="gray80"
        )

        subtitle.pack(
            anchor="w",
            padx=25,
            pady=(0,20)
        )

        # ==============================
        # SETTINGS CONTAINER
        # ==============================

        container = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        container.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=10
        )

        container.grid_columnconfigure(0, weight=1)
        container.grid_columnconfigure(1, weight=1)

        # ---------------- Theme ----------------

        self.create_setting_card(

            container,

            row=0,

            column=0,

            title="🌙 Theme",

            description="Choose Light or Dark mode."

        )

        self.theme = ctk.CTkOptionMenu(

            container,

            values=[

                "Dark",

                "Light"

            ]

        )

        self.theme.grid(

            row=0,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # ---------------- Currency ----------------

        self.create_setting_card(

            container,

            row=1,

            column=0,

            title="💰 Currency",

            description="Select your preferred currency."

        )

        self.currency = ctk.CTkOptionMenu(

            container,

            values=[

                "INR (₹)",

                "USD ($)",

                "EUR (€)",

                "GBP (£)"

            ]

        )

        self.currency.grid(

            row=1,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # ---------------- Company ----------------

        self.create_setting_card(

            container,

            row=2,

            column=0,

            title="🏢 Company Name",

            description="Displayed on reports."

        )

        self.company = ctk.CTkEntry(

            container,

            width=250,

            placeholder_text="Enter Company Name"

        )

        self.company.grid(

            row=2,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # ---------------- Export Folder ----------------

        self.create_setting_card(

            container,

            row=3,

            column=0,

            title="📁 Export Folder",

            description="Choose default export directory."

        )

        self.folder = ctk.CTkEntry(

            container,

            width=250,

            placeholder_text="exports/"

        )

        self.folder.grid(

            row=3,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # ---------------- Notifications ----------------

        self.create_setting_card(

            container,

            row=4,

            column=0,

            title="🔔 Notifications",

            description="Enable dashboard notifications."

        )

        self.notifications = ctk.CTkSwitch(

            container,

            text="Enable"

        )

        self.notifications.grid(

            row=4,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # ---------------- Auto Backup ----------------

        self.create_setting_card(

            container,

            row=5,

            column=0,

            title="💾 Auto Backup",

            description="Automatically backup inventory."

        )

        self.backup = ctk.CTkSwitch(

            container,

            text="Enable"

        )

        self.backup.grid(

            row=5,

            column=1,

            padx=25,

            pady=25,

            sticky="w"

        )

        # Save Button

        save = ctk.CTkButton(

            self,

            text="💾 Save Settings",

            width=180,

            height=45,

            fg_color="#2563EB"

        )

        save.pack(

            pady=20

        )

    # =====================================================
    # SETTING CARD
    # =====================================================

    def create_setting_card(

        self,

        parent,

        row,

        column,

        title,

        description

    ):

        frame = ctk.CTkFrame(

            parent,

            fg_color="#1E293B",

            corner_radius=15

        )

        frame.grid(

            row=row,

            column=column,

            sticky="ew",

            padx=10,

            pady=10

        )

        label = ctk.CTkLabel(

            frame,

            text=title,

            font=("Segoe UI",16,"bold")

        )

        label.pack(

            anchor="w",

            padx=15,

            pady=(15,5)

        )

        desc = ctk.CTkLabel(

            frame,

            text=description,

            font=("Segoe UI",12),

            text_color="gray80"

        )

        desc.pack(

            anchor="w",

            padx=15,

            pady=(0,15)

        )