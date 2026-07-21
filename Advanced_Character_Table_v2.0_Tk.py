#!/usr/bin/env python3
"""
Tablica Znaków Unicode — Wersja Rozszerzona (v2.0)
Alternatywa dla windowsowskiego charmap.exe z zaawansowanymi funkcjami.
Wymaga tylko Python 3 (wbudowany tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog, simpledialog
import unicodedata
import os
import sys
import json
import urllib.parse

APP_VERSION = "v2.0"

LANG = {
    "en": {
        "title": "Advanced Character Table",
        "category": "Category:",
        "search": "Search:",
        "filter_type": "Type:",
        "count_chars": "{} characters",
        "count_char": "{} character",
        "no_name": "(no name)",
        "click_hint": "Click a character to see details",
        "copy_char": "📋 Copy Char",
        "copy_seq": "Copy Hex",
        "copied": "✓ Copied!",
        "favorites": "⭐ Palettes",
        "add_to_fav": "Add to current palette",
        "remove_from_fav": "Remove from palette",
        "add_to_macro": "Assign to Quick Slot {}",
        "about": "About",
        "about_title": "About Advanced Character Table",
        "program_name": "Advanced Character Table",
        "version": "Version:",
        "author": "Author:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Search all",
        "history": "🕘 History",
        "analyzer": "📋 Clip Analyzer",
        "options": "⋮",
        "export_fav": "Export current palette…",
        "import_fav": "Import palette…",
        "new_palette": "Create new palette…",
        "delete_palette": "Delete current palette",
        "clear_history": "Clear history",
        "export_title": "Export Palette",
        "import_title": "Import Palette",
        "export_success": "Exported {} character(s) to:\n{}",
        "import_success": "Imported {} new character(s).",
        "export_error": "Export failed:\n{}",
        "import_error": "Import failed:\n{}",
        "no_favorites": "Empty palette. Right-click a character to add it here.",
        "no_history": "No characters copied yet.",
        "no_analyzer": "Clipboard is empty or contains no valid text characters.",
        "shortcuts_hint": "Ctrl+C: copy selected  •  Ctrl+F: focus search  •  Esc: clear filter",
        "palette_prompt_title": "New Palette",
        "palette_prompt_msg": "Enter palette name:",
        "quick_access": "Quick Slots:",
        "filter_types": ["All", "Uppercase", "Lowercase", "Numbers", "Punctuation", "Symbols"],
        "categories": [
            "Basic Latin", "Latin Extended", "IPA Phonetic Alphabet", "Greek and Coptic",
            "Cyrillic", "Hebrew", "Arabic", "Currency", "Letterlike Symbols",
            "Punctuation", "Arrows", "Mathematical", "Misc Technical", "Geometric Shapes",
            "Misc Symbols", "Dingbats", "Emoji (Basic)", "Emoji (Transport)",
            "Emoji (Faces/Gestures)", "Mahjong and Cards"
        ]
    },
    "pl": {
        "title": "Zaawansowana Tablica Znaków",
        "category": "Kategoria:",
        "search": "Szukaj:",
        "filter_type": "Typ:",
        "count_chars": "{} znaków",
        "count_char": "{} znak",
        "no_name": "(brak nazwy)",
        "click_hint": "Kliknij znak, aby zobaczyć szczegóły",
        "copy_char": "📋 Kopiuj znak",
        "copy_seq": "Kopiuj kod",
        "copied": "✓ Skopiowano!",
        "favorites": "⭐ Zestawy/Palety",
        "add_to_fav": "Dodaj do bieżącej palety",
        "remove_from_fav": "Usuń z tej palety",
        "add_to_macro": "Przypisz do Szybkiego Slotu {}",
        "about": "O programie",
        "about_title": "O programie Advanced Character Table",
        "program_name": "Advanced Character Table",
        "version": "Wersja:",
        "author": "Autor:",
        "mail": "Mail:",
        "github": "GitHub:",
        "global_search": "Szukaj wszędzie",
        "history": "🕘 Historia",
        "analyzer": "📋 Analizuj schowek",
        "options": "⋮",
        "export_fav": "Eksportuj bieżącą paletę…",
        "import_fav": "Importuj paletę…",
        "new_palette": "Stwórz nową paletę…",
        "delete_palette": "Usuń bieżącą paletę",
        "clear_history": "Wyczyść historię",
        "export_title": "Eksportuj paletę",
        "import_title": "Importuj paletę",
        "export_success": "Wyeksportowano {} znaków do:\n{}",
        "import_success": "Zaimportowano {} nowych znaków.",
        "export_error": "Eksport nie powiódł się:\n{}",
        "import_error": "Import nie powiódł się:\n{}",
        "no_favorites": "Pusta paleta. Kliknij prawym przyciskiem myszy na znak, aby go dodać.",
        "no_history": "Nie skopiowano jeszcze żadnego znaku.",
        "no_analyzer": "Schowek jest pusty lub nie zawiera prawidłowych znaków tekstowych.",
        "shortcuts_hint": "Ctrl+C: kopiuj znak  •  Ctrl+F: focus na szukanie  •  Esc: resetuj filtry",
        "palette_prompt_title": "Nowa Paleta",
        "palette_prompt_msg": "Podaj nazwę nowej palety:",
        "quick_access": "Szybkie Sloty:",
        "filter_types": ["Wszystkie", "Wielkie litery", "Małe litery", "Cyfry/Liczby", "Interpunkcja", "Symbole"],
        "categories": [
            "Łacińskie podstawowe", "Łacińskie rozszerzone", "Alfabet fonetyczny (IPA)", "Grecki i koptyjski",
            "Cyrylica", "Hebrajski", "Arabski", "Waluty", "Literopodobne symbole",
            "Znaki interpunkcji", "Strzałki", "Matematyczne", "Różne techniczne", "Geometryczne kształty",
            "Różne symbole", "Dingbats", "Emoji (podstawowe)", "Emoji (transport)",
            "Emoji (twarze/gesty)", "Mahjong i karty"
        ]
    }
}

CATEGORIES = [
    ("Basic Latin",     0x0020, 0x007E),
    ("Latin Extended",    0x00C0, 0x02AF),
    ("IPA Phonetic Alphabet", 0x0250, 0x02AF),
    ("Greek and Coptic",       0x0370, 0x03FF),
    ("Cyrillic",                 0x0400, 0x04FF),
    ("Hebrew",                0x0590, 0x05FF),
    ("Arabic",                  0x0600, 0x06FF),
    ("Currency",                   0x20A0, 0x20CF),
    ("Letterlike Symbols",    0x2100, 0x214F),
    ("Punctuation",       0x2000, 0x206F),
    ("Arrows",                 0x2190, 0x21FF),
    ("Mathematical",             0x2200, 0x22FF),
    ("Misc Technical",         0x2300, 0x23FF),
    ("Geometric Shapes",    0x25A0, 0x25FF),
    ("Misc Symbols",            0x2600, 0x26FF),
    ("Dingbats",                 0x2700, 0x27BF),
    ("Emoji (Basic)",       0x1F300, 0x1F5FF),
    ("Emoji (Transport)",        0x1F680, 0x1F6FF),
    ("Emoji (Faces/Gestures)",     0x1F900, 0x1F9FF),
    ("Mahjong and Cards",          0x1F000, 0x1F0FF),
]

COLS = 16
HISTORY_MAX = 60

FONT_FAMILY = "Segoe UI"
FONT_NORMAL = (FONT_FAMILY, 10)
FONT_SMALL = (FONT_FAMILY, 9)
FONT_TINY = (FONT_FAMILY, 8)
FONT_BOLD = (FONT_FAMILY, 10, "bold")
FONT_TITLE = (FONT_FAMILY, 13, "bold")
FONT_CHAR = (FONT_FAMILY, 14)
FONT_PREVIEW = (FONT_FAMILY, 34)
FONT_MONO = ("Consolas", 9)

BG = "#f3f4f9"
PANEL_BG = "#ffffff"
BORDER = "#e1e4ec"
TEXT = "#1e2130"
TEXT_MUTED = "#767c8c"
TEXT_SUBTLE = "#9aa0ad"
ACCENT = "#4f46e5"
ACCENT_HOVER = "#4338ca"
ACCENT_LIGHT = "#ecebfd"

BTN_BG = "#ffffff"
BTN_HOVER = "#eef0f7"
BTN_BORDER = "#dadde6"
BTN_ACTIVE_BG = "#e3e0fb"

CHAR_BTN_BG = "#ffffff"
CHAR_BTN_HOVER = "#ecebfd"
CHAR_BTN_SELECTED = "#4f46e5"
CHAR_BTN_SELECTED_FG = "#ffffff"
CHAR_BTN_FAV = "#fff3cd"
CHAR_BTN_FAV_HOVER = "#ffe9a8"

SUCCESS_BG = "#dcfce7"
SUCCESS_TEXT = "#15803d"
SCROLLBAR_BG = "#c7cbd8"
SCROLLBAR_TROUGH = "#f3f4f9"
TOOLTIP_BG = "#1e2130"
TOOLTIP_FG = "#ffffff"

def _add_hover(btn, hover_bg, normal_bg=None):
    if normal_bg is not None:
        btn._normal_bg = normal_bg
    else:
        btn._normal_bg = btn.cget("bg")

    def _on_enter(_event=None):
        btn.config(bg=hover_bg)
    def _on_leave(_event=None):
        btn.config(bg=getattr(btn, "_normal_bg", hover_bg))

    btn.bind("<Enter>", _on_enter, add="+")
    btn.bind("<Leave>", _on_leave, add="+")

def set_normal_bg(btn, color):
    btn._normal_bg = color
    btn.config(bg=color)

_all_chars_cache = None

def get_chars(start, end):
    result = []
    for cp in range(start, end + 1):
        try:
            ch = chr(cp)
            cat = unicodedata.category(ch)
            if cat not in ("Cc", "Cs", "Co"):
                result.append(cp)
        except (ValueError, OverflowError):
            pass
    return result

def get_all_chars():
    global _all_chars_cache
    if _all_chars_cache is None:
        seen = {}
        for _, start, end in CATEGORIES:
            for cp in get_chars(start, end):
                seen[cp] = True
        _all_chars_cache = sorted(seen.keys())
    return _all_chars_cache

def char_name(cp, lang="en"):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return LANG[lang]["no_name"]

def get_resource_path(filename):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)

def get_app_data_dir():
    app_name = "AdvancedCharacterTable"
    if sys.platform.startswith("win"):
        base = os.environ.get("APPDATA") or os.path.expanduser("~")
    elif sys.platform == "darwin":
        base = os.path.join(os.path.expanduser("~"), "Library", "Application Support")
    else:
        base = os.environ.get("XDG_CONFIG_HOME") or os.path.join(os.path.expanduser("~"), ".config")
    path = os.path.join(base, app_name)
    os.makedirs(path, exist_ok=True)
    return path

class ToolTip:
    def __init__(self, widget, text_func, delay=450):
        self.widget = widget
        self.text_func = text_func
        self.delay = delay
        self.tipwindow = None
        self.after_id = None
        widget.bind("<Enter>", self._schedule, add="+")
        widget.bind("<Leave>", self._hide, add="+")
        widget.bind("<Button-1>", self._hide, add="+")

    def _schedule(self, _event=None):
        self._cancel()
        self.after_id = self.widget.after(self.delay, self._show)

    def _show(self):
        text = self.text_func()
        if not text or self.tipwindow is not None:
            return
        try:
            x = self.widget.winfo_rootx() + 10
            y = self.widget.winfo_rooty() + self.widget.winfo_height() + 6
        except tk.TclError:
            return
        tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(
            tw, text=text, justify="left", background=TOOLTIP_BG, foreground=TOOLTIP_FG,
            relief="flat", borderwidth=0, font=FONT_SMALL, padx=8, pady=5
        )
        label.pack()
        self.tipwindow = tw

    def _cancel(self):
        if self.after_id is not None:
            self.widget.after_cancel(self.after_id)
            self.after_id = None

    def _hide(self, _event=None):
        self._cancel()
        if self.tipwindow is not None:
            self.tipwindow.destroy()
            self.tipwindow = None

class TablicaZnakow(tk.Tk):
    def __init__(self):
        super().__init__()

        self.settings_file = os.path.join(get_app_data_dir(), "settings_v2.json")
        self.palettes_file = os.path.join(get_app_data_dir(), "palettes.json")
        self.history_file = os.path.join(get_app_data_dir(), "history.txt")
        
        settings = self._load_settings()
        self.lang = settings.get("lang", "en")
        self.macros = settings.get("macros", ["", "", "", "", "", "", "", ""])
        
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')
        self.minsize(980, 640)
        self.configure(bg=BG)
        self._setup_ttk_style()

        window_width = 1040
        window_height = 720
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.selected_cp = None
        self.char_buttons = []
        self.char_button_map = {}
        self.tooltips = []
        self.history = []
        self.clipboard_chars = []
        
        # System Zaawansowanych Palet
        self.palettes = {"⭐ Ulubione": []}
        self.current_palette_name = "⭐ Ulubione"
        self._load_palettes()
        self._load_history()
        
        # "category" | "favorites" | "history" | "analyzer"
        self.view_mode = "category"

        self._build_ui()
        self._bind_shortcuts()
        self._set_view_mode("category")

    def _load_settings(self):
        if os.path.exists(self.settings_file):
            try:
                with open(self.settings_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {}

    def _save_settings(self):
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump({"lang": self.lang, "macros": self.macros}, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _load_palettes(self):
        if os.path.exists(self.palettes_file):
            try:
                with open(self.palettes_file, "r", encoding="utf-8") as f:
                    self.palettes = json.load(f)
                if not self.palettes or "⭐ Ulubione" not in self.palettes:
                    self.palettes["⭐ Ulubione"] = []
                self.current_palette_name = list(self.palettes.keys())[0]
            except Exception:
                self.palettes = {"⭐ Ulubione": []}

    def _save_palettes(self):
        try:
            with open(self.palettes_file, "w", encoding="utf-8") as f:
                json.dump(self.palettes, f, ensure_ascii=False, indent=2)
        except OSError:
            pass

    def _setup_ttk_style(self):
        style = ttk.Style(self)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure(
            "TCombobox",
            fieldbackground=PANEL_BG, background=PANEL_BG, foreground=TEXT,
            arrowcolor=ACCENT, bordercolor=BORDER, lightcolor=PANEL_BG,
            darkcolor=PANEL_BG, padding=4, relief="flat",
        )
        style.map(
            "TCombobox",
            fieldbackground=[("readonly", PANEL_BG)],
            foreground=[("readonly", TEXT)],
            bordercolor=[("focus", ACCENT)],
        )
        style.configure("TCheckbutton", background=BG, foreground=TEXT, font=FONT_SMALL)
        style.map("TCheckbutton", background=[("active", BG)])

        style.configure(
            "Vertical.TScrollbar",
            background=SCROLLBAR_BG, troughcolor=SCROLLBAR_TROUGH,
            bordercolor=BG, arrowcolor=TEXT_MUTED, relief="flat", width=12,
        )
        style.map("Vertical.TScrollbar", background=[("active", ACCENT)])

    def _flat_button(self, parent, text, command, font=FONT_NORMAL, padx=12, pady=6,
                      bg=BTN_BG, hover=BTN_HOVER, fg=TEXT, state="normal"):
        btn = tk.Button(
            parent, text=text, font=font, command=command,
            bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
            disabledforeground=TEXT_SUBTLE,
            relief="flat", bd=0, padx=padx, pady=pady, cursor="hand2",
            highlightthickness=1, highlightbackground=BTN_BORDER, highlightcolor=BTN_BORDER,
            state=state,
        )
        _add_hover(btn, hover, normal_bg=bg)
        return btn

    def _switch_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        self.title(f'{LANG[self.lang]["title"]} {APP_VERSION}')
        self._save_settings()
        self._update_ui_text()
        self.search_var.set("")
        self._refresh_current_view()

    def _update_ui_text(self):
        self.cat_label.config(text=LANG[self.lang]["category"])
        self.search_label.config(text=LANG[self.lang]["search"])
        self.filter_label.config(text=LANG[self.lang]["filter_type"])
        self.fav_btn.config(text=LANG[self.lang]["favorites"])
        self.history_btn.config(text=LANG[self.lang]["history"])
        self.analyzer_btn.config(text=LANG[self.lang]["analyzer"])
        self.global_chk.config(text=LANG[self.lang]["global_search"])
        self.lang_btn.config(text="PL" if self.lang == "en" else "EN")
        self.about_btn.config(text=LANG[self.lang]["about"])
        self.options_btn.config(text=LANG[self.lang]["options"])
        self.shortcuts_label.config(text=LANG[self.lang]["shortcuts_hint"])
        self.macro_title_label.config(text=LANG[self.lang]["quick_access"])
        if self.selected_cp is None:
            self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.copy_btn.config(text=LANG[self.lang]["copy_char"])
        self.copy_seq_btn.config(text=LANG[self.lang]["copy_seq"])
        
        current_idx = self.cat_combo.current()
        self.cat_combo.config(values=LANG[self.lang]["categories"])
        self.cat_combo.current(max(0, current_idx))

        current_f_idx = self.filter_combo.current()
        self.filter_combo.config(values=LANG[self.lang]["filter_types"])
        self.filter_combo.current(max(0, current_f_idx))
        self._update_palette_combo_list()

    def _build_ui(self):
        accent_bar = tk.Frame(self, bg=ACCENT, height=3)
        accent_bar.pack(fill="x", side="top")

        top_wrap = tk.Frame(self, bg=PANEL_BG, highlightthickness=1, highlightbackground=BORDER)
        top_wrap.pack(fill="x")
        top = tk.Frame(top_wrap, bg=PANEL_BG, pady=10, padx=16)
        top.pack(fill="x")

        row1 = tk.Frame(top, bg=PANEL_BG)
        row1.pack(fill="x")
        row2 = tk.Frame(top, bg=PANEL_BG)
        row2.pack(fill="x", pady=(10, 0))

        # Kategoria
        self.cat_label = tk.Label(row1, text=LANG[self.lang]["category"], bg=PANEL_BG, fg=TEXT, font=FONT_NORMAL)
        self.cat_label.pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(row1, textvariable=self.cat_var, values=LANG[self.lang]["categories"], state="readonly", width=22, font=FONT_NORMAL)
        self.cat_combo.current(0)
        self.cat_combo.pack(side="left", padx=(6, 12))
        self.cat_combo.bind("<<ComboboxSelected>>", self._on_category)

        # Szukaj tekstowo
        self.search_label = tk.Label(row1, text=LANG[self.lang]["search"], bg=PANEL_BG, fg=TEXT, font=FONT_NORMAL)
        self.search_label.pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        self.search_entry = tk.Entry(row1, textvariable=self.search_var, font=FONT_NORMAL, width=14, relief="flat", bg=PANEL_BG, fg=TEXT, insertbackground=TEXT, highlightthickness=1, highlightbackground=BTN_BORDER, highlightcolor=ACCENT)
        self.search_entry.pack(side="left", padx=(6, 12), ipady=4)

        # Zaawansowane Filtrowanie Typograficzne
        self.filter_label = tk.Label(row1, text=LANG[self.lang]["filter_type"], bg=PANEL_BG, fg=TEXT, font=FONT_NORMAL)
        self.filter_label.pack(side="left")
        self.filter_var = tk.StringVar()
        self.filter_combo = ttk.Combobox(row1, textvariable=self.filter_var, values=LANG[self.lang]["filter_types"], state="readonly", width=14, font=FONT_NORMAL)
        self.filter_combo.current(0)
        self.filter_combo.pack(side="left", padx=(6, 10))
        self.filter_combo.bind("<<ComboboxSelected>>", self._on_search)

        self.global_search_var = tk.BooleanVar(value=False)
        self.global_chk = tk.Checkbutton(row1, text=LANG[self.lang]["global_search"], variable=self.global_search_var, command=self._on_search, bg=PANEL_BG, fg=TEXT, font=FONT_SMALL)
        self.global_chk.pack(side="left", padx=(5, 0))

        self.count_label = tk.Label(row1, text="", bg=PANEL_BG, font=FONT_SMALL, fg=TEXT_MUTED)
        self.count_label.pack(side="right")

        # Row 2 — Widoki i system palet
        self.fav_btn = self._flat_button(row2, LANG[self.lang]["favorites"], self._toggle_favorites_panel, padx=10, pady=5)
        self.fav_btn.pack(side="left")

        self.palette_var = tk.StringVar()
        self.palette_combo = ttk.Combobox(row2, textvariable=self.palette_var, state="readonly", width=16, font=FONT_NORMAL)
        self._update_palette_combo_list()
        self.palette_combo.pack(side="left", padx=(4, 12))
        self.palette_combo.bind("<<ComboboxSelected>>", self._on_palette_changed)

        self.history_btn = self._flat_button(row2, LANG[self.lang]["history"], self._toggle_history_panel, padx=10, pady=5)
        self.history_btn.pack(side="left")

        self.analyzer_btn = self._flat_button(row2, LANG[self.lang]["analyzer"], self._analyze_clipboard, padx=10, pady=5)
        self.analyzer_btn.pack(side="left", padx=(8, 0))

        self.options_btn = self._flat_button(row2, LANG[self.lang]["options"], self._show_options_menu, font=FONT_CHAR, padx=10, pady=2)
        self.options_btn.pack(side="left", padx=(8, 0))

        self.about_btn = self._flat_button(row2, LANG[self.lang]["about"], self._show_about, padx=12, pady=5)
        self.about_btn.pack(side="right")

        self.lang_btn = self._flat_button(row2, "PL" if self.lang == "en" else "EN", self._switch_language, font=FONT_BOLD, padx=12, pady=5, bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff")
        self.lang_btn.pack(side="right", padx=(8, 0))

        shortcuts_bar = tk.Frame(self, bg=BG, padx=16)
        shortcuts_bar.pack(fill="x")
        self.shortcuts_label = tk.Label(shortcuts_bar, text=LANG[self.lang]["shortcuts_hint"], bg=BG, font=FONT_TINY, fg=TEXT_SUBTLE, anchor="w")
        self.shortcuts_label.pack(side="left", pady=(4, 2))

        # Wizualna Klawiatura Glifów / Makra szybkiego dostępu (Quick Access Pad)
        macro_wrap = tk.Frame(self, bg=BG, padx=16)
        macro_wrap.pack(fill="x", side="bottom", pady=(0, 4))
        macro_pad = tk.Frame(macro_wrap, bg=PANEL_BG, padx=10, pady=6, highlightthickness=1, highlightbackground=BORDER)
        macro_pad.pack(fill="x")
        
        self.macro_title_label = tk.Label(macro_pad, text=LANG[self.lang]["quick_access"], bg=PANEL_BG, fg=TEXT_MUTED, font=FONT_SMALL)
        self.macro_title_label.pack(side="left", padx=(0, 10))
        
        self.macro_buttons = []
        for i in range(8):
            lbl_txt = self.macros[i] if self.macros[i] else "-"
            m_btn = tk.Button(macro_pad, text=lbl_txt, font=FONT_BOLD, width=3, bg=BG, fg=ACCENT, relief="flat", bd=0, cursor="hand2")
            m_btn.pack(side="left", padx=3)
            m_btn.config(command=lambda slot=i: self._use_macro(slot))
            _add_hover(m_btn, ACCENT_LIGHT, normal_bg=BG)
            self.macro_buttons.append(m_btn)

        # Dolny pasek informacyjny (Rozbudowany generator wielu formatów kodowania)
        info_wrap = tk.Frame(self, bg=BG)
        info_wrap.pack(fill="x", side="bottom", padx=16, pady=(0, 6))
        info = tk.Frame(info_wrap, bg=PANEL_BG, padx=14, pady=10, highlightthickness=1, highlightbackground=BORDER)
        info.pack(fill="x")

        self.preview_label = tk.Label(info, text="", font=FONT_PREVIEW, bg=ACCENT_LIGHT, fg=ACCENT, width=2, anchor="center", highlightthickness=1, highlightbackground=BORDER)
        self.preview_label.grid(row=0, column=0, rowspan=3, padx=(0, 14), sticky="ns")

        self.name_label = tk.Label(info, text=LANG[self.lang]["click_hint"], font=FONT_BOLD, bg=PANEL_BG, fg=TEXT, anchor="w")
        self.name_label.grid(row=0, column=1, columnspan=2, sticky="w")

        # Linie formatów kodowania
        self.code_line1 = tk.Entry(info, font=FONT_MONO, bg=PANEL_BG, fg=TEXT, relief="flat", bd=0, state="readonly")
        self.code_line1.grid(row=1, column=1, columnspan=2, sticky="ew", pady=(2, 0))
        self.code_line2 = tk.Entry(info, font=FONT_MONO, bg=PANEL_BG, fg=TEXT_MUTED, relief="flat", bd=0, state="readonly")
        self.code_line2.grid(row=2, column=1, columnspan=2, sticky="ew", pady=(1, 0))

        self.copy_btn = self._flat_button(info, LANG[self.lang]["copy_char"], self._copy_char, padx=12, pady=5, bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff", state="disabled")
        self.copy_btn.grid(row=0, column=3, rowspan=3, padx=(12, 0), sticky="e")

        self.copy_seq_btn = self._flat_button(info, LANG[self.lang]["copy_seq"], self._copy_seq, padx=12, pady=5, state="disabled")
        self.copy_seq_btn.grid(row=0, column=4, rowspan=3, padx=(6, 0), sticky="e")

        info.columnconfigure(1, weight=1)

        # Główna siatka znaków
        grid_frame = tk.Frame(self, bg=BG, padx=16)
        grid_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(grid_frame, bg=BG, highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(canvas, bg=BG)
        self.canvas_window = canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(self.canvas_window, width=e.width))

        def _on_mousewheel(event):
            if event.num == 4: canvas.yview_scroll(-1, "units")
            elif event.num == 5: canvas.yview_scroll(1, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")

        canvas.bind("<Enter>", lambda e: [canvas.bind_all("<MouseWheel>", _on_mousewheel), canvas.bind_all("<Button-4>", _on_mousewheel), canvas.bind_all("<Button-5>", _on_mousewheel)])
        canvas.bind("<Leave>", lambda e: [canvas.unbind_all("<MouseWheel>"), canvas.unbind_all("<Button-4>"), canvas.unbind_all("<Button-5>")])
        self.canvas = canvas

    def _bind_shortcuts(self):
        self.bind_all("<Control-c>", self._on_ctrl_c)
        self.bind_all("<Control-C>", self._on_ctrl_c)
        self.bind_all("<Control-f>", lambda e: [self.search_entry.focus_set(), self.search_entry.select_range(0, tk.END), "break"])
        self.bind_all("<Control-F>", lambda e: [self.search_entry.focus_set(), self.search_entry.select_range(0, tk.END), "break"])
        self.bind_all("<Escape>", self._on_escape)

    def _on_ctrl_c(self, event=None):
        focused = self.focus_get()
        if isinstance(focused, tk.Entry): return
        if self.selected_cp is not None: self._copy_char()
        return "break"

    def _on_escape(self, event=None):
        self.search_var.set("")
        self.filter_combo.current(0)
        self.focus_set()
        self._on_search()
        return "break"

    def _update_palette_combo_list(self):
        self.palette_combo.config(values=list(self.palettes.keys()))
        if self.current_palette_name in self.palettes:
            self.palette_var.set(self.current_palette_name)
        else:
            self.current_palette_name = "⭐ Ulubione"
            self.palette_var.set("⭐ Ulubione")

    def _current_category_chars(self):
        idx = self.cat_combo.current()
        if idx < 0: idx = 0
        _, start, end = CATEGORIES[idx]
        return get_chars(start, end)

    def _refresh_current_view(self):
        if self.view_mode == "favorites":
            self._render_grid(self.palettes.get(self.current_palette_name, []))
        elif self.view_mode == "history":
            self._render_grid(self.history)
        elif self.view_mode == "analyzer":
            self._render_grid(self.clipboard_chars)
        else:
            self._on_search()

    def _on_category(self, event=None):
        self._set_view_mode("category")

    def _on_palette_changed(self, event=None):
        self.current_palette_name = self.palette_var.get()
        self._set_view_mode("favorites")

    def _on_search(self, *args):
        q = self.search_var.get().strip().lower()
        filter_idx = self.filter_combo.current() # 0=All, 1=Upper, 2=Lower, 3=Numbers, 4=Punct, 5=Symbols

        if self.view_mode == "favorites":
            source = self.palettes.get(self.current_palette_name, [])
        elif self.view_mode == "history":
            source = self.history
        elif self.view_mode == "analyzer":
            source = self.clipboard_chars
        elif self.global_search_var.get() and (q or filter_idx > 0):
            source = get_all_chars()
        else:
            source = self._current_category_chars()

        filtered = []
        for cp in source:
            ch = chr(cp)
            
            # Filtrowanie zaawansowane po kategoriach Unicode
            if filter_idx > 0:
                ucat = unicodedata.category(ch)
                if filter_idx == 1 and not ucat.startswith("Lu"): continue
                elif filter_idx == 2 and not ucat.startswith("Ll"): continue
                elif filter_idx == 3 and not ucat.startswith("N"): continue
                elif filter_idx == 4 and not ucat.startswith("P"): continue
                elif filter_idx == 5 and not (ucat.startswith("S") or ucat.startswith("M")): continue

            if q:
                hex_code = f"u+{cp:04x}"
                name = char_name(cp, self.lang).lower()
                if q not in hex_code and q not in str(cp) and q not in ch.lower() and q not in name:
                    continue
                    
            filtered.append(cp)
            
        self._render_grid(filtered)

    def _render_grid(self, chars):
        for tip in self.tooltips: tip._hide()
        self.tooltips.clear()
        for btn in self.char_buttons: btn.destroy()
        self.char_buttons.clear()
        self.char_button_map = {}
        self.selected_cp = None

        if not chars:
            self.count_label.config(text=LANG[self.lang]["count_char"].format(0))
            empty_text = LANG[self.lang]["no_favorites"] if self.view_mode == "favorites" else (LANG[self.lang]["no_history"] if self.view_mode == "history" else (LANG[self.lang]["no_analyzer"] if self.view_mode == "analyzer" else None))
            if empty_text:
                placeholder = tk.Label(self.inner, text=empty_text, bg=BG, fg=TEXT_MUTED, font=FONT_NORMAL, justify="left")
                placeholder.grid(row=0, column=0, columnspan=COLS, sticky="w", pady=10, padx=4)
                self.char_buttons.append(placeholder)
            self.canvas.yview_moveto(0)
            return

        count_text = LANG[self.lang]["count_char"] if len(chars) == 1 else LANG[self.lang]["count_chars"]
        self.count_label.config(text=count_text.format(len(chars)))

        current_favs = self.palettes.get(self.current_palette_name, [])
        for i, cp in enumerate(chars):
            ch = chr(cp)
            is_fav = cp in current_favs
            rest_bg = CHAR_BTN_FAV if is_fav else CHAR_BTN_BG
            btn = tk.Button(self.inner, text=ch, font=FONT_CHAR, width=2, height=1, relief="flat", bd=0, bg=rest_bg, fg=TEXT, activebackground=CHAR_BTN_HOVER, activeforeground=TEXT, highlightthickness=1, highlightbackground=BORDER, highlightcolor=BORDER, cursor="hand2", command=lambda c=cp: self._select(c))
            _add_hover(btn, CHAR_BTN_FAV_HOVER if is_fav else CHAR_BTN_HOVER, normal_bg=rest_bg)
            btn.bind("<Button-3>", lambda e, c=cp: self._show_context_menu(e, c))
            btn.grid(row=i // COLS, column=i % COLS, padx=3, pady=3, sticky="nsew")
            self.char_buttons.append(btn)
            self.char_button_map[cp] = btn
            self.tooltips.append(ToolTip(btn, (lambda c=cp: f"{char_name(c, self.lang)}\nU+{c:04X}")))

        for col in range(COLS): self.inner.columnconfigure(col, weight=1, minsize=42)
        self.canvas.yview_moveto(0)

    def _select(self, cp):
        self.selected_cp = cp
        ch = chr(cp)
        name = char_name(cp, self.lang)
        
        # Obliczenie formatów kodowania (Multi-Format Code Generator)
        hex4 = f"U+{cp:04X}"
        html_ent = f"&#{cp};"
        py_esc = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
        js_esc = f"\\u{{{cp:0X}}}"
        css_esc = f"\\{cp:0X}"
        url_enc = urllib.parse.quote(ch)

        self.preview_label.config(text=ch)
        self.name_label.config(text=name)
        
        # Zapis do pól edycyjnych, by użytkownik mógł łatwo zaznaczyć i skopiować podsekcję
        self.code_line1.config(state="normal")
        self.code_line1.delete(0, tk.END)
        self.code_line1.insert(0, f"{hex4}   HTML: {html_ent}   Python: {py_esc}   JS: {js_esc}")
        self.code_line1.config(state="readonly")

        self.code_line2.config(state="normal")
        self.code_line2.delete(0, tk.END)
        self.code_line2.insert(0, f"CSS: {css_esc}   URL Encoded: {url_enc}   DEC: {cp}")
        self.code_line2.config(state="readonly")

        self.copy_btn.config(state="normal")
        self.copy_seq_btn.config(state="normal")

        current_favs = self.palettes.get(self.current_palette_name, [])
        for btn_cp, btn in self.char_button_map.items():
            rest_bg = CHAR_BTN_FAV if btn_cp in current_favs else CHAR_BTN_BG
            set_normal_bg(btn, rest_bg)
            btn.config(fg=TEXT)
        selected_btn = self.char_button_map.get(cp)
        if selected_btn is not None:
            selected_btn.config(bg=CHAR_BTN_SELECTED, fg=CHAR_BTN_SELECTED_FG)
            selected_btn._normal_bg = CHAR_BTN_SELECTED

    def _clear_selection(self):
        self.selected_cp = None
        self.preview_label.config(text="")
        self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.code_line1.config(state="normal")
        self.code_line1.delete(0, tk.END)
        self.code_line1.config(state="readonly")
        self.code_line2.config(state="normal")
        self.code_line2.delete(0, tk.END)
        self.code_line2.config(state="readonly")
        self.copy_btn.config(state="disabled")
        self.copy_seq_btn.config(state="disabled")

    def _copy_char(self):
        if self.selected_cp is not None:
            self.clipboard_clear()
            self.clipboard_append(chr(self.selected_cp))
            self._add_to_history(self.selected_cp)
            self._flash_btn()

    def _copy_seq(self):
        if self.selected_cp is not None:
            cp = self.selected_cp
            seq = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
            self.clipboard_clear()
            self.clipboard_append(seq)
            self._add_to_history(cp)
            self._flash_btn(seq=True)

    # Funkcja do wstawiania makra / szybkiego klonowania ze slotu
    def _use_macro(self, slot):
        char = self.macros[slot]
        if char:
            self.clipboard_clear()
            self.clipboard_append(char)
            self._add_to_history(ord(char))
            
            # mignięcie wizualne slotu
            orig_txt = self.macro_buttons[slot].cget("text")
            self.macro_buttons[slot].config(text=LANG[self.lang]["copied"], bg=SUCCESS_BG)
            self.after(800, lambda: self.macro_buttons[slot].config(text=orig_txt, bg=BG))

    def _assign_macro(self, slot, cp):
        self.macros[slot] = chr(cp)
        self.macro_buttons[slot].config(text=chr(cp))
        self._save_settings()

    # 1. Detektor i Inspekcja Znaków ze Schowka (Clipboard Analyzer)
    def _analyze_clipboard(self):
        try:
            text = self.clipboard_get()
            if text:
                # Wyciągnięcie unikalnych code pointów z odczytanego ciągu
                seen = {}
                self.clipboard_chars = []
                for c in text:
                    cp = ord(c)
                    if cp not in seen and unicodedata.category(c) not in ("Cc", "Cs", "Co"):
                        seen[cp] = True
                        self.clipboard_chars.append(cp)
            else:
                self.clipboard_chars = []
        except Exception:
            self.clipboard_chars = []
            
        self._set_view_mode("analyzer")

    # Obsługa zaawansowanych operacji na paletach
    def _toggle_favorite(self, cp):
        current_favs = self.palettes.get(self.current_palette_name, [])
        if cp in current_favs: current_favs.remove(cp)
        else: current_favs.append(cp)
        self._save_palettes()
        if self.view_mode == "favorites": self._refresh_current_view()
        elif cp in self.char_button_map:
            btn = self.char_button_map[cp]
            is_f = cp in current_favs
            rest_bg = CHAR_BTN_FAV if is_f else CHAR_BTN_BG
            if cp != self.selected_cp: set_normal_bg(btn, rest_bg)

    def _create_new_palette(self):
        name = simpledialog.askstring(LANG[self.lang]["palette_prompt_title"], LANG[self.lang]["palette_prompt_msg"], parent=self)
        if name and name.strip():
            name = name.strip()
            if name not in self.palettes:
                self.palettes[name] = []
                self._save_palettes()
                self._update_palette_combo_list()
            self.palette_var.set(name)
            self.current_palette_name = name
            self._set_view_mode("favorites")

    def _delete_current_palette(self):
        if self.current_palette_name == "⭐ Ulubione":
            return # Nie pozwól usunąć domyślnej palety
        if messagebox.askyesno(LANG[self.lang]["options"], f"Delete '{self.current_palette_name}'?"):
            del self.palettes[self.current_palette_name]
            self.current_palette_name = "⭐ Ulubione"
            self._save_palettes()
            self._update_palette_combo_list()
            self._set_view_mode("favorites")

    def _export_favorites(self):
        current_favs = self.palettes.get(self.current_palette_name, [])
        if not current_favs:
            messagebox.showinfo(LANG[self.lang]["export_title"], LANG[self.lang]["no_favorites"])
            return
        path = filedialog.asksaveasfilename(title=LANG[self.lang]["export_title"], defaultextension=".json", filetypes=[("JSON", "*.json"), ("Text", "*.txt")])
        if not path: return
        try:
            if path.lower().endswith(".json"):
                data = [{"cp": cp, "char": chr(cp), "name": char_name(cp, self.lang)} for cp in current_favs]
                with open(path, "w", encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
            else:
                with open(path, "w", encoding="utf-8") as f:
                    for cp in current_favs: f.write(f"{cp}\n")
            messagebox.showinfo(LANG[self.lang]["export_title"], LANG[self.lang]["export_success"].format(len(current_favs), path))
        except OSError as e:
            messagebox.showerror(LANG[self.lang]["export_title"], LANG[self.lang]["export_error"].format(e))

    def _import_favorites(self):
        path = filedialog.askopenfilename(title=LANG[self.lang]["import_title"], filetypes=[("JSON/Text", "*.json *.txt"), ("All files", "*.*")])
        if not path: return
        try:
            added = 0
            current_favs = self.palettes.get(self.current_palette_name, [])
            if path.lower().endswith(".json"):
                with open(path, "r", encoding="utf-8") as f: data = json.load(f)
                for item in data:
                    cp = item["cp"] if isinstance(item, dict) else int(item)
                    if cp not in current_favs:
                        current_favs.append(cp)
                        added += 1
            else:
                with open(path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line:
                            try: cp = int(line)
                            except ValueError: continue
                            if cp not in current_favs:
                                current_favs.append(cp)
                                added += 1
            self._save_palettes()
            if self.view_mode == "favorites": self._refresh_current_view()
            messagebox.showinfo(LANG[self.lang]["import_title"], LANG[self.lang]["import_success"].format(added))
        except Exception as e:
            messagebox.showerror(LANG[self.lang]["import_title"], LANG[self.lang]["import_error"].format(e))

    def _load_history(self):
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if line: self.history.append(int(line))
            except Exception: pass

    def _save_history(self):
        try:
            with open(self.history_file, "w", encoding="utf-8") as f:
                for cp in self.history: f.write(f"{cp}\n")
        except OSError: pass

    def _add_to_history(self, cp):
        if cp in self.history: self.history.remove(cp)
        self.history.insert(0, cp)
        del self.history[HISTORY_MAX:]
        self._save_history()
        if self.view_mode == "history": self._refresh_current_view()

    def _toggle_favorites_panel(self):
        self._set_view_mode("category" if self.view_mode == "favorites" else "favorites")

    def _toggle_history_panel(self):
        self._set_view_mode("category" if self.view_mode == "history" else "history")

    def _set_view_mode(self, mode):
        self.view_mode = mode
        if mode == "favorites":
            set_normal_bg(self.fav_btn, BTN_ACTIVE_BG)
            set_normal_bg(self.history_btn, BTN_BG)
            set_normal_bg(self.analyzer_btn, BTN_BG)
            self.cat_combo.config(state="disabled")
        elif mode == "history":
            set_normal_bg(self.fav_btn, BTN_BG)
            set_normal_bg(self.history_btn, BTN_ACTIVE_BG)
            set_normal_bg(self.analyzer_btn, BTN_BG)
            self.cat_combo.config(state="disabled")
        elif mode == "analyzer":
            set_normal_bg(self.fav_btn, BTN_BG)
            set_normal_bg(self.history_btn, BTN_BG)
            set_normal_bg(self.analyzer_btn, BTN_ACTIVE_BG)
            self.cat_combo.config(state="disabled")
        else:
            set_normal_bg(self.fav_btn, BTN_BG)
            set_normal_bg(self.history_btn, BTN_BG)
            set_normal_bg(self.analyzer_btn, BTN_BG)
            self.cat_combo.config(state="readonly")
        self._clear_selection()
        self._on_search()

    def _show_options_menu(self):
        menu = tk.Menu(self, tearoff=0, bg=PANEL_BG, fg=TEXT, activebackground=ACCENT_LIGHT, activeforeground=TEXT, bd=0, relief="flat", font=FONT_NORMAL)
        menu.add_command(label=LANG[self.lang]["new_palette"], command=self._create_new_palette)
        menu.add_command(label=LANG[self.lang]["export_fav"], command=self._export_favorites)
        menu.add_command(label=LANG[self.lang]["import_fav"], command=self._import_favorites)
        if self.current_palette_name != "⭐ Ulubione":
            menu.add_command(label=LANG[self.lang]["delete_palette"], command=self._delete_current_palette)
        menu.add_separator()
        menu.add_command(label=LANG[self.lang]["clear_history"], command=lambda: [self.history.clear(), self._save_history(), self._refresh_current_view()])
        x = self.options_btn.winfo_rootx()
        y = self.options_btn.winfo_rooty() + self.options_btn.winfo_height()
        menu.post(x, y)

    def _show_context_menu(self, event, cp):
        menu = tk.Menu(self, tearoff=0, bg=PANEL_BG, fg=TEXT, activebackground=ACCENT_LIGHT, activeforeground=TEXT, bd=0, relief="flat", font=FONT_NORMAL)
        current_favs = self.palettes.get(self.current_palette_name, [])
        lbl = LANG[self.lang]["remove_from_fav"] if cp in current_favs else LANG[self.lang]["add_to_fav"]
        menu.add_command(label=lbl, command=lambda: self._toggle_favorite(cp))
        
        # Podmenu do przypisywania Szybkich Slotów (Macro Pad)
        macro_menu = tk.Menu(menu, tearoff=0, bg=PANEL_BG, fg=TEXT, activebackground=ACCENT_LIGHT, activeforeground=TEXT, bd=0, relief="flat", font=FONT_NORMAL)
        for slot in range(8):
            macro_menu.add_command(label=LANG[self.lang]["add_to_macro"].format(slot + 1), command=lambda s=slot: self._assign_macro(s, cp))
        menu.add_cascade(label=LANG[self.lang]["quick_access"], menu=macro_menu)
        
        menu.post(event.x_root, event.y_root)

    def _show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title(LANG[self.lang]["about_title"])
        about_window.resizable(False, False)
        about_window.configure(bg=PANEL_BG)
        window_width, window_height = 380, 260
        screen_width = about_window.winfo_screenwidth()
        screen_height = about_window.winfo_screenheight()
        about_window.geometry(f"{window_width}x{window_height}+{int(screen_width/2 - window_width/2)}+{int(screen_height/2 - window_height/2)}")
        about_window.transient(self)
        about_window.grab_set()

        tk.Frame(about_window, bg=ACCENT, height=4).pack(fill="x", side="top")
        frame = tk.Frame(about_window, bg=PANEL_BG, padx=20, pady=15)
        frame.pack(fill="both", expand=True)

        tk.Label(frame, text=LANG[self.lang]["program_name"], font=FONT_TITLE, bg=PANEL_BG, fg=TEXT).pack(anchor="w")
        tk.Label(frame, text=f"{LANG[self.lang]['version']} {APP_VERSION}", font=FONT_SMALL, bg=PANEL_BG, fg=TEXT_MUTED).pack(anchor="w", pady=(2, 8))
        tk.Label(frame, text=f"{LANG[self.lang]['author']} Sebastian Januchowski", font=FONT_NORMAL, bg=PANEL_BG, fg=TEXT).pack(anchor="w", pady=2)
        tk.Label(frame, text=f"{LANG[self.lang]['mail']} polsoft.its@mail.com", font=FONT_NORMAL, bg=PANEL_BG, fg=ACCENT).pack(anchor="w", pady=2)
        tk.Label(frame, text=f"{LANG[self.lang]['github']} polsoft.ITS™", font=FONT_NORMAL, bg=PANEL_BG, fg=ACCENT).pack(anchor="w", pady=2)

        self._flat_button(frame, "OK", about_window.destroy, font=FONT_SMALL, padx=20, pady=4, bg=ACCENT, hover=ACCENT_HOVER, fg="#ffffff").pack(pady=(15, 0))

    def _flash_btn(self, seq=False):
        btn = self.copy_seq_btn if seq else self.copy_btn
        orig = btn.cget("text")
        orig_bg = ACCENT if not seq else BTN_BG
        btn.config(text=LANG[self.lang]["copied"], bg=SUCCESS_BG, fg=SUCCESS_TEXT)
        btn._normal_bg = SUCCESS_BG
        self.after(1200, lambda: [btn.config(text=orig, bg=orig_bg, fg="#ffffff" if not seq else TEXT), setattr(btn, "_normal_bg", orig_bg)])

if __name__ == "__main__":
    app = TablicaZnakow()
    app.mainloop()