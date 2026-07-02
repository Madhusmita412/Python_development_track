import customtkinter as ctk


class DashboardCard(ctk.CTkFrame):

    def __init__(self, parent, icon, title, value):

        super().__init__(
            parent,
            width=260,
            height=150,
            corner_radius=18,
            fg_color="#1E293B",
            border_width=1,
            border_color="#334155"
        )

        self.grid_propagate(False)

        
        # Icon
        

        self.icon_label = ctk.CTkLabel(
            self,
            text=icon,
            font=("Segoe UI Emoji", 30)
        )

        self.icon_label.pack(
            pady=(18, 8)
        )

        
        # Title
        

        self.title_label = ctk.CTkLabel(
            self,
            text=title,
            font=("Segoe UI", 15),
            text_color="#CBD5E1"
        )

        self.title_label.pack()

        
        # Value
        

        self.value_label = ctk.CTkLabel(
            self,
            text=value,
            font=("Segoe UI", 28, "bold"),
            text_color="white"
        )

        self.value_label.pack(
            pady=(10, 18)
        )

    
    # Update Card Value
    

    def update_value(self, value):

        self.value_label.configure(
            text=value
        )

    
    # Update Card Title (Optional)
    

    def update_title(self, title):

        self.title_label.configure(
            text=title
        )

    
    # Update Icon (Optional)
    

    def update_icon(self, icon):

        self.icon_label.configure(
            text=icon
        )