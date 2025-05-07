import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog, font
import os
import platform
import json
import re # For Find/Replace, auto-indent, bracket matching

# --- Configuration & Settings ---
CONFIG_FILE = "textra_config.json"
DEFAULT_THEME_NAME = "Darkula"
DEFAULT_FONT_FAMILY = "Cascadia Code" if platform.system() == "Windows" else "JetBrains Mono" if platform.system() == "Darwin" else "Fira Code"
DEFAULT_FONT_SIZE = 13
MAX_RECENT_FILES = 10

# --- Global Theme Variable (Accessed by multiple parts) ---
current_theme_settings = {}

def load_config():
    try:
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {
            "theme": DEFAULT_THEME_NAME,
            "font_family": DEFAULT_FONT_FAMILY,
            "font_size": DEFAULT_FONT_SIZE,
            "recent_files": [],
            "word_wrap": True, # Default to word wrap on
        }

def save_config(config_data):
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config_data, f, indent=4)
    except IOError:
        messagebox.showerror("Config Error", "Could not save settings.")

config = load_config()

# --- Theme Loading (similar to before, but uses global current_theme_settings) ---
THEME_FILE = "editor_themes.json"

def load_themes_definition():
    # Define a template for what a complete theme should look like, with defaults
    theme_template = {
        "bg": "#2B2B2B", "fg": "#A9B7C6", "text_bg": "#3C3F41", "text_fg": "#A9B7C6",
        "select_bg": "#214283", "select_fg": "#FFFFFF", "cursor_insert_color": "#BBBBBB",
        "menu_bg": "#3C3F41", "menu_fg": "#BBBBBB", "menu_active_bg": "#4B6EAF", "menu_active_fg": "#FFFFFF",
        "statusbar_bg": "#3C3F41", "statusbar_fg": "#A9B7C6", "notebook_bg": "#3C3F41",
        "tab_bg": "#2B2B2B", "tab_fg": "#A9B7C6", "tab_active_bg": "#4A4D4F", "tab_active_fg": "#FFFFFF",
        "linenum_bg": "#313335", "linenum_fg": "#606366", 
        "bracket_match_bg": "#3B514D", "bracket_match_fg": "#FFEF28",
        # Add other potential keys here with their defaults if needed in the future
        "button_bg": "#3C3F41", "button_fg": "#BBBBBB", 
        "button_active_bg": "#4B6EAF", "button_active_fg": "#FFFFFF",
        "indicator": "#A9B7C6" # For TCheckbutton
    }
    
    default_themes_data = {
        "Darkula": theme_template.copy(), # Base Darkula is the template
        "Classic Light": {
            "bg": "#F0F0F0", "fg": "#000000", "text_bg": "#FFFFFF", "text_fg": "#000000",
            "select_bg": "#0078D7", "select_fg": "#FFFFFF", "cursor_insert_color": "#000000",
            "menu_bg": "#F0F0F0", "menu_fg": "#000000", "menu_active_bg": "#D0E0F0", "menu_active_fg": "#000000",
            "statusbar_bg": "#E0E0E0", "statusbar_fg": "#000000", "notebook_bg": "#E0E0E0",
            "tab_bg": "#D0D0D0", "tab_fg": "#000000", "tab_active_bg": "#FFFFFF", "tab_active_fg": "#000000",
            "linenum_bg": "#EAEAEA", "linenum_fg": "#888888", 
            "bracket_match_bg": "#A6D2FF", "bracket_match_fg": "#000000",
            "button_bg": "#F0F0F0", "button_fg": "#000000",
            "button_active_bg": "#D0E0F0", "button_active_fg": "#000000",
            "indicator": "#000000"
        },
        "Nord": {
            "bg": "#2E3440", "fg": "#ECEFF4", "text_bg": "#3B4252", "text_fg": "#E5E9F0",
            "select_bg": "#5E81AC", "select_fg": "#ECEFF4", "cursor_insert_color": "#D8DEE9",
            "menu_bg": "#3B4252", "menu_fg": "#E5E9F0", "menu_active_bg": "#4C566A", "menu_active_fg": "#ECEFF4",
            "statusbar_bg": "#3B4252", "statusbar_fg": "#E5E9F0", "notebook_bg": "#3B4252",
            "tab_bg": "#2E3440", "tab_fg": "#E5E9F0", "tab_active_bg": "#4C566A", "tab_active_fg": "#ECEFF4",
            "linenum_bg": "#2E3440", "linenum_fg": "#4C566A",
            "bracket_match_bg": "#5E81AC", "bracket_match_fg": "#ECEFF4",
            "button_bg": "#3B4252", "button_fg": "#E5E9F0",
            "button_active_bg": "#4C566A", "button_active_fg": "#ECEFF4",
            "indicator": "#88C0D0"
        },
        "Tokyo Night": {
            "bg": "#1A1B26", "fg": "#A9B1D6", "text_bg": "#24283B", "text_fg": "#C0CAF5",
            "select_bg": "#7AA2F7", "select_fg": "#1A1B26", "cursor_insert_color": "#C0CAF5",
            "menu_bg": "#24283B", "menu_fg": "#A9B1D6", "menu_active_bg": "#7AA2F7", "menu_active_fg": "#1A1B26",
            "statusbar_bg": "#24283B", "statusbar_fg": "#A9B1D6", "notebook_bg": "#24283B",
            "tab_bg": "#1A1B26", "tab_fg": "#A9B1D6", "tab_active_bg": "#7AA2F7", "tab_active_fg": "#1A1B26",
            "linenum_bg": "#1A1B26", "linenum_fg": "#565F89",
            "bracket_match_bg": "#7AA2F7", "bracket_match_fg": "#1A1B26",
            "button_bg": "#24283B", "button_fg": "#A9B1D6",
            "button_active_bg": "#7AA2F7", "button_active_fg": "#1A1B26",
            "indicator": "#7AA2F7"
        },
        "Catppuccin": {
            "bg": "#1E1E2E", "fg": "#CDD6F4", "text_bg": "#313244", "text_fg": "#CDD6F4",
            "select_bg": "#89B4FA", "select_fg": "#1E1E2E", "cursor_insert_color": "#CDD6F4",
            "menu_bg": "#313244", "menu_fg": "#CDD6F4", "menu_active_bg": "#89B4FA", "menu_active_fg": "#1E1E2E",
            "statusbar_bg": "#313244", "statusbar_fg": "#CDD6F4", "notebook_bg": "#313244",
            "tab_bg": "#1E1E2E", "tab_fg": "#CDD6F4", "tab_active_bg": "#89B4FA", "tab_active_fg": "#1E1E2E",
            "linenum_bg": "#1E1E2E", "linenum_fg": "#6C7086",
            "bracket_match_bg": "#89B4FA", "bracket_match_fg": "#1E1E2E",
            "button_bg": "#313244", "button_fg": "#CDD6F4",
            "button_active_bg": "#89B4FA", "button_active_fg": "#1E1E2E",
            "indicator": "#89B4FA"
        },
        "One Dark": {
            "bg": "#282C34", "fg": "#ABB2BF", "text_bg": "#21252B", "text_fg": "#ABB2BF",
            "select_bg": "#528BFF", "select_fg": "#FFFFFF", "cursor_insert_color": "#ABB2BF",
            "menu_bg": "#21252B", "menu_fg": "#ABB2BF", "menu_active_bg": "#528BFF", "menu_active_fg": "#FFFFFF",
            "statusbar_bg": "#21252B", "statusbar_fg": "#ABB2BF", "notebook_bg": "#21252B",
            "tab_bg": "#282C34", "tab_fg": "#ABB2BF", "tab_active_bg": "#528BFF", "tab_active_fg": "#FFFFFF",
            "linenum_bg": "#282C34", "linenum_fg": "#495162",
            "bracket_match_bg": "#528BFF", "bracket_match_fg": "#FFFFFF",
            "button_bg": "#21252B", "button_fg": "#ABB2BF",
            "button_active_bg": "#528BFF", "button_active_fg": "#FFFFFF",
            "indicator": "#528BFF"
        },
        "Warm Brown": {
            "bg": "#2D1810", "fg": "#E8D3B6", "text_bg": "#3D2318", "text_fg": "#E8D3B6",
            "select_bg": "#C17817", "select_fg": "#2D1810", "cursor_insert_color": "#E8D3B6",
            "menu_bg": "#3D2318", "menu_fg": "#E8D3B6", "menu_active_bg": "#C17817", "menu_active_fg": "#2D1810",
            "statusbar_bg": "#3D2318", "statusbar_fg": "#E8D3B6", "notebook_bg": "#3D2318",
            "tab_bg": "#2D1810", "tab_fg": "#E8D3B6", "tab_active_bg": "#C17817", "tab_active_fg": "#2D1810",
            "linenum_bg": "#2D1810", "linenum_fg": "#8B5A2B",
            "bracket_match_bg": "#C17817", "bracket_match_fg": "#2D1810",
            "button_bg": "#3D2318", "button_fg": "#E8D3B6",
            "button_active_bg": "#C17817", "button_active_fg": "#2D1810",
            "indicator": "#C17817"
        },
        "Cyberpunk": {
            "bg": "#0C0C0C", "fg": "#00FF9F", "text_bg": "#1A1A1A", "text_fg": "#00FF9F",
            "select_bg": "#FF00FF", "select_fg": "#0C0C0C", "cursor_insert_color": "#00FF9F",
            "menu_bg": "#1A1A1A", "menu_fg": "#00FF9F", "menu_active_bg": "#FF00FF", "menu_active_fg": "#0C0C0C",
            "statusbar_bg": "#1A1A1A", "statusbar_fg": "#00FF9F", "notebook_bg": "#1A1A1A",
            "tab_bg": "#0C0C0C", "tab_fg": "#00FF9F", "tab_active_bg": "#FF00FF", "tab_active_fg": "#0C0C0C",
            "linenum_bg": "#0C0C0C", "linenum_fg": "#FF00FF",
            "bracket_match_bg": "#FF00FF", "bracket_match_fg": "#0C0C0C",
            "button_bg": "#1A1A1A", "button_fg": "#00FF9F",
            "button_active_bg": "#FF00FF", "button_active_fg": "#0C0C0C",
            "indicator": "#FF00FF"
        },
        "Forest": {
            "bg": "#1B2B1B", "fg": "#A8C6A8", "text_bg": "#243224", "text_fg": "#A8C6A8",
            "select_bg": "#4A8A4A", "select_fg": "#1B2B1B", "cursor_insert_color": "#A8C6A8",
            "menu_bg": "#243224", "menu_fg": "#A8C6A8", "menu_active_bg": "#4A8A4A", "menu_active_fg": "#1B2B1B",
            "statusbar_bg": "#243224", "statusbar_fg": "#A8C6A8", "notebook_bg": "#243224",
            "tab_bg": "#1B2B1B", "tab_fg": "#A8C6A8", "tab_active_bg": "#4A8A4A", "tab_active_fg": "#1B2B1B",
            "linenum_bg": "#1B2B1B", "linenum_fg": "#4A8A4A",
            "bracket_match_bg": "#4A8A4A", "bracket_match_fg": "#1B2B1B",
            "button_bg": "#243224", "button_fg": "#A8C6A8",
            "button_active_bg": "#4A8A4A", "button_active_fg": "#1B2B1B",
            "indicator": "#4A8A4A"
        },
        "Sunset": {
            "bg": "#2C1B2E", "fg": "#FFB6C1", "text_bg": "#3D2739", "text_fg": "#FFB6C1",
            "select_bg": "#FF8C00", "select_fg": "#2C1B2E", "cursor_insert_color": "#FFB6C1",
            "menu_bg": "#3D2739", "menu_fg": "#FFB6C1", "menu_active_bg": "#FF8C00", "menu_active_fg": "#2C1B2E",
            "statusbar_bg": "#3D2739", "statusbar_fg": "#FFB6C1", "notebook_bg": "#3D2739",
            "tab_bg": "#2C1B2E", "tab_fg": "#FFB6C1", "tab_active_bg": "#FF8C00", "tab_active_fg": "#2C1B2E",
            "linenum_bg": "#2C1B2E", "linenum_fg": "#FF8C00",
            "bracket_match_bg": "#FF8C00", "bracket_match_fg": "#2C1B2E",
            "button_bg": "#3D2739", "button_fg": "#FFB6C1",
            "button_active_bg": "#FF8C00", "button_active_fg": "#2C1B2E",
            "indicator": "#FF8C00"
        },
        "Ocean": {
            "bg": "#0A192F", "fg": "#64FFDA", "text_bg": "#112240", "text_fg": "#64FFDA",
            "select_bg": "#00B4D8", "select_fg": "#0A192F", "cursor_insert_color": "#64FFDA",
            "menu_bg": "#112240", "menu_fg": "#64FFDA", "menu_active_bg": "#00B4D8", "menu_active_fg": "#0A192F",
            "statusbar_bg": "#112240", "statusbar_fg": "#64FFDA", "notebook_bg": "#112240",
            "tab_bg": "#0A192F", "tab_fg": "#64FFDA", "tab_active_bg": "#00B4D8", "tab_active_fg": "#0A192F",
            "linenum_bg": "#0A192F", "linenum_fg": "#00B4D8",
            "bracket_match_bg": "#00B4D8", "bracket_match_fg": "#0A192F",
            "button_bg": "#112240", "button_fg": "#64FFDA",
            "button_active_bg": "#00B4D8", "button_active_fg": "#0A192F",
            "indicator": "#00B4D8"
        }
    }

    try:
        if not os.path.exists(THEME_FILE):
            print(f"Creating theme file: {THEME_FILE}")
            with open(THEME_FILE, 'w') as f:
                json.dump(default_themes_data, f, indent=4)
            return default_themes_data

        print(f"Loading theme file: {THEME_FILE}")
        with open(THEME_FILE, 'r') as f:
            loaded_themes_from_file = json.load(f)
            print(f"Loaded themes from file: {list(loaded_themes_from_file.keys())}")

            # Ensure all loaded themes have all keys from the template
            processed_themes = {}
            for theme_name, theme_data in loaded_themes_from_file.items():
                # Start with a copy of the template, then update with loaded data
                complete_theme = theme_template.copy() 
                complete_theme.update(theme_data) # Override template with specifics from file
                processed_themes[theme_name] = complete_theme
            
            # Also ensure our default themes are in the processed list if not in file
            for default_name, default_data in default_themes_data.items():
                if default_name not in processed_themes:
                    processed_themes[default_name] = default_data.copy()

            # If the file themes are outdated, overwrite the file with complete themes
            save_updated_themes = False
            for theme_name in loaded_themes_from_file: # Check only themes that were IN the file
                if loaded_themes_from_file[theme_name] != processed_themes.get(theme_name):
                    save_updated_themes = True
                    break
            if save_updated_themes:
                 print(f"Updating theme file {THEME_FILE} with new/missing keys.")
                 with open(THEME_FILE, 'w') as f:
                    json.dump(processed_themes, f, indent=4)

            return processed_themes
            
    except json.JSONDecodeError:
        print(f"Error parsing {THEME_FILE}. Using hardcoded defaults.")
        messagebox.showerror("Theme Error", f"Could not parse {THEME_FILE}. Using default themes.")
        return default_themes_data # Fallback to hardcoded complete defaults
    except Exception as e:
        print(f"An unexpected error occurred loading themes: {e}. Using hardcoded defaults.")
        return default_themes_data

THEMES_DEFINITION = load_themes_definition()
print(f"Available themes: {list(THEMES_DEFINITION.keys())}")

class TextEditor:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Textra - Untitled") # Renamed
        self.root.geometry("1000x700") # Slightly larger for more features

        self.unsaved_changes = {} # tab_id: boolean
        self.current_find_options = {"text": "", "match_case": tk.BooleanVar(), "regex": tk.BooleanVar(), "direction_down": tk.BooleanVar(value=True)}
        self.find_dialog = None # To keep track of find dialog

        self.editor_font = font.Font(family=config["font_family"], size=config["font_size"])

        # Apply theme first, before creating any widgets
        print(f"Applying theme: {config['theme']}")
        self.apply_theme_globally(config["theme"])
        self.configure_styles()

        self.create_widgets()
        self.create_menu()
        
        self.update_status_bar()
        self.create_new_tab(title="Untitled")

        self.root.protocol("WM_DELETE_WINDOW", self.exit_editor)
        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Auto-save config on exit
        self.root.bind("<Destroy>", lambda e: save_config(config) if e.widget == self.root else None)

    def apply_theme_globally(self, theme_name):
        global current_theme_settings
        print(f"Applying theme: {theme_name}")
        print(f"Available themes: {list(THEMES_DEFINITION.keys())}")
        if theme_name in THEMES_DEFINITION:
            config["theme"] = theme_name # Update config
            current_theme_settings = THEMES_DEFINITION[theme_name].copy()  # Make a copy to avoid reference issues
            print(f"Applied theme settings: {list(current_theme_settings.keys())}")
        else: # Fallback if theme name is invalid
            print(f"Theme {theme_name} not found, using default: {DEFAULT_THEME_NAME}")
            config["theme"] = DEFAULT_THEME_NAME
            current_theme_settings = THEMES_DEFINITION[DEFAULT_THEME_NAME].copy()  # Make a copy to avoid reference issues
            print(f"Applied default theme settings: {list(current_theme_settings.keys())}")
        
        # Apply to root and other non-ttk elements directly affected
        self.root.configure(bg=current_theme_settings['bg'])
        
        # Re-configure styles and existing widgets
        if hasattr(self, 'style'): self.configure_styles()
        if hasattr(self, 'status_bar'): self.status_bar.config(background=current_theme_settings['statusbar_bg'], foreground=current_theme_settings['statusbar_fg'])
        if hasattr(self, 'menu_bar'): self.configure_menu_theme_colors()
        if hasattr(self, 'notebook'):
            for tab_id in self.notebook.tabs():
                frame = self.notebook.nametowidget(tab_id)
                # First child is the Frame holding LineNumbers and Text
                content_frame = frame.winfo_children()[0]
                line_numbers = content_frame.winfo_children()[0] # Assuming LineNumbers is first
                text_area = content_frame.winfo_children()[1]    # Assuming Text is second
                
                self.configure_text_area_theme(text_area)
                if isinstance(line_numbers, tk.Canvas): # LineNumbers widget
                    line_numbers.config(bg=current_theme_settings['linenum_bg'])
                    self.redraw_line_numbers(text_area, line_numbers) # Redraw with new colors

    def configure_styles(self):
        self.style = ttk.Style()
        available_themes = self.style.theme_names()
        if 'clam' in available_themes: self.style.theme_use('clam')
        elif 'alt' in available_themes: self.style.theme_use('alt')

        # Configure modern notebook style
        self.style.configure("TNotebook", background=current_theme_settings['notebook_bg'])
        
        # Fix the tab style mapping
        self.style.configure("TNotebook.Tab",
            background=current_theme_settings['tab_bg'],
            foreground=current_theme_settings['tab_fg'],
            padding=[10, 5],
            font=(self.editor_font.cget("family"), 10)
        )
        self.style.map("TNotebook.Tab",
            background=[("selected", current_theme_settings['tab_active_bg'])],
            foreground=[("selected", current_theme_settings['tab_active_fg'])]
        )

        # Configure modern frame style
        self.style.configure("TFrame", background=current_theme_settings['bg'])
        
        # Configure modern label style
        self.style.configure("TLabel", 
            background=current_theme_settings['bg'], 
            foreground=current_theme_settings['fg'],
            font=(self.editor_font.cget("family"), 10)
        )

        # Configure modern status bar style
        self.style.configure("Status.TFrame", 
            background=current_theme_settings['statusbar_bg'],
            relief=tk.FLAT
        )
        self.style.configure("Status.TLabel", 
            background=current_theme_settings['statusbar_bg'], 
            foreground=current_theme_settings['statusbar_fg'],
            padding=5,
            font=(self.editor_font.cget("family"), 9)
        )

        # Configure modern button style
        self.style.configure("TButton", 
            background=current_theme_settings.get('button_bg', current_theme_settings['bg']),
            foreground=current_theme_settings.get('button_fg', current_theme_settings['fg']),
            padding=[10, 5],
            font=(self.editor_font.cget("family"), 10)
        )
        self.style.map("TButton",
            background=[('active', current_theme_settings.get('button_active_bg', current_theme_settings['menu_active_bg']))],
            foreground=[('active', current_theme_settings.get('button_active_fg', current_theme_settings['menu_active_fg']))]
        )

        # Configure modern entry style
        self.style.configure("TEntry", 
            fieldbackground=current_theme_settings['text_bg'],
            foreground=current_theme_settings['text_fg'],
            insertcolor=current_theme_settings['cursor_insert_color'],
            padding=[5, 2],
            font=(self.editor_font.cget("family"), 10)
        )

        # Configure modern checkbutton style
        self.style.configure("TCheckbutton", 
            background=current_theme_settings['bg'],
            foreground=current_theme_settings['fg'],
            indicatorcolor=current_theme_settings.get('indicator', current_theme_settings['fg']),
            font=(self.editor_font.cget("family"), 10)
        )

        # Configure modern separator style
        self.style.configure("TSeparator", 
            background=current_theme_settings['statusbar_bg']
        )

    def configure_text_area_theme(self, text_area):
        text_area.config(
            background=current_theme_settings['text_bg'],
            foreground=current_theme_settings['text_fg'],
            selectbackground=current_theme_settings['select_bg'],
            selectforeground=current_theme_settings['select_fg'],
            insertbackground=current_theme_settings['cursor_insert_color'],
            undo=True,
            wrap=tk.WORD if config["word_wrap"] else tk.NONE,
            font=self.editor_font,
            tabs=(self.editor_font.measure('    ')), # 4 spaces tab
            # For bracket matching
            highlightthickness=0, bd=0 # Remove default border if any
        )
        # Configure bracket matching tags
        text_area.tag_configure("bracket_match", 
                                background=current_theme_settings.get('bracket_match_bg', 'yellow'),
                                foreground=current_theme_settings.get('bracket_match_fg', None)) # None means use default fg


    def create_widgets(self):
        # Create a main container with padding
        main_container = ttk.Frame(self.root, style="TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)

        # Create notebook with modern styling
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # Create status bar with modern styling
        self.status_bar_frame = ttk.Frame(self.root, style="Status.TFrame")
        self.status_bar_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=2, pady=(0,2))
        
        # Add a subtle separator line above status bar
        separator = ttk.Separator(self.root, orient='horizontal')
        separator.pack(side=tk.BOTTOM, fill=tk.X, padx=2)
        
        self.status_label_main = ttk.Label(self.status_bar_frame, text="Ln 1, Col 1", style="Status.TLabel", anchor=tk.W)
        self.status_label_main.pack(side=tk.LEFT, padx=8, pady=4)

        self.status_label_info = ttk.Label(self.status_bar_frame, text="", style="Status.TLabel", anchor=tk.E)
        self.status_label_info.pack(side=tk.RIGHT, padx=8, pady=4)
    
    def get_current_text_content_frame(self):
        try:
            current_tab_main_frame_name = self.notebook.select()
            if not current_tab_main_frame_name: return None
            current_tab_main_frame = self.notebook.nametowidget(current_tab_main_frame_name)
            # The content_frame is the first child of the main_frame (which is the tab itself)
            return current_tab_main_frame.winfo_children()[0] 
        except (tk.TclError, IndexError):
            return None

    def get_current_text_area(self):
        content_frame = self.get_current_text_content_frame()
        if content_frame:
            # Text area is the second child of content_frame (after line_numbers Canvas)
            try: return content_frame.winfo_children()[1]
            except IndexError: return None
        return None

    def get_current_tab_id(self):
        """Returns the ID of the currently selected tab, or None if no tabs exist."""
        try:
            return self.notebook.select()
        except tk.TclError:
            return None

    def get_current_line_numbers_canvas(self):
        content_frame = self.get_current_text_content_frame()
        if content_frame:
            # Line numbers canvas is the first child of content_frame
            try: return content_frame.winfo_children()[0]
            except IndexError: return None
        return None

    def create_new_tab(self, title="Untitled", content="", file_path=None):
        tab_main_frame = ttk.Frame(self.notebook, style="TFrame")
        tab_main_frame.pack(fill=tk.BOTH, expand=True)

        # Create a content frame with modern styling
        content_frame = ttk.Frame(tab_main_frame, style="TFrame")
        content_frame.pack(fill=tk.BOTH, expand=True)

        # Create line numbers with modern styling
        line_numbers = tk.Canvas(content_frame, width=45, bg=current_theme_settings['linenum_bg'], 
                               highlightthickness=0, bd=0)
        line_numbers.pack(side=tk.LEFT, fill=tk.Y)

        # Create text area with modern styling
        text_area = tk.Text(content_frame, relief=tk.FLAT, borderwidth=0, padx=8, pady=4)
        self.configure_text_area_theme(text_area)
        text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        text_area.insert(tk.END, content)
        text_area.edit_modified(False)

        # Link scrolling with proper command handling
        def on_scroll(*args):
            self.on_text_scroll(*args, text_area=text_area, line_numbers=line_numbers)
        
        text_area.config(yscrollcommand=on_scroll)
        
        # Bindings
        text_area.bind("<KeyRelease>", self.on_text_change)
        text_area.bind("<ButtonRelease-1>", self.on_text_change)
        text_area.bind("<FocusIn>", self.on_text_change)
        text_area.bind("<Return>", lambda e, ta=text_area: self.handle_auto_indent(e, ta))
        text_area.bind("<KeyPress>", lambda e, ta=text_area: self.handle_bracket_matching(e, ta))

        self.notebook.add(tab_main_frame, text=title)
        self.notebook.select(tab_main_frame)

        tab_id = self.notebook.select()
        self.unsaved_changes[tab_id] = False
        text_area.file_path = file_path
        
        text_area.line_numbers_canvas = line_numbers
        line_numbers.text_widget = text_area

        self.update_window_title()
        self.on_text_change()
        text_area.focus_set()
        
        if file_path:
            self.add_recent_file(file_path)
        return text_area

    def on_text_scroll(self, *args, text_area, line_numbers):
        # Handle scroll commands properly
        if args:
            if args[0] == "moveto":
                text_area.yview_moveto(args[1])
            elif args[0] == "scroll":
                text_area.yview_scroll(args[1], args[2])
        # Redraw line numbers based on new view
        self.redraw_line_numbers(text_area, line_numbers)

    def redraw_line_numbers(self, text_area=None, line_numbers_canvas=None):
        if text_area is None: text_area = self.get_current_text_area()
        if line_numbers_canvas is None: line_numbers_canvas = self.get_current_line_numbers_canvas()

        if not text_area or not line_numbers_canvas: return

        line_numbers_canvas.delete("all")
        
        # Get the first visible line index
        first_visible_char_index = text_area.index("@0,0")
        first_visible_line = int(first_visible_char_index.split('.')[0])
        
        # Get the y-offset of the first visible line
        try:
            dlineinfo_first = text_area.dlineinfo(first_visible_char_index)
            if dlineinfo_first is None: # Not yet rendered
                line_numbers_canvas.after(50, lambda ta=text_area, ln=line_numbers_canvas: self.redraw_line_numbers(ta, ln))
                return
            y_offset = dlineinfo_first[1] # y-coordinate of the baseline
            line_height = dlineinfo_first[3] # height of the line
            char_height_approx = self.editor_font.metrics('linespace') # Approx line height
        except tk.TclError: # Can happen if widget is not fully mapped
             line_numbers_canvas.after(50, lambda ta=text_area, ln=line_numbers_canvas: self.redraw_line_numbers(ta, ln))
             return


        # Iterate through visible lines
        current_line_num = first_visible_line
        total_lines = int(text_area.index('end-1c').split('.')[0])

        y = (line_height // 2) - y_offset # Start drawing from a bit above the first line's baseline
                                          # Adjust y to align with text lines
        
        while y < line_numbers_canvas.winfo_height() and current_line_num <= total_lines :
            line_index = f"{current_line_num}.0"
            dlineinfo = text_area.dlineinfo(line_index)
            if dlineinfo is None: # Line not visible or doesn't exist
                if current_line_num > total_lines + 5 : # safety break
                    break
                current_line_num +=1
                y += char_height_approx # Increment by approx height if dlineinfo fails
                continue

            # x, y_pos, width, height, baseline = dlineinfo # Unpack all
            y_pos_line_baseline = dlineinfo[1] # y-coordinate of baseline for THIS line
            current_line_height = dlineinfo[3]

            # Calculate drawing y: relative to canvas top, aligning with text line's vertical center
            # The y from dlineinfo is relative to the text widget's top visible part.
            # We need to map this to the line_numbers_canvas.
            # The y_offset was for the *first* line's baseline.
            draw_y = y_pos_line_baseline - y_offset + (current_line_height // 2)


            # Add 2px padding from right edge of canvas
            line_numbers_canvas.create_text(
                line_numbers_canvas.winfo_width() - 5, draw_y,
                anchor=tk.NE, text=str(current_line_num),
                font=self.editor_font, fill=current_theme_settings['linenum_fg']
            )
            
            if current_line_num == total_lines and text_area.get(f"{current_line_num}.end-1c", f"{current_line_num}.end").strip() == "":
                 # If the last line is empty, dlineinfo might give small height, so break
                 if not text_area.get(f"{current_line_num}.0", f"{current_line_num}.end-1c").strip():
                    break


            current_line_num += 1
            # y += current_line_height # This was the issue, y should track the actual drawing position based on dlineinfo
            y = draw_y + (current_line_height // 2) # Next estimated position

        # If the text area is scrolled all the way to the bottom, ensure last line number is visible
        # This is a heuristic, dlineinfo is more reliable
        last_line_on_screen_index = text_area.index(f"@0,{text_area.winfo_height()}")
        last_line_num_on_screen = int(last_line_on_screen_index.split('.')[0])

        if last_line_num_on_screen >= total_lines and y < line_numbers_canvas.winfo_height():
            dlineinfo_last = text_area.dlineinfo(f"{total_lines}.0")
            if dlineinfo_last:
                draw_y = dlineinfo_last[1] - y_offset + (dlineinfo_last[3] // 2)
                if line_numbers_canvas.find_withtag(str(total_lines)) == (): # if not already drawn
                    line_numbers_canvas.create_text(
                        line_numbers_canvas.winfo_width() - 5, draw_y,
                        anchor=tk.NE, text=str(total_lines),
                        font=self.editor_font, fill=current_theme_settings['linenum_fg']
                    )


    def on_text_change(self, event=None):
        text_area = self.get_current_text_area()
        if not text_area: return

        # Unsaved changes marker
        tab_id = self.get_current_tab_id()
        if tab_id:
            if text_area.edit_modified():
                if not self.unsaved_changes.get(tab_id, False):
                    self.unsaved_changes[tab_id] = True
                    current_tab_text = self.notebook.tab(tab_id, "text")
                    if not current_tab_text.endswith("*"):
                        self.notebook.tab(tab_id, text=current_tab_text + "*")
        
        self.update_status_bar()
        self.redraw_line_numbers(text_area, text_area.line_numbers_canvas)
        
        # For bracket matching, needs to be triggered on cursor move or key press
        # We'll call it from keypress too for immediacy.
        # And also here for selection changes/mouse clicks.
        if event and event.type == tk.EventType.ButtonRelease or event and event.type == tk.EventType.FocusIn:
            self.handle_bracket_matching(event, text_area)


    def update_status_bar(self, event=None):
        text_area = self.get_current_text_area()
        if text_area:
            cursor_pos = text_area.index(tk.INSERT)
            line, col = map(int, cursor_pos.split('.'))
            main_status = f"  Ln {line}, Col {col+1}"

            # Word and Char count
            content = text_area.get("1.0", tk.END)
            char_count = len(content.replace('\n', '')) # Exclude newlines from char count for typical display
            word_count = len(content.split())

            info_status = f"Chars: {char_count}  Words: {word_count}"

            # Selection count
            if text_area.tag_ranges(tk.SEL):
                sel_start = text_area.index(tk.SEL_FIRST)
                sel_end = text_area.index(tk.SEL_LAST)
                selected_text = text_area.get(sel_start, sel_end)
                sel_chars = len(selected_text.replace('\n',''))
                sel_lines = selected_text.count('\n') +1
                if selected_text.endswith('\n') and sel_lines > 1 : sel_lines -=1 # Heuristic for line selection
                main_status += f"    Sel: {sel_lines}L, {sel_chars}C"

            self.status_label_main.config(text=main_status)
            self.status_label_info.config(text=info_status)
        else:
            self.status_label_main.config(text="")
            self.status_label_info.config(text="")

    def update_window_title(self):
        text_area = self.get_current_text_area()
        if text_area and hasattr(text_area, 'file_path') and text_area.file_path:
            base_name = os.path.basename(text_area.file_path)
            self.root.title(f"Textra - {base_name}{' *' if self.unsaved_changes.get(self.get_current_tab_id()) else ''}")
        elif text_area:
            tab_text = self.notebook.tab(self.notebook.select(), 'text').replace("*","")
            self.root.title(f"Textra - {tab_text}{' *' if self.unsaved_changes.get(self.get_current_tab_id()) else ''}")
        else:
            self.root.title("Textra")
            
    def on_tab_changed(self, event=None):
        self.update_window_title()
        self.on_text_change() # This will update status bar and line numbers
        text_area = self.get_current_text_area()
        if text_area:
            text_area.focus_set()
            self.apply_word_wrap_to_current_tab() # Ensure wrap state is correct
            self.handle_bracket_matching(None, text_area) # Update bracket matching for new tab

    def create_menu(self):
        self.menu_bar = tk.Menu(self.root) # No special styling here, done in apply_theme
        self.root.config(menu=self.menu_bar)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New Tab", accelerator=self.get_accelerator("N"), command=self.new_file)
        self.file_menu.add_command(label="Open...", accelerator=self.get_accelerator("O"), command=self.open_file)
        
        self.recent_files_menu = tk.Menu(self.file_menu, tearoff=0)
        self.file_menu.add_cascade(label="Open Recent", menu=self.recent_files_menu)
        self.populate_recent_files_menu()
        
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Save", accelerator=self.get_accelerator("S"), command=self.save_file)
        self.file_menu.add_command(label="Save As...", accelerator=self.get_accelerator("Shift+S"), command=self.save_as_file)
        self.file_menu.add_command(label="Save All", command=self.save_all_files)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Close Tab", accelerator=self.get_accelerator("W"), command=self.close_current_tab)
        self.file_menu.add_command(label="Close All Tabs", command=self.close_all_tabs)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", accelerator=self.get_accelerator("Q"), command=self.exit_editor)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Undo", accelerator=self.get_accelerator("Z"), command=self.edit_undo)
        self.edit_menu.add_command(label="Redo", accelerator=self.get_accelerator_redo(), command=self.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Cut", accelerator=self.get_accelerator("X"), command=self.edit_cut)
        self.edit_menu.add_command(label="Copy", accelerator=self.get_accelerator("C"), command=self.edit_copy)
        self.edit_menu.add_command(label="Paste", accelerator=self.get_accelerator("V"), command=self.edit_paste)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Select All", accelerator=self.get_accelerator("A"), command=self.edit_select_all)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label="Go to Line...", accelerator=self.get_accelerator("G"), command=self.go_to_line)

        # Search Menu
        self.search_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Search", menu=self.search_menu)
        self.search_menu.add_command(label="Find/Replace...", accelerator=self.get_accelerator("F"), command=self.show_find_replace_dialog)
        self.search_menu.add_command(label="Find Next", accelerator="F3", command=lambda: self.find_next_occurrence(direction="down"))
        self.search_menu.add_command(label="Find Previous", accelerator="Shift+F3", command=lambda: self.find_next_occurrence(direction="up"))
        
        # View Menu
        self.view_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="View", menu=self.view_menu)
        
        self.word_wrap_var = tk.BooleanVar(value=config.get("word_wrap", True))
        self.view_menu.add_checkbutton(label="Word Wrap", variable=self.word_wrap_var, command=self.toggle_word_wrap)

        self.theme_submenu = tk.Menu(self.view_menu, tearoff=0)
        self.view_menu.add_cascade(label="Themes", menu=self.theme_submenu)
        for theme_name_key in THEMES_DEFINITION.keys(): # Use THEMES_DEFINITION
            self.theme_submenu.add_command(label=theme_name_key, command=lambda t=theme_name_key: self.apply_theme_globally(t))
        
        # Tools Menu (placeholder for future, or for Font Settings)
        self.tools_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Tools", menu=self.tools_menu)
        self.tools_menu.add_command(label="Font Settings...", command=self.show_font_dialog)

        # Keyboard shortcuts
        mod_key = "Command" if platform.system() == "Darwin" else "Control"
        self.root.bind(f"<{mod_key}-n>", lambda e: self.new_file())
        self.root.bind(f"<{mod_key}-o>", lambda e: self.open_file())
        self.root.bind(f"<{mod_key}-s>", lambda e: self.save_file())
        self.root.bind(f"<{mod_key}-Shift-s>", lambda e: self.save_as_file())
        self.root.bind(f"<{mod_key}-w>", lambda e: self.close_current_tab())
        self.root.bind(f"<{mod_key}-q>", lambda e: self.exit_editor())
        self.root.bind(f"<{mod_key}-f>", lambda e: self.show_find_replace_dialog())
        self.root.bind("<F3>", lambda e: self.find_next_occurrence(direction="down"))
        self.root.bind("<Shift-F3>", lambda e: self.find_next_occurrence(direction="up"))
        self.root.bind(f"<{mod_key}-g>", lambda e: self.go_to_line())
        # Standard edit shortcuts are handled by Text widget or explicitly via menu commands for clarity

        # Apply theme to menus after all menus are created
        self.configure_menu_theme_colors()

    def configure_menu_theme_colors(self):
        if not hasattr(self, 'menu_bar'): # Check if menu_bar itself exists
            return
        
        self.menu_bar.config(bg=current_theme_settings['menu_bg'], fg=current_theme_settings['menu_fg'],
                             activebackground=current_theme_settings['menu_active_bg'],
                             activeforeground=current_theme_settings['menu_active_fg'],
                             relief=tk.FLAT, bd=0)
        
        # This inner function is fine as is, it operates on the 'menu' object passed to it.
        def _configure_submenu(menu): 
            menu.config(bg=current_theme_settings['menu_bg'], fg=current_theme_settings['menu_fg'],
                        activebackground=current_theme_settings['menu_active_bg'],
                        activeforeground=current_theme_settings['menu_active_fg'],
                        relief=tk.FLAT, tearoff=0, bd=0)
            # Iterate over menu items to style them individually if needed, especially for active state
            for i in range(menu.index(tk.END) + 1 if menu.index(tk.END) is not None else 0):
                item_type = menu.type(i)
                if item_type == "cascade":
                    # This cascades to submenus like recent_files_menu if 'menu' is file_menu
                    submenu_widget_name = menu.entrycget(i, "menu")
                    if submenu_widget_name: # Ensure the submenu actually exists
                        submenu = menu.nametowidget(submenu_widget_name)
                        _configure_submenu(submenu) 
                elif item_type in ["command", "checkbutton", "radiobutton"]:
                    # This styles individual items within the 'menu'
                    # Note: Direct background styling of individual menu items might be limited by OS/theme
                    menu.entryconfigure(i, 
                                        activebackground=current_theme_settings['menu_active_bg'],
                                        activeforeground=current_theme_settings['menu_active_fg']
                                        # background=current_theme_settings['menu_bg'] # Often overridden by OS
                                        )

        # Check for existence of each top-level menu attribute before trying to configure it
        if hasattr(self, 'file_menu'):
            _configure_submenu(self.file_menu)
        if hasattr(self, 'edit_menu'): # This check will prevent the AttributeError
            _configure_submenu(self.edit_menu)
        if hasattr(self, 'view_menu'):
            _configure_submenu(self.view_menu)
        if hasattr(self, 'search_menu'):
            _configure_submenu(self.search_menu)
        if hasattr(self, 'tools_menu'):
            _configure_submenu(self.tools_menu)
        # _configure_submenu(self.settings_menu) # If we add a dedicated settings menu

    def get_accelerator(self, key_char_combo):
        # key_char_combo can be "N", "Shift+S", etc.
        mod_key_symbol = "⌘" if platform.system() == "Darwin" else "Ctrl"
        parts = key_char_combo.split('+')
        accelerator_parts = [mod_key_symbol]
        
        for part in parts[:-1]: # Modifiers like Shift
            if part.lower() == "shift":
                accelerator_parts.append("Shift" if platform.system() != "Darwin" else "⇧")
        
        accelerator_parts.append(parts[-1].upper())
        return "+".join(accelerator_parts)

    def get_accelerator_redo(self):
        if platform.system() == "Darwin": return "⇧⌘Z" # Shift+Cmd+Z
        return "Ctrl+Y"

    # --- Edit Menu Actions (wrapper for text area events) ---
    def _get_ta_and_do(self, action_event_name=None, action_method_name=None):
        ta = self.get_current_text_area()
        if ta:
            if action_event_name: ta.event_generate(action_event_name)
            elif action_method_name: getattr(ta, action_method_name)()
    
    def edit_undo(self): self._get_ta_and_do(action_method_name="edit_undo")
    def edit_redo(self): self._get_ta_and_do(action_method_name="edit_redo")
    def edit_cut(self): self._get_ta_and_do(action_event_name="<<Cut>>")
    def edit_copy(self): self._get_ta_and_do(action_event_name="<<Copy>>")
    def edit_paste(self): self._get_ta_and_do(action_event_name="<<Paste>>")
    def edit_select_all(self): 
        ta = self.get_current_text_area()
        if ta:
            ta.tag_add(tk.SEL, "1.0", tk.END)
            ta.focus_set() # Ensure focus to see selection
            return 'break' # Prevents other bindings if any

    # --- File Operations ---
    def new_file(self, event=None):
        untitled_count = 1
        existing_titles = [self.notebook.tab(tid, "text").replace("*","") for tid in self.notebook.tabs()]
        while f"Untitled-{untitled_count}" in existing_titles:
            untitled_count += 1
        self.create_new_tab(title=f"Untitled-{untitled_count}")

    def open_file(self, event=None, filepath=None): # Modified to accept filepath
        if not filepath:
            filepath = filedialog.askopenfilename(
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("Markdown", "*.md"), ("All Files", "*.*")]
            )
        if not filepath: return

        for tab_id in self.notebook.tabs():
            frame = self.notebook.nametowidget(tab_id)
            content_frame = frame.winfo_children()[0]
            text_area = content_frame.winfo_children()[1]
            if hasattr(text_area, 'file_path') and text_area.file_path == filepath:
                self.notebook.select(tab_id)
                messagebox.showinfo("Info", f"{os.path.basename(filepath)} is already open.")
                return

        try:
            with open(filepath, "r", encoding='utf-8') as f:
                content = f.read()
            self.create_new_tab(title=os.path.basename(filepath), content=content, file_path=filepath)
        except Exception as e:
            messagebox.showerror("Error Opening File", f"Could not open file: {e}")

    def save_file(self, event=None, text_area_to_save=None, tab_id_to_save=None):
        current_text_area = text_area_to_save if text_area_to_save else self.get_current_text_area()
        if not current_text_area: return False

        current_tab_id = tab_id_to_save if tab_id_to_save else self.get_current_tab_id()
        current_file_path = getattr(current_text_area, 'file_path', None)

        if current_file_path:
            try:
                content = current_text_area.get("1.0", tk.END).rstrip('\n') + '\n' # Ensure trailing newline
                with open(current_file_path, "w", encoding='utf-8') as f:
                    f.write(content)
                
                self.unsaved_changes[current_tab_id] = False
                current_text_area.edit_modified(False)
                tab_text = self.notebook.tab(current_tab_id, "text")
                if tab_text.endswith("*"):
                    self.notebook.tab(current_tab_id, text=tab_text[:-1])
                self.update_window_title()
                self.add_recent_file(current_file_path) # Update MRU
                return True
            except Exception as e:
                messagebox.showerror("Error Saving File", f"Could not save file: {e}")
                return False
        else:
            return self.save_as_file(text_area_to_save=current_text_area, tab_id_to_save=current_tab_id)

    def save_as_file(self, event=None, text_area_to_save=None, tab_id_to_save=None):
        current_text_area = text_area_to_save if text_area_to_save else self.get_current_text_area()
        if not current_text_area: return False

        current_tab_id = tab_id_to_save if tab_id_to_save else self.get_current_tab_id()
        
        initial_filename = self.notebook.tab(current_tab_id, "text").replace("*","")
        if initial_filename.lower().startswith("untitled"):
            initial_filename = "" # Don't suggest "Untitled-1.txt" as default if it's truly new

        filepath = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("Python Files", "*.py"), ("All Files", "*.*")],
            initialfile=initial_filename
        )
        if not filepath: return False

        try:
            content = current_text_area.get("1.0", tk.END).rstrip('\n') + '\n'
            with open(filepath, "w", encoding='utf-8') as f:
                f.write(content)
            
            current_text_area.file_path = filepath
            self.unsaved_changes[current_tab_id] = False
            current_text_area.edit_modified(False)
            self.notebook.tab(current_tab_id, text=os.path.basename(filepath))
            self.update_window_title()
            self.add_recent_file(filepath) # Update MRU
            return True
        except Exception as e:
            messagebox.showerror("Error Saving File", f"Could not save file: {e}")
            return False

    def save_all_files(self):
        saved_any = False
        for tab_id in list(self.notebook.tabs()): # Iterate over a copy
            self.notebook.select(tab_id) # Switch to tab to ensure context
            frame = self.notebook.nametowidget(tab_id)
            content_frame = frame.winfo_children()[0]
            text_area = content_frame.winfo_children()[1]
            if self.unsaved_changes.get(tab_id, False) or not getattr(text_area, 'file_path', None):
                if self.save_file(text_area_to_save=text_area, tab_id_to_save=tab_id):
                    saved_any = True
                else: # Save was cancelled or failed for this tab
                    messagebox.showwarning("Save All", f"Could not save {self.notebook.tab(tab_id,'text')}. Save All operation may be incomplete.")
                    # Optionally break or ask user if they want to continue saving others
        if saved_any:
            messagebox.showinfo("Save All", "All changed files saved.")


    def close_current_tab(self, event=None):
        current_tab_id = self.get_current_tab_id()
        if not current_tab_id:
            if not self.notebook.tabs(): self.exit_editor(force_close_if_empty=True)
            return

        if self.unsaved_changes.get(current_tab_id, False):
            text_area = self.get_current_text_area()
            filename = os.path.basename(getattr(text_area, 'file_path', None) or self.notebook.tab(current_tab_id, "text").replace("*",""))
            response = messagebox.askyesnocancel("Unsaved Changes", f"Do you want to save changes to {filename}?")
            if response is True: # Yes
                if not self.save_file(): return # Save failed or was cancelled
            elif response is None: return # Cancel
        
        self.notebook.forget(current_tab_id)
        if current_tab_id in self.unsaved_changes: del self.unsaved_changes[current_tab_id]
        
        if not self.notebook.tabs():
            self.update_window_title()
            self.exit_editor(force_close_if_empty=True)
        else:
            self.on_tab_changed() # To update title and focus

    def close_all_tabs(self):
        # Iterate backwards because closing modifies the list of tabs
        for tab_id in reversed(list(self.notebook.tabs())):
            self.notebook.select(tab_id) # Bring tab to front
            self.close_current_tab()
            # If close_current_tab was cancelled (e.g. user hit cancel on save dialog), stop closing
            if tab_id in self.notebook.tabs(): 
                return 
        # If all tabs closed successfully, this point is reached.
        # exit_editor will be called by the last close_current_tab if it's force_close_if_empty


    def exit_editor(self, event=None, force_close_if_empty=False):
        if force_close_if_empty and not self.notebook.tabs():
            save_config(config)
            self.root.quit()
            return

        pending_saves_filenames = []
        tabs_to_save_ids = []

        for tab_id in self.notebook.tabs():
            if self.unsaved_changes.get(tab_id, False):
                tabs_to_save_ids.append(tab_id)
                frame = self.notebook.nametowidget(tab_id)
                content_frame = frame.winfo_children()[0]
                text_area = content_frame.winfo_children()[1]
                filename = os.path.basename(getattr(text_area, 'file_path', None) or self.notebook.tab(tab_id, "text").replace("*",""))
                pending_saves_filenames.append(filename)

        if pending_saves_filenames:
            file_list_str = "\n - ".join(pending_saves_filenames)
            response = messagebox.askyesnocancel(
                "Unsaved Changes", 
                f"You have unsaved changes in:\n - {file_list_str}\n\nSave changes before exiting?"
            )
            if response is True: # Yes, save
                for tab_id in tabs_to_save_ids:
                    self.notebook.select(tab_id)
                    frame = self.notebook.nametowidget(tab_id)
                    content_frame = frame.winfo_children()[0]
                    text_area = content_frame.winfo_children()[1]
                    if not self.save_file(text_area_to_save=text_area, tab_id_to_save=tab_id):
                        messagebox.showwarning("Exit Cancelled", f"Could not save {self.notebook.tab(tab_id,'text')}. Exiting cancelled.")
                        return # Don't exit
                # All successfully saved
            elif response is None: # Cancel exit
                return
            # If False (No, don't save), proceed to quit
        
        save_config(config) # Save settings like theme, font, recent files
        self.root.quit()

    # --- Recent Files ---
    def add_recent_file(self, filepath):
        if filepath in config["recent_files"]:
            config["recent_files"].remove(filepath)
        config["recent_files"].insert(0, filepath)
        config["recent_files"] = config["recent_files"][:MAX_RECENT_FILES]
        self.populate_recent_files_menu()
        # save_config(config) # Could save here, or on exit. Saving on exit is less frequent.

    def populate_recent_files_menu(self):
        self.recent_files_menu.delete(0, tk.END) # Clear existing items
        if not config["recent_files"]:
            self.recent_files_menu.add_command(label="(No recent files)", state=tk.DISABLED)
        else:
            for i, filepath in enumerate(config["recent_files"]):
                # Shorten very long paths for display
                display_name = filepath
                if len(filepath) > 70:
                    display_name = "..." + filepath[-67:]
                self.recent_files_menu.add_command(label=f"{i+1}. {display_name}", 
                                                 command=lambda fp=filepath: self.open_file(filepath=fp))
        self.configure_menu_theme_colors() # Re-apply theme to this dynamic menu

    # --- Go To Line ---
    def go_to_line(self, event=None):
        text_area = self.get_current_text_area()
        if not text_area: return

        line_num_str = simpledialog.askstring("Go To Line", "Enter line number:", parent=self.root)
        if line_num_str:
            try:
                line_num = int(line_num_str)
                total_lines = int(text_area.index('end-1c').split('.')[0])
                if 1 <= line_num <= total_lines:
                    text_area.mark_set(tk.INSERT, f"{line_num}.0")
                    text_area.see(f"{line_num}.0")
                    text_area.focus_set()
                    self.update_status_bar()
                    self.redraw_line_numbers()
                else:
                    messagebox.showwarning("Invalid Line", f"Line number must be between 1 and {total_lines}.")
            except ValueError:
                messagebox.showerror("Invalid Input", "Please enter a valid number.")

    # --- Font Settings ---
    def show_font_dialog(self):
        current_f = self.editor_font.actual()
        
        font_dialog = tk.Toplevel(self.root)
        font_dialog.title("Font Settings")
        font_dialog.transient(self.root)
        font_dialog.grab_set()
        font_dialog.resizable(False, False)
        font_dialog.configure(bg=current_theme_settings['bg'])

        # Add a modern title bar
        title_frame = ttk.Frame(font_dialog, style="TFrame")
        title_frame.pack(fill=tk.X, padx=10, pady=(10,0))
        ttk.Label(title_frame, text="Font Settings", style="TLabel", font=(self.editor_font.cget("family"), 12, "bold")).pack(side=tk.LEFT)

        main_frame = ttk.Frame(font_dialog, padding=15)
        main_frame.pack(expand=True, fill=tk.BOTH)

        # Font family selection with modern styling
        font_frame = ttk.Frame(main_frame)
        font_frame.pack(fill=tk.X, pady=(0,10))
        
        ttk.Label(font_frame, text="Font Family:", style="TLabel").pack(side=tk.LEFT, padx=(0,10))
        available_fonts = sorted(list(font.families()))
        self.font_family_var = tk.StringVar(value=current_f['family'])
        font_combo = ttk.Combobox(font_frame, textvariable=self.font_family_var, 
                                 values=available_fonts, state="readonly", width=30)
        font_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Font size selection with modern styling
        size_frame = ttk.Frame(main_frame)
        size_frame.pack(fill=tk.X, pady=(0,15))
        
        ttk.Label(size_frame, text="Font Size:", style="TLabel").pack(side=tk.LEFT, padx=(0,10))
        self.font_size_var = tk.IntVar(value=current_f['size'])
        font_size_spin = ttk.Spinbox(size_frame, from_=8, to=72, textvariable=self.font_size_var, 
                                    width=5, justify=tk.CENTER)
        font_size_spin.pack(side=tk.LEFT)

        # Preview section with modern styling
        preview_frame = ttk.LabelFrame(main_frame, text="Preview", padding=10)
        preview_frame.pack(fill=tk.X, pady=(0,15))
        
        preview_text = tk.Text(preview_frame, height=4, width=35, relief=tk.FLAT, borderwidth=1,
                              background=current_theme_settings['text_bg'],
                              foreground=current_theme_settings['text_fg'],
                              insertbackground=current_theme_settings['cursor_insert_color'])
        preview_text.insert(tk.END, "AaBbCcDdEe 12345\nTextra Editor\nModern UI Design\n2025 Edition")
        preview_text.config(state=tk.DISABLED)
        preview_text.pack(fill=tk.X, expand=True)

        def update_preview(*args):
            try:
                fam = self.font_family_var.get()
                siz = self.font_size_var.get()
                if fam and siz > 0:
                    preview_text.config(font=(fam, siz))
            except tk.TclError: pass

        self.font_family_var.trace_add("write", update_preview)
        self.font_size_var.trace_add("write", update_preview)
        update_preview()

        # Modern button styling
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5,0))
        
        def apply_font():
            new_family = self.font_family_var.get()
            new_size = self.font_size_var.get()
            try:
                self.editor_font.config(family=new_family, size=new_size)
                config["font_family"] = new_family
                config["font_size"] = new_size
                for tab_id in self.notebook.tabs():
                    frame = self.notebook.nametowidget(tab_id)
                    content_frame = frame.winfo_children()[0]
                    text_area = content_frame.winfo_children()[1]
                    line_numbers = content_frame.winfo_children()[0]
                    text_area.config(font=self.editor_font, tabs=(self.editor_font.measure('    ')))
                    self.redraw_line_numbers(text_area, line_numbers)
                font_dialog.destroy()
            except tk.TclError as e:
                messagebox.showerror("Font Error", f"Could not apply font: {e}", parent=font_dialog)

        # Modern button layout
        ok_button = ttk.Button(button_frame, text="Apply", command=apply_font, style="Accent.TButton")
        ok_button.pack(side=tk.RIGHT, padx=(5,0))
        cancel_button = ttk.Button(button_frame, text="Cancel", command=font_dialog.destroy)
        cancel_button.pack(side=tk.RIGHT)
        
        # Center dialog
        font_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (font_dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (font_dialog.winfo_height() // 2)
        font_dialog.geometry(f"+{x}+{y}")
        
        # Add accent button style
        self.style.configure("Accent.TButton",
            background=current_theme_settings.get('button_active_bg', current_theme_settings['menu_active_bg']),
            foreground=current_theme_settings.get('button_active_fg', current_theme_settings['menu_active_fg'])
        )
        
        font_dialog.mainloop()


    # --- Word Wrap ---
    def toggle_word_wrap(self):
        config["word_wrap"] = self.word_wrap_var.get()
        self.apply_word_wrap_to_current_tab()
        # save_config(config) # Optional: save immediately

    def apply_word_wrap_to_current_tab(self):
        text_area = self.get_current_text_area()
        if text_area:
            text_area.config(wrap=tk.WORD if config["word_wrap"] else tk.NONE)


    # --- Auto Indentation ---
    def handle_auto_indent(self, event, text_area):
        current_line_index = text_area.index(tk.INSERT).split('.')[0]
        prev_line_num = int(current_line_index) -1
        if prev_line_num < 1: return # No previous line

        prev_line_content = text_area.get(f"{prev_line_num}.0", f"{prev_line_num}.end")
        match = re.match(r"^(\s*)", prev_line_content) # Get leading whitespace
        indentation = match.group(1) if match else ""

        # Simple Python-like auto-indent: add extra indent if previous line ends with ':'
        if prev_line_content.strip().endswith(":"):
            # Use tab or spaces based on what's common or a setting
            # For now, just add 4 spaces if primarily spaces, or 1 tab if primarily tabs
            if '\t' in indentation:
                indentation += "\t"
            else: # Default to spaces or continue existing space indent
                # Check if current indentation consists of multiple of 4 spaces
                # if len(indentation) % 4 == 0 :
                indentation += "    " # Add typical tab worth of spaces
        
        # Insert newline character first (Tkinter does this automatically on <Return>)
        # Then insert the indentation AFTER the newline.
        # text_area.insert(tk.INSERT, "\n" + indentation) # This inserts before automatic newline.
        # So, schedule the insertion.
        text_area.after_idle(lambda: text_area.insert(tk.INSERT, indentation))
        
        # Return "break" is not strictly necessary here if Tkinter's default newline is fine,
        # but if we wanted full control over newline insertion, it would be.
        # return "break" # Prevents default newline handling if we manually inserted it.
        # For now, let Tkinter handle the newline, then we add indent.


    # --- Bracket Matching ---
    def handle_bracket_matching(self, event, text_area):
        text_area.tag_remove("bracket_match", "1.0", tk.END) # Clear previous matches

        # Get char before cursor
        cursor_index = text_area.index(tk.INSERT)
        char_before_cursor_index = text_area.index(f"{cursor_index}-1c")
        char_before = text_area.get(char_before_cursor_index)

        # Get char at cursor (or after if at end of line)
        char_at_cursor = text_area.get(cursor_index)

        brackets = {'(': ')', '[': ']', '{': '}'}
        closing_brackets = {v: k for k, v in brackets.items()}

        def find_match(start_char, start_index, direction):
            match_char = brackets.get(start_char) or closing_brackets.get(start_char)
            if not match_char: return None

            level = 1
            current_index = text_area.index(f"{start_index}{direction}1c") # Move one char in direction

            while True:
                if direction == '+': # Searching forward
                    if text_area.compare(current_index, ">=", tk.END): break
                else: # Searching backward
                    if text_area.compare(current_index, "<=", "1.0"): break
                
                char_at_current = text_area.get(current_index)

                if char_at_current == start_char: # e.g. another '(' when searching for ')'
                    level += 1
                elif char_at_current == match_char:
                    level -= 1
                    if level == 0:
                        return current_index
                
                current_index = text_area.index(f"{current_index}{direction}1c")
            return None

        match_found_indices = []

        # Check character before cursor
        if char_before in brackets: # Opening bracket
            match_index = find_match(char_before, char_before_cursor_index, '+')
            if match_index: match_found_indices = [char_before_cursor_index, match_index]
        elif char_before in closing_brackets: # Closing bracket
            match_index = find_match(char_before, char_before_cursor_index, '-')
            if match_index: match_found_indices = [char_before_cursor_index, match_index]
        
        # If no match from char_before, try char_at_cursor (useful if cursor is just before an opening bracket)
        if not match_found_indices:
            if char_at_cursor in brackets:
                match_index = find_match(char_at_cursor, cursor_index, '+')
                if match_index: match_found_indices = [cursor_index, match_index]
            elif char_at_cursor in closing_brackets:
                match_index = find_match(char_at_cursor, cursor_index, '-')
                if match_index: match_found_indices = [cursor_index, match_index]

        if match_found_indices:
            for idx in match_found_indices:
                text_area.tag_add("bracket_match", idx, f"{idx}+1c")


    # --- Find and Replace ---
    def show_find_replace_dialog(self):
        if self.find_dialog and self.find_dialog.winfo_exists():
            self.find_dialog.lift()
            self.find_dialog.focus_set()
            # Populate search text from current selection if any
            text_area = self.get_current_text_area()
            if text_area and text_area.tag_ranges(tk.SEL):
                sel_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
                if sel_text and '\n' not in sel_text and len(sel_text) < 100: # Reasonable selection
                    self.find_entry.delete(0, tk.END)
                    self.find_entry.insert(0, sel_text)
            return

        self.find_dialog = tk.Toplevel(self.root)
        self.find_dialog.title("Find / Replace")
        self.find_dialog.transient(self.root)
        self.find_dialog.resizable(False, False)
        self.find_dialog.protocol("WM_DELETE_WINDOW", self._clear_find_highlights_and_close_dialog)
        self.find_dialog.configure(bg=current_theme_settings['bg'])

        # Use ttk Frame for consistent styling
        main_fr = ttk.Frame(self.find_dialog, padding=10)
        main_fr.pack(expand=True, fill=tk.BOTH)

        ttk.Label(main_fr, text="Find:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.find_entry = ttk.Entry(main_fr, width=40)
        self.find_entry.grid(row=0, column=1, columnspan=2, sticky=tk.EW, pady=2, padx=5)
        self.find_entry.insert(0, self.current_find_options["text"])
        # Populate search text from current selection if any
        text_area = self.get_current_text_area()
        if text_area and text_area.tag_ranges(tk.SEL):
            sel_text = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            if sel_text and '\n' not in sel_text and len(sel_text) < 100: # Reasonable selection
                self.find_entry.delete(0, tk.END)
                self.find_entry.insert(0, sel_text)


        ttk.Label(main_fr, text="Replace with:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.replace_entry = ttk.Entry(main_fr, width=40)
        self.replace_entry.grid(row=1, column=1, columnspan=2, sticky=tk.EW, pady=2, padx=5)

        options_frame = ttk.Frame(main_fr)
        options_frame.grid(row=2, column=0, columnspan=3, pady=5, sticky=tk.W)
        
        self.current_find_options["match_case"] = tk.BooleanVar(value=self.current_find_options.get("match_case_val", False))
        ttk.Checkbutton(options_frame, text="Match Case", variable=self.current_find_options["match_case"]).pack(side=tk.LEFT, padx=3)
        
        self.current_find_options["regex"] = tk.BooleanVar(value=self.current_find_options.get("regex_val", False))
        ttk.Checkbutton(options_frame, text="Regex", variable=self.current_find_options["regex"]).pack(side=tk.LEFT, padx=3)
        
        direction_frame = ttk.Frame(main_fr) # Separate frame for radio buttons
        direction_frame.grid(row=3, column=1, columnspan=2, pady=2, sticky=tk.E)
        self.current_find_options["direction_down"] = tk.BooleanVar(value=self.current_find_options.get("direction_val", True))
        ttk.Radiobutton(direction_frame, text="Down", variable=self.current_find_options["direction_down"], value=True).pack(side=tk.LEFT)
        ttk.Radiobutton(direction_frame, text="Up", variable=self.current_find_options["direction_down"], value=False).pack(side=tk.LEFT, padx=5)


        button_frame = ttk.Frame(main_fr)
        button_frame.grid(row=4, column=0, columnspan=3, pady=(10,0), sticky=tk.EW)

        find_next_btn = ttk.Button(button_frame, text="Find Next", command=self.find_next_occurrence_from_dialog)
        find_next_btn.pack(side=tk.LEFT, padx=3)
        replace_btn = ttk.Button(button_frame, text="Replace", command=self.replace_occurrence)
        replace_btn.pack(side=tk.LEFT, padx=3)
        replace_all_btn = ttk.Button(button_frame, text="Replace All", command=self.replace_all_occurrences)
        replace_all_btn.pack(side=tk.LEFT, padx=3)
        
        # ttk.Button(button_frame, text="Close", command=self.find_dialog.destroy).pack(side=tk.RIGHT, padx=3)
        # Closing is handled by _clear_find_highlights_and_close_dialog via protocol

        self.find_entry.focus_set()
        self.find_dialog.bind('<Escape>', lambda e: self._clear_find_highlights_and_close_dialog())
        
        # Center dialog
        self.find_dialog.update_idletasks()
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - (self.find_dialog.winfo_width() // 2)
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - (self.find_dialog.winfo_height() // 2)
        self.find_dialog.geometry(f"+{x}+{y}")


    def _clear_find_highlights_and_close_dialog(self, event=None):
        text_area = self.get_current_text_area()
        if text_area:
            text_area.tag_remove("found", "1.0", tk.END) # Clear all "found" tags
        if self.find_dialog and self.find_dialog.winfo_exists():
            self.find_dialog.destroy()
        self.find_dialog = None


    def _update_find_options_from_dialog(self):
        self.current_find_options["text"] = self.find_entry.get()
        # Store the actual boolean values for persistence if dialog is reopened
        self.current_find_options["match_case_val"] = self.current_find_options["match_case"].get()
        self.current_find_options["regex_val"] = self.current_find_options["regex"].get()
        self.current_find_options["direction_val"] = self.current_find_options["direction_down"].get()


    def find_next_occurrence_from_dialog(self):
        self._update_find_options_from_dialog()
        direction = "down" if self.current_find_options["direction_down"].get() else "up"
        self.find_next_occurrence(direction=direction, from_dialog=True)

    def find_next_occurrence(self, direction="down", from_dialog=False):
        text_area = self.get_current_text_area()
        if not text_area: return

        if not from_dialog and self.find_dialog and self.find_dialog.winfo_exists():
             self._update_find_options_from_dialog() # Get latest text from entry if dialog is open
        
        search_term = self.current_find_options["text"]
        if not search_term:
            if from_dialog : messagebox.showwarning("Find", "Please enter text to find.", parent=self.find_dialog)
            return

        text_area.tag_remove("found", "1.0", tk.END) # Clear previous highlights

        nocase = not self.current_find_options["match_case"].get()
        use_regex = self.current_find_options["regex"].get()

        if direction == "down":
            start_index = text_area.index(tk.INSERT)
            # If there's a selection and we're searching down, start after the selection
            if text_area.tag_ranges(tk.SEL):
                sel_end_index = text_area.index(tk.SEL_END)
                # Check if current insert position is within or at start of selection, to avoid re-finding same.
                if text_area.compare(start_index, "<", sel_end_index):
                    start_index = sel_end_index
            
            end_index = tk.END
            count_var = tk.IntVar()
            pos = text_area.search(search_term, start_index, stopindex=end_index, nocase=nocase, regexp=use_regex, count=count_var)
        else: # up
            start_index = text_area.index(tk.INSERT)
            # If there's a selection and we're searching up, start before the selection
            if text_area.tag_ranges(tk.SEL):
                 sel_start_index = text_area.index(tk.SEL_FIRST)
                 # Check if current insert position is within or at end of selection
                 if text_area.compare(start_index, ">", sel_start_index):
                     start_index = sel_start_index

            end_index = "1.0"
            count_var = tk.IntVar()
            pos = text_area.search(search_term, start_index, stopindex=end_index, nocase=nocase, regexp=use_regex, backwards=True, count=count_var)

        if pos:
            match_len = count_var.get()
            if match_len == 0 and use_regex: # Regex might match zero-length string
                 # Try to advance one char and search again if zero-length match
                adv_idx = text_area.index(f"{pos}{'+1c' if direction == 'down' else '-1c'}")
                if text_area.compare(adv_idx, "!=", pos): # Ensure we can advance
                    return self.find_next_occurrence(direction=direction) # Recurse, starting from next char
                else: # Cannot advance, probably at end/start of doc
                    if from_dialog: messagebox.showinfo("Find", f"'{search_term}' not found.", parent=self.find_dialog)
                    return

            end_pos = f"{pos}+{match_len}c"
            text_area.tag_remove(tk.SEL, "1.0", tk.END) # Remove current selection
            text_area.tag_add(tk.SEL, pos, end_pos)    # Select the found text
            text_area.tag_add("found", pos, end_pos)   # Optionally highlight it too (e.g., yellow bg)
            text_area.mark_set(tk.INSERT, pos if direction=="up" else end_pos) # Move cursor to start/end of find
            text_area.see(pos)
            text_area.focus_set()
            if hasattr(text_area.tag_cget("found", "background"),'string') and not text_area.tag_cget("found", "background"):
                 text_area.tag_config("found", background=current_theme_settings.get('select_bg', "yellow"), 
                                             foreground=current_theme_settings.get('select_fg', None)) # Ensure 'found' tag is visible
        else:
            if from_dialog:
                messagebox.showinfo("Find", f"'{search_term}' not found.", parent=self.find_dialog if self.find_dialog and self.find_dialog.winfo_exists() else self.root)
            # Optional: Beep or status bar message if not found from F3/Shift+F3
            # Wrap search:
            wrapped_search_msg_shown = getattr(self, "_wrapped_search_msg_shown", False) # Track if msg shown in this search session
            if not wrapped_search_msg_shown:
                if from_dialog:
                    do_wrap = messagebox.askyesno("Find", "Reached end of document. Wrap around?", parent=self.find_dialog if self.find_dialog and self.find_dialog.winfo_exists() else self.root)
                else: # F3/Shift+F3 - maybe just wrap automatically or based on a setting
                    do_wrap = True # For now, auto-wrap for F3
                
                if do_wrap:
                    new_start = "1.0" if direction == "down" else tk.END
                    text_area.mark_set(tk.INSERT, new_start)
                    setattr(self, "_wrapped_search_msg_shown", True) # Mark that we are now in a wrapped search attempt
                    self.find_next_occurrence(direction=direction, from_dialog=from_dialog) # Try again from start/end
                    return # Important: return after recursive call
            
            # If we reach here, it means either wrap was no, or wrap also found nothing.
            if from_dialog: 
                pass # Message already shown or will be by recursive call's end
            elif wrapped_search_msg_shown : # F3/Shift+F3 and wrapped search failed
                self.root.bell() # Simple feedback
            
            delattr(self, "_wrapped_search_msg_shown") # Reset for next fresh search


    def replace_occurrence(self):
        text_area = self.get_current_text_area()
        if not text_area: return
        self._update_find_options_from_dialog() # Get latest text

        replace_term = self.replace_entry.get()
        search_term = self.current_find_options["text"]

        if not search_term:
            messagebox.showwarning("Replace", "Please enter text to find.", parent=self.find_dialog)
            return

        if text_area.tag_ranges(tk.SEL): # If something is selected
            sel_start = text_area.index(tk.SEL_FIRST)
            sel_end = text_area.index(tk.SEL_END)
            selected_text = text_area.get(sel_start, sel_end)
            
            # Verify if selected text actually matches the search criteria (important for regex, case)
            is_match = False
            if self.current_find_options["regex"].get():
                try:
                    flags = 0 if self.current_find_options["match_case"].get() else re.IGNORECASE
                    if re.fullmatch(search_term, selected_text, flags):
                        is_match = True
                except re.error: # Invalid regex
                    pass # Let find_next handle error reporting
            else:
                if self.current_find_options["match_case"].get():
                    if selected_text == search_term: is_match = True
                else:
                    if selected_text.lower() == search_term.lower(): is_match = True
            
            if is_match:
                text_area.delete(sel_start, sel_end)
                text_area.insert(sel_start, replace_term)
                # After replacing, find the next one automatically
                text_area.mark_set(tk.INSERT, f"{sel_start}+{len(replace_term)}c") # Move cursor after replaced text
                self.find_next_occurrence(direction="down" if self.current_find_options["direction_down"].get() else "up", from_dialog=True)
                return

        # If nothing selected or selection doesn't match, just find next
        self.find_next_occurrence(direction="down" if self.current_find_options["direction_down"].get() else "up", from_dialog=True)


    def replace_all_occurrences(self):
        text_area = self.get_current_text_area()
        if not text_area: return
        self._update_find_options_from_dialog()

        search_term = self.current_find_options["text"]
        replace_term = self.replace_entry.get()

        if not search_term:
            messagebox.showwarning("Replace All", "Please enter text to find.", parent=self.find_dialog)
            return

        content = text_area.get("1.0", tk.END)
        nocase = not self.current_find_options["match_case"].get()
        use_regex = self.current_find_options["regex"].get()
        
        replacements_count = 0
        if use_regex:
            try:
                flags = 0 if nocase else re.IGNORECASE # re.IGNORECASE means nocase=True
                # When using re.sub with user input for replacement_string,
                # be mindful of backreferences like \1, \g<name>.
                # For simple replacement, this is fine. For complex, might need to escape replace_term.
                new_content, replacements_count = re.subn(search_term, replace_term, content, flags=flags)
            except re.error as e:
                messagebox.showerror("Regex Error", f"Invalid regular expression: {e}", parent=self.find_dialog)
                return
        else:
            # Manual replace for non-regex to handle nocase
            new_content = []
            last_pos = 0
            search_len = len(search_term)
            
            s_term_to_use = search_term if nocase else search_term.lower()
            c_to_use_for_search = content if nocase else content.lower()

            start_find_idx = 0
            while True:
                idx = c_to_use_for_search.find(s_term_to_use, start_find_idx)
                if idx == -1:
                    new_content.append(content[last_pos:])
                    break
                new_content.append(content[last_pos:idx])
                new_content.append(replace_term)
                last_pos = idx + search_len
                start_find_idx = idx + search_len # search from after this match
                replacements_count += 1
            new_content = "".join(new_content)


        if replacements_count > 0:
            # Preserve cursor and scroll position if possible (tricky with full replace)
            # current_cursor = text_area.index(tk.INSERT)
            # current_scroll = text_area.yview()

            text_area.delete("1.0", tk.END)
            text_area.insert("1.0", new_content)
            text_area.edit_modified(True) # Mark as modified
            self.on_text_change() # Update status, line numbers etc.
            messagebox.showinfo("Replace All", f"Replaced {replacements_count} occurrence(s).", parent=self.find_dialog)
            
            # text_area.mark_set(tk.INSERT, current_cursor) # May not be valid
            # text_area.yview_moveto(current_scroll[0])
        else:
            messagebox.showinfo("Replace All", "No occurrences found.", parent=self.find_dialog)
        
        text_area.tag_remove("found", "1.0", tk.END) # Clear any highlights


if __name__ == "__main__":
    root = tk.Tk()
    # Ensure config and theme files can be loaded/created before app starts
    if not os.path.exists(THEME_FILE): load_themes_definition()
    if not os.path.exists(CONFIG_FILE): load_config()
    
    app = TextEditor(root)
    root.mainloop()