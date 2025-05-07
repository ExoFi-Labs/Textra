# Textra - A Modern Python Text Editor

Textra is a feature-rich, cross-platform text editor built with Python and the Tkinter GUI toolkit. It aims to provide a modern, user-friendly experience with essential coding and text manipulation features, inspired by editors like Notepad++.

*(Consider adding a screenshot of Textra here once it's looking good)*
`<!-- ![Textra Screenshot](path/to/your/screenshot.png) -->`

## Features

Textra comes packed with a variety of features to enhance your text editing workflow:

*   **Tabbed Interface:** Open and manage multiple files in separate tabs.
*   **Theming Support:**
    *   Comes with a rich selection of pre-built themes:
        *   Darkula (Default)
        *   Classic Light
        *   Nord
        *   Tokyo Night
        *   Catppuccin
        *   One Dark
        *   Warm Brown
        *   Cyberpunk
        *   Forest
        *   Sunset
        *   Ocean
    *   Easily switch themes via the View menu.
    *   Themes are customizable via `editor_themes.json`.
*   **Customizable Fonts:**
    *   Change editor font family and size through a dedicated dialog (Tools > Font Settings...).
    *   Settings are saved across sessions.
    *   Defaults to modern coding fonts like Cascadia Code (Windows), JetBrains Mono (macOS), or Fira Code (Linux).
*   **Line Numbers:** A dedicated, themed line number bar that scrolls with the text.
*   **Status Bar:**
    *   Displays current line and column number.
    *   Shows character count and word count.
    *   Displays selection length (lines, characters) when text is selected.
*   **Find and Replace:**
    *   Comprehensive dialog with options for:
        *   Match Case
        *   Regular Expressions (Regex)
        *   Search Direction (Up/Down)
    *   Find Next (F3), Find Previous (Shift+F3) shortcuts.
    *   Replace current occurrence and Replace All.
    *   Wrap-around search.
*   **File Management:**
    *   New Tab, Open, Save, Save As, Save All.
    *   Close Tab, Close All Tabs.
    *   Prompts to save unsaved changes on close/exit.
    *   Recent Files menu for quick access (File > Open Recent).
*   **Editing Enhancements:**
    *   Standard Undo/Redo, Cut/Copy/Paste, Select All.
    *   Go to Line (Ctrl+G / Cmd+G).
    *   Word Wrap toggle (View > Word Wrap).
    *   Basic Auto-Indentation (indents new lines, adds extra indent after lines ending with `:`).
    *   Bracket Matching (highlights matching `()`, `[]`, `{}`).
*   **Cross-Platform:** Built with Python and Tkinter, designed to run on Windows, macOS, and Linux.
*   **Persistent Settings:** Remembers your chosen theme, font, recent files, and word wrap preference across sessions via `textra_config.json`.
*   **Modern Look and Feel:** Uses `ttk` themed widgets and custom styling for a more contemporary appearance than standard Tkinter. The UI elements and dialogs have been updated for a sleeker design.

## Requirements

*   **Python 3.x:** Textra is developed using Python 3. (Tkinter is usually included with standard Python installations).
*   **(Optional but Recommended) Modern Coding Fonts:** For the best visual experience, having fonts like Cascadia Code, JetBrains Mono, or Fira Code installed is recommended. Textra will fall back to system defaults if these are not found.

## Getting Started

1.  **Clone the Repository (or Download the Code):**
    ```bash
    git clone https://github.com/your-username/textra.git
    cd textra
    ```
    *(Replace `your-username/textra.git` with your actual repository URL)*

2.  **Run Textra:**
    Execute the main Python script (e.g., `textra.py` or whatever you named it):
    ```bash
    python textra.py
    ```

    On the first run, Textra will automatically create two JSON files in the same directory if they don't exist:
    *   `textra_config.json`: Stores your settings (theme, font, recent files, word wrap).
    *   `editor_themes.json`: Contains the color definitions for the available themes. If you have an older version of this file, Textra will attempt to update it with any new theme keys or default themes.

## Usage

### Menus

*   **File:** Standard file operations (New, Open, Save, Close), recent files, and exit.
*   **Edit:** Undo, Redo, Cut, Copy, Paste, Select All, Go to Line.
*   **Search:** Find/Replace dialog, Find Next, Find Previous.
*   **View:** Toggle Word Wrap, select Themes.
*   **Tools:** Font Settings.

### Keyboard Shortcuts

Textra supports common keyboard shortcuts:

*   **File Operations:**
    *   New Tab: `Ctrl+N` (Windows/Linux) / `Cmd+N` (macOS)
    *   Open: `Ctrl+O` / `Cmd+O`
    *   Save: `Ctrl+S` / `Cmd+S`
    *   Save As: `Ctrl+Shift+S` / `Cmd+Shift+S`
    *   Close Tab: `Ctrl+W` / `Cmd+W`
    *   Exit: `Ctrl+Q` / `Cmd+Q`
*   **Editing:**
    *   Undo: `Ctrl+Z` / `Cmd+Z`
    *   Redo: `Ctrl+Y` (Windows/Linux) / `Cmd+Shift+Z` (macOS)
    *   Cut: `Ctrl+X` / `Cmd+X`
    *   Copy: `Ctrl+C` / `Cmd+C`
    *   Paste: `Ctrl+V` / `Cmd+V`
    *   Select All: `Ctrl+A` / `Cmd+A`
    *   Go to Line: `Ctrl+G` / `Cmd+G`
*   **Search:**
    *   Find/Replace Dialog: `Ctrl+F` / `Cmd+F`
    *   Find Next: `F3`
    *   Find Previous: `Shift+F3`

*(Note: Accelerator symbols in menus might differ slightly based on your operating system.)*

## Customization

### Themes

You can customize existing themes or add new ones by editing the `editor_themes.json` file. Each theme is a JSON object with color definitions for various UI elements. Textra uses a theme template to ensure all necessary color keys are present; if you add a new theme or have an older `editor_themes.json`, missing keys will be populated with defaults from the "Darkula" theme template.

A complete theme structure includes keys like:
```json
{
    "Your New Theme Name": {
        "bg": "#RRGGBB",             // Main background
        "fg": "#RRGGBB",             // Main foreground (text)
        "text_bg": "#RRGGBB",        // Text area background
        "text_fg": "#RRGGBB",        // Text area foreground
        "select_bg": "#RRGGBB",      // Selected text background
        "select_fg": "#RRGGBB",      // Selected text foreground
        "cursor_insert_color": "#RRGGBB", // Cursor color
        "menu_bg": "#RRGGBB",        // Menu background
        "menu_fg": "#RRGGBB",        // Menu foreground
        "menu_active_bg": "#RRGGBB", // Active/hovered menu item background
        "menu_active_fg": "#RRGGBB", // Active/hovered menu item foreground
        "statusbar_bg": "#RRGGBB",   // Status bar background
        "statusbar_fg": "#RRGGBB",   // Status bar foreground
        "notebook_bg": "#RRGGBB",    // Notebook (tab area) background
        "tab_bg": "#RRGGBB",         // Inactive tab background
        "tab_fg": "#RRGGBB",         // Inactive tab foreground
        "tab_active_bg": "#RRGGBB",  // Active tab background
        "tab_active_fg": "#RRGGBB",  // Active tab foreground
        "linenum_bg": "#RRGGBB",     // Line number bar background
        "linenum_fg": "#RRGGBB",     // Line number bar foreground
        "bracket_match_bg": "#RRGGBB",// Matched bracket background
        "bracket_match_fg": "#RRGGBB",// Matched bracket foreground
        "button_bg": "#RRGGBB",      // Default button background
        "button_fg": "#RRGGBB",      // Default button foreground
        "button_active_bg": "#RRGGBB",// Active/hovered button background
        "button_active_fg": "#RRGGBB",// Active/hovered button foreground
        "indicator": "#RRGGBB"       // Checkbutton/Radiobutton indicator color
    }
}