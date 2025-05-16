import os
import json
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox, filedialog, colorchooser
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk
from tkinter import ttk
from pathlib import Path

# Hardcoded Fish Data for Better Lookup
fish_data = {
    "അയല": {"english": "Mackerel", "manglish": "Ayala"},
    "ചെമ്മീൻ": {"english": "Prawns", "manglish": "Chemmeen"},
    "ചെമ്പല്ലി": {"english": "Bulls Eye", "manglish": "Chembally"},
    "കിളിമീൻ": {"english": "Pink Perch", "manglish": "Kilimeen"},
    "മുള്ളൻ": {"english": "Mullet", "manglish": "Mullan"},
    "മാന്തൽ": {"english": "Sole Fish", "manglish": "Manthal"},
    "മത്തി": {"english": "Sardine", "manglish": "Mathi"},
    "വാള": {"english": "Ruben", "manglish": "Vala"},
    "കരിമീൻ": {"english": "Pearlspot", "manglish": "Karimeen"},
    "വെലമീൻ": {"english": "Emperor", "manglish": "Velameen"},
    "സിലോപ്യ": {"english": "Tilapia", "manglish": "Silopya"},
    "കട്ടള": {"english": "Carp", "manglish": "Kattala"},
    "റൂഹ്": {"english": "Labeo", "manglish": "Rooh"},
    "ആവോലി": {"english": "Pomfret", "manglish": "Avoli"},
    "കേര": {"english": "Kera (Meat)", "manglish": "Kera"},
    "ഓല നെയ്മ്മീൻ": {"english": "Sail Fish", "manglish": "Ola Neymeen"},
    "സ്രാവ്": {"english": "Shark", "manglish": "Sravu"},
    "ഓട്ടി മോദ": {"english": "Cobia", "manglish": "Ooti modha"},
    "വറ്റ": {"english": "Trevally", "manglish": "Vatta"},
    "ഹാമൂർ": {"english": "Hamoor", "manglish": "Hamoor"},
    "റെഡ് സ്നാപ്പർ": {"english": "Red Snapper", "manglish": "Red Snapper"},
    "കുന്തൽ": {"english": "Squid", "manglish": "koonthal"},
    "ചൂര": {"english": "Red Tuna", "manglish": "choora"}
}

# Butcher Layouts
butcher_layouts = {
    "usaj": "1.png",
    "bismi": "2.png",
    "kak": "3.png",
    "ka sons": "4.png"
}

# Add this after the fish_data dictionary
fish_categories = ["Sea Water Fish", "Fresh Water Fish", "Meat Only"]

# Add this after existing dictionaries
meat_categories = {
    "Chicken": ["Meat", "Leg", "Lollipop", "Breast", "Boneless"],
    "Mutton": ["Meat", "Rib", "Boneless", "Liver", "Botty", "Brain"],
    "Beef": ["Meat", "Bone"]
}

# Initialize price dictionary
meat_prices = {
    "Chicken": {item: "0" for item in ["Meat", "Leg", "Lollipop", "Breast", "Boneless"]},
    "Mutton": {item: "0" for item in ["Meat", "Rib", "Boneless", "Liver", "Botty", "Brain"]},
    "Beef": {item: "0" for item in ["Meat", "Bone"]}
}


class StyleConfig:
    def __init__(self):
        self.font_color = "#008080"  # Default teal color for categories
        self.fish_name_color = "#000000"  # Default black color for fish names
        self.category_font_size = 35
        self.item_font_size = 30
        self.category_bold = True
        self.category_italic = False
        self.category_underline = True
        self.item_bold = False
        self.item_italic = False
        self.item_underline = False
        self.font_family = "AnekMalayalam-Regular.ttf"


class MenuGenerator:
    def __init__(self):
        # Set dark mode as default before creating the window
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")



        self.root = ctk.CTk()
        self.root.title("bezgoFresh Menu Card Generator")
        self.root.geometry("1200x800")

        # Initialize variables
        self.current_theme = "dark"
        self.fish_list = []
        self.style_config = StyleConfig()
        self.butcher_name = ""

        # Create main window after setting theme
        self.setup_main_window()

        # Force update preview colors after initialization
        self.root.after(100, self.force_preview_colors)

    def force_preview_colors(self):
        """Force the preview backgrounds to be dark after initialization"""
        bg_color = '#2B2B2B'  # Dark background
        fg_color = '#FFFFFF'  # White text

        if hasattr(self, 'preview_text'):
            self.preview_text.configure(bg=bg_color, fg=fg_color)

        if hasattr(self, 'meat_preview_text'):
            self.meat_preview_text.configure(bg=bg_color, fg=fg_color)

    def setup_main_window(self):
        # Create header frame
        header_frame = ctk.CTkFrame(self.root)
        header_frame.pack(fill="x", padx=20, pady=(10, 0))

        # Load and display logo
        try:
            # Load logo image
            logo_img = Image.open("logo.png")
            # Resize logo to appropriate size (adjust size as needed)
            logo_size = (100, 50)  # Adjust these dimensions to match your logo
            logo_img = logo_img.resize(logo_size)
            self.logo = ctk.CTkImage(logo_img, size=logo_size)

            # Create and pack logo label
            logo_label = ctk.CTkLabel(header_frame, image=self.logo, text="")
            logo_label.pack(side="left", padx=5)
        except Exception as e:
            print(f"Failed to load logo: {str(e)}")
            # Fallback to text if logo fails to load
            logo_label = ctk.CTkLabel(header_frame, text="bezgoFresh")
            logo_label.pack(side="left", padx=5)

        # Add title
        title_label = ctk.CTkLabel(
            header_frame,
            text="Menu Card Generator",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(side="left", padx=20)

        # Create main container
        self.main_container = ctk.CTkFrame(self.root)
        self.main_container.pack(fill="both", expand=True, padx=20, pady=20)

        # Setup tabs
        self.setup_tabs()

    def setup_tabs(self):
        # Create tab view
        self.tabview = ctk.CTkTabview(self.main_container)
        self.tabview.pack(fill="both", expand=True)

        # Create tabs
        self.fish_tab = self.tabview.add("Fish Menu")
        self.meat_tab = self.tabview.add("Meat Menu")
        self.layouts_tab = self.tabview.add("Layouts")
        self.settings_tab = self.tabview.add("Settings")

        self.setup_fish_tab()
        self.setup_meat_tab()
        self.setup_layouts_tab()
        self.setup_settings_tab()

    def setup_fish_tab(self):
        # Create frame for preview
        preview_frame = ctk.CTkFrame(self.fish_tab)
        preview_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Preview label
        ctk.CTkLabel(preview_frame, text="Preview", font=("Helvetica", 14, "bold")).pack(pady=(5, 0))

        # Create Text widget with scrollbar
        self.preview_text = tk.Text(preview_frame,
                                    height=10,
                                    font=("TkDefaultFont", 10),
                                    wrap="word",
                                    bg='#F0F0F0',
                                    fg='#2C3E50')

        # Add scrollbar
        scrollbar = ttk.Scrollbar(preview_frame, orient="vertical", command=self.preview_text.yview)
        self.preview_text.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and text widget
        scrollbar.pack(side="right", fill="y")
        self.preview_text.pack(pady=5, padx=5, fill="both", expand=True)

        # Configure tags for styling
        self.setup_preview_tags()

        # Button frame
        button_frame = ctk.CTkFrame(self.fish_tab)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add Fish", command=self.add_fish_popup).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Edit List", command=self.edit_list_popup).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Set Butcher Name", command=self.set_butcher_name).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Generate Menu", command=self.generate_fish_menu).pack(side="left", padx=5)

    def setup_meat_tab(self):
        # Create main container for meat tab
        meat_container = ctk.CTkFrame(self.meat_tab)
        meat_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Split into two columns
        left_frame = ctk.CTkFrame(meat_container)
        left_frame.pack(side="left", fill="both", expand=True, padx=5)

        right_frame = ctk.CTkFrame(meat_container)
        right_frame.pack(side="right", fill="both", expand=True, padx=5)

        # Price entry section
        self.setup_meat_price_entries(left_frame)

        # Preview section
        self.setup_meat_preview(right_frame)

        # Button frame
        button_frame = ctk.CTkFrame(self.meat_tab)
        button_frame.pack(pady=10)

        # Add Set Butcher Name button
        ctk.CTkButton(button_frame, text="Set Butcher Name",
                      command=self.set_butcher_name).pack(side="left", padx=5)

        ctk.CTkButton(button_frame, text="Generate Menu",
                      command=self.generate_meat_menu).pack(side="left", padx=5)

    def setup_meat_price_entries(self, parent_frame):
        # Create scrollable frame for price entries
        price_frame = ctk.CTkScrollableFrame(parent_frame, label_text="Price Entry")
        price_frame.pack(fill="both", expand=True, padx=5, pady=5)

        self.price_entries = {}

        for category in meat_categories:
            # Category label
            ctk.CTkLabel(price_frame,
                         text=category,
                         font=("Helvetica", 12, "bold")).pack(pady=(10, 5))

            self.price_entries[category] = {}

            # Create entry fields for each item
            for item in meat_categories[category]:
                item_frame = ctk.CTkFrame(price_frame)
                item_frame.pack(fill="x", pady=2)

                ctk.CTkLabel(item_frame, text=f"{item}:").pack(side="left", padx=5)
                price_entry = ctk.CTkEntry(item_frame, placeholder_text="Enter price")
                price_entry.pack(side="left", padx=5, fill="x", expand=True)

                self.price_entries[category][item] = price_entry

                # Bind entry to preview update
                price_entry.bind('<KeyRelease>', lambda e: self.update_meat_preview())

    def setup_meat_preview(self, parent_frame):
        # Create frame for preview
        preview_frame = ctk.CTkFrame(parent_frame)
        preview_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Add preview label
        ctk.CTkLabel(preview_frame, text="Preview",
                     font=("Helvetica", 14, "bold")).pack(pady=(5, 0))

        # Force dark background
        bg_color = '#2B2B2B'  # Dark background
        fg_color = '#FFFFFF'  # White text

        # Create Text widget with explicit background
        self.meat_preview_text = tk.Text(
            preview_frame,
            height=10,
            font=("TkDefaultFont", 10),
            wrap="word",
            bg=bg_color,
            fg=fg_color,
            insertbackground=fg_color,  # Cursor color
            selectbackground='#454545',  # Selection background
            selectforeground=fg_color,  # Selection text color
        )

        # Create and configure scrollbar
        scrollbar = ttk.Scrollbar(
            preview_frame,
            orient="vertical",
            command=self.meat_preview_text.yview
        )
        self.meat_preview_text.configure(yscrollcommand=scrollbar.set)

        # Pack scrollbar and preview text
        scrollbar.pack(side="right", fill="y")
        self.meat_preview_text.pack(pady=5, padx=5, fill="both", expand=True)

        # Force the background color again
        self.meat_preview_text.configure(bg=bg_color, fg=fg_color)

        # Configure tags for styling
        self.setup_meat_preview_tags()

        # Bind configuration event to maintain colors
        self.meat_preview_text.bind('<Configure>', lambda e: self.maintain_preview_colors())

    def maintain_preview_colors(self):
        """Maintain dark background for previews"""
        bg_color = '#2B2B2B'
        fg_color = '#FFFFFF'

        if hasattr(self, 'preview_text'):
            self.preview_text.configure(bg=bg_color, fg=fg_color)

        if hasattr(self, 'meat_preview_text'):
            self.meat_preview_text.configure(bg=bg_color, fg=fg_color)

    def setup_meat_preview_tags(self):
        # Always use white text on dark background for preview
        fg_color = '#FFFFFF'
        item_name_color = '#FFFFFF'

        # Use selected color for item names if set
        if hasattr(self, 'style_config') and self.style_config.fish_name_color != "#000000":
            item_name_color = self.style_config.fish_name_color

        self.meat_preview_text.tag_configure("bold",
                                             font=(self.style_config.font_family, 11, "bold"),
                                             foreground=fg_color)
        self.meat_preview_text.tag_configure("normal",
                                             font=(self.style_config.font_family, 10),
                                             foreground=fg_color)
        self.meat_preview_text.tag_configure("category",
                                             font=(self.style_config.font_family, 12, "bold"),
                                             foreground=self.style_config.font_color)
        self.meat_preview_text.tag_configure("item_name",
                                             font=(self.style_config.font_family, 10),
                                             foreground=item_name_color)
        self.meat_preview_text.tag_configure("separator",
                                             font=(self.style_config.font_family, 10),
                                             foreground="#666666")

    def update_meat_preview(self):
        self.meat_preview_text.configure(state="normal")
        self.meat_preview_text.delete("1.0", tk.END)

        first_category = True
        for category in meat_categories:
            if not first_category:
                self.meat_preview_text.insert("end", "\n" + "─" * 40 + "\n", "separator")
            else:
                first_category = False

            # Category header in category color
            self.meat_preview_text.insert("end", f"\n{category}\n", "category")

            for idx, item in enumerate(meat_categories[category], 1):
                # Item number in bold
                self.meat_preview_text.insert("end", f"{idx}. ", "bold")

                # Item name in same color as fish names
                self.meat_preview_text.insert("end", item, "item_name")

                # Price in normal style
                price = self.price_entries[category][item].get() or "0"
                self.meat_preview_text.insert("end", f" - ₹{price}\n", "normal")

            self.meat_preview_text.insert("end", "\n")

        self.meat_preview_text.configure(state="disabled")

    def setup_layouts_tab(self):
        layouts_frame = ctk.CTkFrame(self.layouts_tab)
        layouts_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Layout Management
        ctk.CTkLabel(layouts_frame, text="Layout Management",
                     font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        # Add New Layout
        add_layout_frame = ctk.CTkFrame(layouts_frame)
        add_layout_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(add_layout_frame, text="Add New Layout:").pack(side="left", padx=5)

        self.layout_name_var = tk.StringVar()
        ctk.CTkEntry(add_layout_frame, textvariable=self.layout_name_var,
                     placeholder_text="Layout Name").pack(side="left", padx=5)

        ctk.CTkButton(add_layout_frame, text="Choose Image",
                      command=self.add_new_layout).pack(side="left", padx=5)

        # Existing Layouts
        ctk.CTkLabel(layouts_frame, text="Existing Layouts:",
                     font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

        # Create scrollable frame for layouts
        self.layouts_list_frame = ctk.CTkScrollableFrame(layouts_frame, height=200)
        self.layouts_list_frame.pack(fill="x", pady=5)

        self.update_layouts_list()

    def setup_settings_tab(self):
        settings_frame = ctk.CTkFrame(self.settings_tab)
        settings_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Theme Selection
        theme_frame = ctk.CTkFrame(settings_frame)
        theme_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(theme_frame, text="Application Theme",
                     font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        # Theme Selection with dark mode as default
        self.theme_var = tk.StringVar(value="Dark")

        themes_container = ctk.CTkFrame(theme_frame)
        themes_container.pack(fill="x", pady=5)

        ctk.CTkRadioButton(
            themes_container,
            text="Light Theme",
            variable=self.theme_var,
            value="Light",
            command=self.change_theme
        ).pack(side="left", padx=20)

        ctk.CTkRadioButton(
            themes_container,
            text="Dark Theme",
            variable=self.theme_var,
            value="Dark",
            command=self.change_theme
        ).pack(side="left", padx=20)

        # Separator
        ttk.Separator(settings_frame, orient="horizontal").pack(fill="x", pady=15)

        # Color Selection
        color_frame = ctk.CTkFrame(settings_frame)
        color_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(color_frame, text="Color Settings",
                     font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        # Category Color
        category_color_frame = ctk.CTkFrame(color_frame)
        category_color_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(category_color_frame, text="Category Color:").pack(side="left", padx=5)
        self.category_color_preview = ctk.CTkLabel(category_color_frame, text="      ",
                                                   fg_color=self.style_config.font_color)
        self.category_color_preview.pack(side="left", padx=5)

        ctk.CTkButton(category_color_frame, text="Choose Color",
                      command=self.choose_category_color).pack(side="left", padx=5)

        # Fish Name Color
        fish_color_frame = ctk.CTkFrame(color_frame)
        fish_color_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(fish_color_frame, text="Fish Name Color:").pack(side="left", padx=5)
        self.fish_color_preview = ctk.CTkLabel(fish_color_frame, text="      ",
                                               fg_color=self.style_config.fish_name_color)
        self.fish_color_preview.pack(side="left", padx=5)

        ctk.CTkButton(fish_color_frame, text="Choose Color",
                      command=self.choose_fish_name_color).pack(side="left", padx=5)

        # Font Sizes
        sizes_frame = ctk.CTkFrame(settings_frame)
        sizes_frame.pack(fill="x", pady=5)

        # Category font size
        ctk.CTkLabel(sizes_frame, text="Category Font Size:").pack(side="left", padx=5)
        self.category_size_var = tk.StringVar(value=str(self.style_config.category_font_size))
        ctk.CTkEntry(sizes_frame, textvariable=self.category_size_var,
                     width=50).pack(side="left", padx=5)

        # Item font size
        ctk.CTkLabel(sizes_frame, text="Item Font Size:").pack(side="left", padx=5)
        self.item_size_var = tk.StringVar(value=str(self.style_config.item_font_size))
        ctk.CTkEntry(sizes_frame, textvariable=self.item_size_var,
                     width=50).pack(side="left", padx=5)

        # Style Toggles
        self.setup_style_toggles(settings_frame)

        # Save Settings Button
        ctk.CTkButton(settings_frame, text="Save Settings",
                      command=self.save_style_settings).pack(pady=10)

        # Add Fish Data Management section
        data_frame = ctk.CTkFrame(settings_frame)
        data_frame.pack(fill="x", pady=10)

        ctk.CTkLabel(data_frame, text="Data Management",
                     font=("Helvetica", 16, "bold")).pack(pady=(0, 10))

        ctk.CTkButton(data_frame, text="Edit Fish Data",
                      command=self.edit_fish_data).pack(pady=5)

    def setup_style_toggles(self, parent_frame):
        toggles_frame = ctk.CTkFrame(parent_frame)
        toggles_frame.pack(fill="x", pady=5)

        # Category Style
        category_style_frame = ctk.CTkFrame(toggles_frame)
        category_style_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(category_style_frame, text="Category Style:").pack(side="left", padx=5)

        self.category_bold_var = tk.BooleanVar(value=self.style_config.category_bold)
        ctk.CTkCheckBox(category_style_frame, text="Bold",
                        variable=self.category_bold_var).pack(side="left", padx=5)

        self.category_italic_var = tk.BooleanVar(value=self.style_config.category_italic)
        ctk.CTkCheckBox(category_style_frame, text="Italic",
                        variable=self.category_italic_var).pack(side="left", padx=5)

        self.category_underline_var = tk.BooleanVar(value=self.style_config.category_underline)
        ctk.CTkCheckBox(category_style_frame, text="Underline",
                        variable=self.category_underline_var).pack(side="left", padx=5)

        # Item Style
        item_style_frame = ctk.CTkFrame(toggles_frame)
        item_style_frame.pack(fill="x", pady=5)

        ctk.CTkLabel(item_style_frame, text="Item Style:").pack(side="left", padx=5)

        self.item_bold_var = tk.BooleanVar(value=self.style_config.item_bold)
        ctk.CTkCheckBox(item_style_frame, text="Bold",
                        variable=self.item_bold_var).pack(side="left", padx=5)

        self.item_italic_var = tk.BooleanVar(value=self.style_config.item_italic)
        ctk.CTkCheckBox(item_style_frame, text="Italic",
                        variable=self.item_italic_var).pack(side="left", padx=5)

        self.item_underline_var = tk.BooleanVar(value=self.style_config.item_underline)
        ctk.CTkCheckBox(item_style_frame, text="Underline",
                        variable=self.item_underline_var).pack(side="left", padx=5)

    def setup_preview_tags(self):
        # Set default colors based on theme
        if self.current_theme == "dark":
            fg_color = '#FFFFFF'
            fish_name_color = '#FFFFFF'
        else:
            fg_color = '#2C3E50'
            fish_name_color = '#000000'  # Default to black in light mode

        # Use selected color for fish names in light mode
        if self.current_theme == "light":
            fish_name_color = self.style_config.fish_name_color

        self.preview_text.tag_configure("bold",
                                        font=(self.style_config.font_family, 11, "bold"),
                                        foreground=fg_color)
        self.preview_text.tag_configure("normal",
                                        font=(self.style_config.font_family, 10),
                                        foreground=fg_color)
        self.preview_text.tag_configure("category",
                                        font=(self.style_config.font_family, 12, "bold"),
                                        foreground=self.style_config.font_color)
        self.preview_text.tag_configure("fish_name",
                                        font=(self.style_config.font_family, 10),
                                        foreground=fish_name_color)
        self.preview_text.tag_configure("separator",
                                        font=(self.style_config.font_family, 10),
                                        foreground="#666666")

    def setup_meat_preview_tags(self):
        # Set default colors based on theme
        if self.current_theme == "dark":
            fg_color = '#FFFFFF'
            item_name_color = '#FFFFFF'
        else:
            fg_color = '#2C3E50'
            item_name_color = '#000000'  # Default to black in light mode

        # Use selected color for item names in light mode
        if self.current_theme == "light":
            item_name_color = self.style_config.fish_name_color

        self.meat_preview_text.tag_configure("bold",
                                             font=(self.style_config.font_family, 11, "bold"),
                                             foreground=fg_color)
        self.meat_preview_text.tag_configure("normal",
                                             font=(self.style_config.font_family, 10),
                                             foreground=fg_color)
        self.meat_preview_text.tag_configure("category",
                                             font=(self.style_config.font_family, 12, "bold"),
                                             foreground=self.style_config.font_color)
        self.meat_preview_text.tag_configure("item_name",
                                             font=(self.style_config.font_family, 10),
                                             foreground=item_name_color)
        self.meat_preview_text.tag_configure("separator",
                                             font=(self.style_config.font_family, 10),
                                             foreground="#666666")

    def choose_category_color(self):
        color = colorchooser.askcolor(color=self.style_config.font_color)
        if color[1]:
            self.style_config.font_color = color[1]
            self.category_color_preview.configure(fg_color=color[1])
            # Update preview text colors for categories
            self.preview_text.tag_configure("category", foreground=color[1])
            self.meat_preview_text.tag_configure("category", foreground=color[1])
            self.update_preview()

    def choose_fish_name_color(self):
        color = colorchooser.askcolor(color=self.style_config.fish_name_color)
        if color[1]:
            self.style_config.fish_name_color = color[1]
            self.fish_color_preview.configure(fg_color=color[1])

            # Only update color if in light mode
            if self.current_theme == "light":
                self.preview_text.tag_configure("fish_name", foreground=color[1])
                self.meat_preview_text.tag_configure("item_name", foreground=color[1])

            # Force refresh of previews
            self.update_preview()
            self.update_meat_preview()

    def save_style_settings(self):
        try:
            self.style_config.category_font_size = int(self.category_size_var.get())
            self.style_config.item_font_size = int(self.item_size_var.get())
            self.style_config.category_bold = self.category_bold_var.get()
            self.style_config.category_italic = self.category_italic_var.get()
            self.style_config.category_underline = self.category_underline_var.get()
            self.style_config.item_bold = self.item_bold_var.get()
            self.style_config.item_italic = self.item_italic_var.get()
            self.style_config.item_underline = self.item_underline_var.get()

            # Update previews with new settings
            self.update_preview()
            self.update_meat_preview()

            messagebox.showinfo("Success", "Settings saved successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter valid font sizes!")

    def add_new_layout(self):
        layout_name = self.layout_name_var.get().strip()
        if not layout_name:
            messagebox.showerror("Error", "Please enter a layout name!")
            return

        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg")]
        )
        if file_path:
            # Create layouts directory if it doesn't exist
            os.makedirs("layouts", exist_ok=True)

            # Copy file to layouts directory
            new_path = f"layouts/{layout_name}{Path(file_path).suffix}"
            Image.open(file_path).save(new_path)

            # Update butcher_layouts dictionary
            butcher_layouts[layout_name] = new_path
            self.update_layouts_list()
            self.layout_name_var.set("")
            messagebox.showinfo("Success", "Layout added successfully!")

    def update_layouts_list(self):
        # Clear existing layouts
        for widget in self.layouts_list_frame.winfo_children():
            widget.destroy()

        # Add each layout with preview and remove button
        for name, path in butcher_layouts.items():
            layout_frame = ctk.CTkFrame(self.layouts_list_frame)
            layout_frame.pack(fill="x", pady=2)

            ctk.CTkLabel(layout_frame, text=name).pack(side="left", padx=5)
            ctk.CTkButton(layout_frame, text="Remove",
                          command=lambda n=name: self.remove_layout(n)).pack(side="right", padx=5)

    def remove_layout(self, layout_name):
        if layout_name in butcher_layouts:
            if messagebox.askyesno("Confirm", f"Remove layout '{layout_name}'?"):
                # Remove file if it exists
                try:
                    os.remove(butcher_layouts[layout_name])
                except OSError:
                    pass

                # Remove from dictionary
                del butcher_layouts[layout_name]
                self.update_layouts_list()
                messagebox.showinfo("Success", "Layout removed successfully!")

    def set_butcher_name(self):
        dialog = ctk.CTkToplevel(self.root)
        dialog.title("Set Butcher Name")
        dialog.geometry("400x200")

        # Make popup appear in front
        dialog.transient(self.root)
        dialog.grab_set()
        dialog.focus_force()

        # Create and pack widgets
        frame = ctk.CTkFrame(dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)

        ctk.CTkLabel(frame, text="Select Butcher Name:").pack(pady=10)

        # Create dropdown with available butcher names
        butcher_var = tk.StringVar(frame)
        butcher_names = sorted(butcher_layouts.keys())  # Get sorted list of butcher names
        butcher_dropdown = ctk.CTkOptionMenu(frame, variable=butcher_var, values=butcher_names)
        butcher_dropdown.pack(pady=5)

        def submit():
            self.butcher_name = butcher_var.get()
            dialog.destroy()

        ctk.CTkButton(frame, text="Submit", command=submit).pack(pady=10)

    def get_fish_details(self, fish_name):
        try:
            fish_name = fish_name.strip()

            # First try direct match with Malayalam name
            if fish_name in fish_data:
                return [fish_name,
                        fish_data[fish_name]["manglish"],
                        fish_data[fish_name]["english"]]

            # Try to find by manglish name
            for mal_name, details in fish_data.items():
                if fish_name.lower() == details["manglish"].lower():
                    return [mal_name,
                            details["manglish"],
                            details["english"]]

            # Try to find by English name
            for mal_name, details in fish_data.items():
                if fish_name.lower() == details["english"].lower():
                    return [mal_name,
                            details["manglish"],
                            details["english"]]

            # If not found, show warning
            messagebox.showwarning(
                "Fish Not Found",
                f"'{fish_name}' not found in database. Please check the spelling."
            )
            return [fish_name, fish_name, fish_name]

        except Exception as e:
            messagebox.showerror("Error", f"Error getting fish details: {str(e)}")
            return [fish_name, fish_name, fish_name]

    def add_fish_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Add Fish")
        popup.geometry("500x500")

        # Make popup appear in front
        popup.transient(self.root)
        popup.grab_set()
        popup.focus_force()

        ctk.CTkLabel(popup, text="Select Fish Category:").pack(pady=5)
        category_var = tk.StringVar(popup)
        category_var.set(fish_categories[0])
        category_menu = ctk.CTkOptionMenu(popup, variable=category_var, values=fish_categories)
        category_menu.pack()

        # Fish name dropdown
        ctk.CTkLabel(popup, text="Select Fish Name:").pack(pady=5)
        fish_var = tk.StringVar(popup)

        # Create display names with all three languages
        fish_names = [details["manglish"] for details in fish_data.values()]
        fish_names = sorted(fish_names, key=lambda x: x.lower())  # Sort by manglish name
        fish_dropdown = ctk.CTkOptionMenu(popup, variable=fish_var, values=fish_names)
        fish_dropdown.pack()

        # Size dropdown
        ctk.CTkLabel(popup, text="Select Fish Size:").pack(pady=5)
        size_var = tk.StringVar(popup)
        size_var.set("Small")  # Default value
        size_dropdown = ctk.CTkOptionMenu(popup, variable=size_var,
                                          values=["Small", "Medium", "Large"])
        size_dropdown.pack()

        ctk.CTkLabel(popup, text="Enter Price (₹):").pack(pady=5)
        price_entry = ctk.CTkEntry(popup)
        price_entry.pack()

        def submit():
            fish_name = fish_var.get().strip()
            size = size_var.get().strip()
            price = price_entry.get().strip()
            category = category_var.get()

            if fish_name and size and price:
                mal_name, mang_name, eng_name = self.get_fish_details(fish_name)
                self.fish_list.append((mal_name, mang_name, eng_name, size, price, category))
                self.update_preview()
                price_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "Please enter all details!")

        def finish():
            popup.destroy()

        button_frame = ctk.CTkFrame(popup)
        button_frame.pack(pady=10)

        ctk.CTkButton(button_frame, text="Add Another", command=submit).pack(side="left", padx=5)
        ctk.CTkButton(button_frame, text="Done", command=finish).pack(side="left", padx=5)

    def edit_list_popup(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("Edit Fish List")
        popup.geometry("600x500")

        # Make popup appear in front
        popup.transient(self.root)
        popup.grab_set()
        popup.focus_force()

        # Create main frame
        main_frame = ctk.CTkFrame(popup)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)

        # Instructions label
        ctk.CTkLabel(main_frame,
                     text="Use ↑↓ buttons to reorder items. Select an item to delete.",
                     font=("Helvetica", 12)).pack(pady=(0, 10))

        # Create listbox frame
        list_frame = ctk.CTkFrame(main_frame)
        list_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Create listbox with scrollbar
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        # Use white background in dark mode, light gray in light mode
        bg_color = 'white' if self.current_theme == "dark" else '#F0F0F0'
        fg_color = 'black' if self.current_theme == "dark" else '#2C3E50'

        self.edit_listbox = tk.Listbox(
            list_frame,
            selectmode="single",
            bg=bg_color,
            fg=fg_color,
            font=("TkDefaultFont", 11),
            height=15
        )
        self.edit_listbox.pack(side="left", fill="both", expand=True)

        # Configure scrollbar
        scrollbar.config(command=self.edit_listbox.yview)
        self.edit_listbox.config(yscrollcommand=scrollbar.set)

        # Populate listbox
        for fish in self.fish_list:
            display_text = f"{fish[0]} \\ {fish[1]} \\ {fish[2]} ({fish[3]}) - ₹{fish[4]} [{fish[5]}]"
            self.edit_listbox.insert(tk.END, display_text)

        # Create button frame
        button_frame = ctk.CTkFrame(main_frame)
        button_frame.pack(fill="x", pady=10)

        # Move up button
        ctk.CTkButton(
            button_frame,
            text="↑ Move Up",
            command=lambda: self.move_item("up")
        ).pack(side="left", padx=5, expand=True)

        # Move down button
        ctk.CTkButton(
            button_frame,
            text="↓ Move Down",
            command=lambda: self.move_item("down")
        ).pack(side="left", padx=5, expand=True)

        # Delete button
        ctk.CTkButton(
            button_frame,
            text="Delete",
            command=self.delete_selected_item,
            fg_color="red",
            hover_color="#D32F2F"
        ).pack(side="left", padx=5, expand=True)

        # Done button
        ctk.CTkButton(
            button_frame,
            text="Done",
            command=popup.destroy
        ).pack(side="left", padx=5, expand=True)

    def move_item(self, direction):
        try:
            # Get selected index
            selected_idx = self.edit_listbox.curselection()[0]

            # Calculate new index
            new_idx = selected_idx - 1 if direction == "up" else selected_idx + 1

            # Check bounds
            if 0 <= new_idx < self.edit_listbox.size():
                # Get the items to swap
                item_text = self.edit_listbox.get(selected_idx)

                # Delete and reinsert in listbox
                self.edit_listbox.delete(selected_idx)
                self.edit_listbox.insert(new_idx, item_text)

                # Update selection
                self.edit_listbox.selection_clear(0, tk.END)
                self.edit_listbox.selection_set(new_idx)
                self.edit_listbox.see(new_idx)

                # Update fish_list
                self.fish_list[selected_idx], self.fish_list[new_idx] = \
                    self.fish_list[new_idx], self.fish_list[selected_idx]

                # Update preview
                self.update_preview()
        except IndexError:
            pass  # No item selected

    def delete_selected_item(self):
        try:
            # Get selected index
            selected_idx = self.edit_listbox.curselection()[0]

            # Remove from listbox
            self.edit_listbox.delete(selected_idx)

            # Remove from fish_list
            self.fish_list.pop(selected_idx)

            # Update preview
            self.update_preview()
        except IndexError:
            messagebox.showwarning("Warning", "Please select an item to delete.")

    def update_preview(self):
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", tk.END)

        # Group fish by categories
        categorized_fish = {category: [] for category in fish_categories}
        for fish in self.fish_list:
            categorized_fish[fish[5]].append(fish)

        # Display fish by category
        first_category = True
        for category in fish_categories:
            if categorized_fish[category]:
                if not first_category:
                    self.preview_text.insert("end", "\n" + "─" * 40 + "\n", "separator")
                else:
                    first_category = False

                # Category header in category color
                self.preview_text.insert("end", f"\n{category}\n", "category")

                for idx, fish in enumerate(categorized_fish[category], 1):
                    # Item number in bold
                    self.preview_text.insert("end", f"{idx}. ", "bold")

                    # Fish names in fish name color
                    self.preview_text.insert("end", f"{fish[0]} \\ {fish[1]} \\ {fish[2]}", "fish_name")

                    # Size and price in normal style
                    self.preview_text.insert("end", f" ({fish[3]}) - ₹{fish[4]}\n", "normal")

                self.preview_text.insert("end", "\n")

        self.preview_text.configure(state="disabled")

    def generate_menu(self, menu_type="fish"):
        if menu_type == "fish" and not self.fish_list:
            messagebox.showerror("Error", "No items to generate menu!")
            return

        if not self.butcher_name:
            messagebox.showerror("Error", "Please set butcher name first!")
            return

        if self.butcher_name not in butcher_layouts:
            messagebox.showerror("Error", "Unknown butcher name! Please enter a valid name.")
            return

        layout_path = butcher_layouts[self.butcher_name]
        if not os.path.exists(layout_path):
            messagebox.showerror("Error", f"Menu layout for {self.butcher_name} not found!")
            return

        img = Image.open(layout_path).convert("RGBA")
        draw = ImageDraw.Draw(img)

        font_path = "AnekMalayalam-Regular.ttf"
        if not os.path.exists(font_path):
            messagebox.showerror("Error", "Font not found! Ensure it's in the script folder.")
            return

        # Apply style settings
        font_style = ""
        if self.style_config.item_bold:
            font_style += "bold "
        if self.style_config.item_italic:
            font_style += "italic "
        font_style = font_style.strip() or "regular"

        category_style = ""
        if self.style_config.category_bold:
            category_style += "bold "
        if self.style_config.category_italic:
            category_style += "italic "
        category_style = category_style.strip() or "regular"

        font = ImageFont.truetype(font_path, self.style_config.item_font_size)
        category_font = ImageFont.truetype(font_path, self.style_config.category_font_size)

        y_offset = 250
        if menu_type == "fish":
            self.generate_fish_menu_content(draw, category_font, font, y_offset)
        else:
            self.generate_meat_menu_content(draw, category_font, font, y_offset)

        img.show()

        save_confirmation = messagebox.askyesno("Export Menu", "Do you want to export this menu card?")
        if save_confirmation:
            prefix = "Fish" if menu_type == "fish" else "Meat"
            default_filename = f"{prefix}_Menu_{self.butcher_name}_{datetime.now().strftime('%Y-%m-%d')}.png"
            file_path = filedialog.asksaveasfilename(
                defaultextension=".png",
                initialfile=default_filename,
                filetypes=[("PNG files", "*.png"), ("All files", "*.*")]
            )
            if file_path:
                img.save(file_path)
                messagebox.showinfo("Success", "Menu saved successfully!")

    def generate_fish_menu_content(self, draw, category_font, font, y_offset):
        categorized_fish = {category: [] for category in fish_categories}
        for fish in self.fish_list:
            categorized_fish[fish[5]].append(fish)

        for category in fish_categories:
            if categorized_fish[category]:
                # Draw category header with category color
                draw.text((200, y_offset), category,
                          fill=self.style_config.font_color,
                          font=category_font)

                if self.style_config.category_underline:
                    text_bbox = draw.textbbox((200, y_offset), category, font=category_font)
                    line_y = text_bbox[3] + 2
                    draw.line([(200, line_y), (text_bbox[2], line_y)],
                              fill=self.style_config.font_color, width=2)

                y_offset += 50

                for idx, fish in enumerate(categorized_fish[category], 1):
                    # Draw item number in default color
                    number_text = f"{idx}. "
                    draw.text((200, y_offset), number_text,
                              fill='black',
                              font=font)

                    # Calculate width of number for positioning fish name
                    number_bbox = draw.textbbox((200, y_offset), number_text, font=font)
                    fish_x = number_bbox[2] + 5  # Add small spacing

                    # Draw fish name in fish name color
                    fish_text = f"{fish[0]} \\ {fish[1]} \\ {fish[2]}"
                    draw.text((fish_x, y_offset), fish_text,
                              fill=self.style_config.fish_name_color,
                              font=font)

                    # Calculate width of fish name for positioning size and price
                    fish_bbox = draw.textbbox((fish_x, y_offset), fish_text, font=font)
                    rest_x = fish_bbox[2] + 5  # Add small spacing

                    # Draw size and price in default color
                    rest_text = f" ({fish[3]}) - ₹{fish[4]}"
                    draw.text((rest_x, y_offset), rest_text,
                              fill='black',
                              font=font)

                    if self.style_config.item_underline:
                        full_text = number_text + fish_text + rest_text
                        text_bbox = draw.textbbox((200, y_offset), full_text, font=font)
                        line_y = text_bbox[3] + 1
                        draw.line([(200, line_y), (text_bbox[2], line_y)],
                                  fill='black', width=1)

                    y_offset += 40

                y_offset += 20

    def generate_meat_menu_content(self, draw, category_font, font, y_offset):
        for category in meat_categories:
            # Draw category header with category color
            draw.text((200, y_offset), category,
                      fill=self.style_config.font_color,
                      font=category_font)

            if self.style_config.category_underline:
                text_bbox = draw.textbbox((200, y_offset), category, font=category_font)
                line_y = text_bbox[3] + 2
                draw.line([(200, line_y), (text_bbox[2], line_y)],
                          fill=self.style_config.font_color, width=2)

            y_offset += 50

            for idx, item in enumerate(meat_categories[category], 1):
                # Draw item number in default color
                number_text = f"{idx}. "
                draw.text((200, y_offset), number_text,
                          fill='black',
                          font=font)

                # Calculate width of number for positioning item name
                number_bbox = draw.textbbox((200, y_offset), number_text, font=font)
                item_x = number_bbox[2] + 5  # Add small spacing

                # Draw item name in fish name color (same as fish names)
                draw.text((item_x, y_offset), item,
                          fill=self.style_config.fish_name_color,
                          font=font)

                # Calculate width of item name for positioning price
                item_bbox = draw.textbbox((item_x, y_offset), item, font=font)
                price_x = item_bbox[2] + 5  # Add small spacing

                # Draw price in default color
                price = self.price_entries[category][item].get() or "0"
                draw.text((price_x, y_offset), f" - ₹{price}",
                          fill='black',
                          font=font)

                if self.style_config.item_underline:
                    full_text = f"{number_text}{item} - ₹{price}"
                    text_bbox = draw.textbbox((200, y_offset), full_text, font=font)
                    line_y = text_bbox[3] + 1
                    draw.line([(200, line_y), (text_bbox[2], line_y)],
                              fill='black', width=1)

                y_offset += 40

            y_offset += 20

    def generate_fish_menu(self):
        self.generate_menu("fish")

    def generate_meat_menu(self):
        self.generate_menu("meat")

    def change_theme(self):
        # Update theme based on radio button selection
        self.current_theme = self.theme_var.get().lower()
        ctk.set_appearance_mode(self.current_theme)

        # Update preview backgrounds based on theme
        bg_color = '#2B2B2B'  # Always keep dark background for preview
        fg_color = '#FFFFFF'  # Always keep white text for preview

        # Update fish preview
        if hasattr(self, 'preview_text'):
            self.preview_text.configure(bg=bg_color, fg=fg_color)
            self.setup_preview_tags()

        # Update meat preview
        if hasattr(self, 'meat_preview_text'):
            self.meat_preview_text.configure(bg=bg_color, fg=fg_color)
            self.setup_meat_preview_tags()

        # Update previews
        self.update_preview()
        self.update_meat_preview()

    def edit_fish_data(self):
        edit_window = ctk.CTkToplevel(self.root)
        edit_window.title("Edit Fish Data")
        edit_window.geometry("800x600")

        # Make popup appear in front
        edit_window.transient(self.root)
        edit_window.grab_set()
        edit_window.focus_force()

        # Format current fish data as JSON
        formatted_data = json.dumps({
            "fish_data": fish_data,
            "fish_categories": fish_categories
        }, indent=4, ensure_ascii=False)

        text_widget = ctk.CTkTextbox(edit_window)
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", formatted_data)

        def save_changes():
            try:
                content = text_widget.get("1.0", "end-1c")
                new_data = json.loads(content)

                # Update global variables
                globals()["fish_data"].clear()
                globals()["fish_data"].update(new_data["fish_data"])
                globals()["fish_categories"][:] = new_data["fish_categories"]

                # Save to JSON file
                with open("fish_data.json", "w", encoding="utf-8") as f:
                    json.dump(new_data, f, ensure_ascii=False, indent=4)

                messagebox.showinfo("Success", "Fish data updated successfully!")
                edit_window.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"Invalid data format: {str(e)}")

        ctk.CTkButton(edit_window, text="Save Changes", command=save_changes).pack(pady=10)

    def load_fish_data(self):
        try:
            json_path = Path("fish_data.json")
            if not json_path.exists():
                # Create default JSON if it doesn't exist
                default_data = {
                    "fish_data": {
                        "അയല": {
                            "english": "Mackerel",
                            "manglish": "Ayala"
                        }
                    },
                    "fish_categories": [
                        "Sea Water Fish",
                        "Fresh Water Fish",
                        "Meat Only"
                    ]
                }
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(default_data, f, ensure_ascii=False, indent=4)

            # Load data from JSON
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                global fish_data, fish_categories
                fish_data = data["fish_data"]
                fish_categories = data["fish_categories"]
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load fish data: {str(e)}")


if __name__ == "__main__":
    app = MenuGenerator()
    app.root.mainloop()
