#!/usr/bin/env python3
"""
Tablica Znaków Unicode
Alternatywa dla windowsowskiego charmap.exe
Wymaga tylko Python 3 (wbudowany tkinter)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import unicodedata
import os
import sys

LANG = {
    "en": {
        "title": "Simple Character Table",
        "category": "Category:",
        "search": "Search:",
        "count_chars": "{} characters",
        "count_char": "{} character",
        "no_name": "(no name)",
        "click_hint": "Click a character to see details",
        "copy_char": "📋  Copy character",
        "copy_seq": "Copy sequence",
        "copied": "✓ Copied!",
        "favorites": "⭐ Favorites",
        "add_to_fav": "Add to favorites",
        "remove_from_fav": "Remove from favorites",
        "about": "About",
        "about_title": "About Simple Character Table",
        "program_name": "Simple Character Table",
        "author": "Author:",
        "mail": "Mail:",
        "github": "GitHub:",
        "categories": [
            "Basic Latin",
            "Latin Extended",
            "IPA Phonetic Alphabet",
            "Greek and Coptic",
            "Cyrillic",
            "Hebrew",
            "Arabic",
            "Currency",
            "Letterlike Symbols",
            "Punctuation",
            "Arrows",
            "Mathematical",
            "Misc Technical",
            "Geometric Shapes",
            "Misc Symbols",
            "Dingbats",
            "Emoji (Basic)",
            "Emoji (Transport)",
            "Emoji (Faces/Gestures)",
            "Mahjong and Cards"
        ]
    },
    "pl": {
        "title": "Simple Character Table",
        "category": "Kategoria:",
        "search": "Szukaj:",
        "count_chars": "{} znaków",
        "count_char": "{} znak",
        "no_name": "(brak nazwy)",
        "click_hint": "Kliknij znak, aby zobaczyć szczegóły",
        "copy_char": "📋  Kopiuj znak",
        "copy_seq": "Kopiuj sekwencję",
        "copied": "✓ Skopiowano!",
        "favorites": "⭐ Ulubione",
        "add_to_fav": "Dodaj do ulubionych",
        "remove_from_fav": "Usuń z ulubionych",
        "about": "O programie",
        "about_title": "O programie Simple Character Table",
        "program_name": "Simple Character Table",
        "author": "Autor:",
        "mail": "Mail:",
        "github": "GitHub:",
        "categories": [
            "Łacińskie podstawowe",
            "Łacińskie rozszerzone",
            "Alfabet fonetyczny (IPA)",
            "Grecki i koptyjski",
            "Cyrylica",
            "Hebrajski",
            "Arabski",
            "Waluty",
            "Literopodobne symbole",
            "Znaki interpunkcji",
            "Strzałki",
            "Matematyczne",
            "Różne techniczne",
            "Geometryczne kształty",
            "Różne symbole",
            "Dingbats",
            "Emoji (podstawowe)",
            "Emoji (transport)",
            "Emoji (twarze/gesty)",
            "Mahjong i karty"
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


def get_chars(start, end):
    result = []
    for cp in range(start, end + 1):
        try:
            ch = chr(cp)
            cat = unicodedata.category(ch)
            # pomiń znaki kontrolne i surrogaty
            if cat not in ("Cc", "Cs", "Co"):
                result.append(cp)
        except (ValueError, OverflowError):
            pass
    return result


def char_name(cp, lang="en"):
    try:
        return unicodedata.name(chr(cp))
    except ValueError:
        return LANG[lang]["no_name"]


def get_resource_path(filename):
    if getattr(sys, "frozen", False) and hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.dirname(__file__), filename)


class TablicaZnakow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.title(LANG[self.lang]["title"])

        ico_path = get_resource_path("tz-ico.ico")
        png_path = get_resource_path("tz-png.png")

        if os.path.exists(ico_path):
            try:
                self.iconbitmap(ico_path)
            except tk.TclError:
                pass
        elif os.path.exists(png_path):
            try:
                self.icon_img = tk.PhotoImage(file=png_path)
                self.iconphoto(True, self.icon_img)
            except tk.TclError:
                pass

        # Set window size and center it
        window_width = 900
        window_height = 650
        self.minsize(750, 500)
        self.configure(bg="#f0f0f0")
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        self.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        self.selected_cp = None
        self.char_buttons = []
        self.current_chars = []
        self.favorites = []
        self.favorites_file = os.path.join(os.path.dirname(__file__), "ulubione.txt")
        self.show_favorites = False

        self._load_favorites()
        self._build_ui()
        self._load_category(0)

    # ── UI ────────────────────────────────────────────────────────────────────

    def _show_about(self):
        about_window = tk.Toplevel(self)
        about_window.title(LANG[self.lang]["about_title"])
        about_window.resizable(False, False)
        about_window.configure(bg="#f0f0f0")

        # Set window size and center it
        window_width = 340
        window_height = 240
        screen_width = about_window.winfo_screenwidth()
        screen_height = about_window.winfo_screenheight()
        center_x = int(screen_width/2 - window_width/2)
        center_y = int(screen_height/2 - window_height/2)
        about_window.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")

        # Make it transient and grab focus
        about_window.transient(self)
        about_window.grab_set()

        frame = tk.Frame(about_window, bg="#f0f0f0", padx=16, pady=16)
        frame.pack(fill="both", expand=True)

        header_frame = tk.Frame(frame, bg="#f0f0f0")
        header_frame.pack(fill="x", pady=(0, 8))

        # Load and display a smaller icon
        try:
            png_path = get_resource_path("tz-png.png")
            if os.path.exists(png_path):
                icon_img = tk.PhotoImage(file=png_path)
                about_window.icon_photo = icon_img.subsample(6, 6)
                icon_label = tk.Label(header_frame, image=about_window.icon_photo, bg="#f0f0f0")
                icon_label.pack(side="left", padx=(0, 10))
        except Exception:
            pass

        # Program name label
        program_label = tk.Label(header_frame, text=LANG[self.lang]["program_name"],
                                 font=("Segoe UI", 12, "bold"), bg="#f0f0f0", anchor="w")
        program_label.pack(side="left", fill="x")

        author_label = tk.Label(frame, text=f"{LANG[self.lang]['author']} Sebastian Januchowski",
                                font=("Segoe UI", 10), bg="#f0f0f0", anchor="w")
        author_label.pack(fill="x", pady=2)

        mail_label = tk.Label(frame, text=f"{LANG[self.lang]['mail']} polsoft.its@mail.com",
                              font=("Segoe UI", 10), bg="#f0f0f0", anchor="w", fg="#0d6efd", cursor="hand2")
        mail_label.pack(fill="x", pady=2)
        mail_label.bind("<Button-1>", lambda e: self._open_url("mailto:polsoft.its@mail.com"))

        github_label = tk.Label(frame, text=f"{LANG[self.lang]['github']} polsoft.ITS™",
                                font=("Segoe UI", 10), bg="#f0f0f0", anchor="w", fg="#0d6efd", cursor="hand2")
        github_label.pack(fill="x", pady=2)
        github_label.bind("<Button-1>", lambda e: self._open_url("https://github.com/polsoft-IT"))

        ok_btn = tk.Button(frame, text="OK", font=("Segoe UI", 9),
                          command=about_window.destroy,
                          bg="#ffffff", relief="raised", bd=2, padx=14, pady=3)
        ok_btn.pack(pady=(12, 4))

    def _open_url(self, url):
        import webbrowser
        webbrowser.open(url)

    def _switch_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        self.title(LANG[self.lang]["title"])
        # Update UI text
        self._update_ui_text()
        if self.show_favorites:
            self._render_grid(self.favorites)
        else:
            self._load_category(self.cat_combo.current())

    def _update_ui_text(self):
        # Update labels and buttons
        self.cat_label.config(text=LANG[self.lang]["category"])
        self.search_label.config(text=LANG[self.lang]["search"])
        self.fav_btn.config(text=LANG[self.lang]["favorites"])
        self.lang_btn.config(text="PL" if self.lang == "en" else "EN")
        self.about_btn.config(text=LANG[self.lang]["about"])
        if self.selected_cp is None:
            self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.copy_btn.config(text=LANG[self.lang]["copy_char"])
        self.copy_seq_btn.config(text=LANG[self.lang]["copy_seq"])
        # Update category combobox
        current_idx = self.cat_combo.current()
        self.cat_combo.config(values=LANG[self.lang]["categories"])
        self.cat_combo.current(current_idx)

    def _build_ui(self):
        # ── pasek górny ──
        top = tk.Frame(self, bg="#f0f0f0", pady=10, padx=15)
        top.pack(fill="x")

        self.cat_label = tk.Label(top, text=LANG[self.lang]["category"], bg="#f0f0f0", font=("Segoe UI", 10))
        self.cat_label.pack(side="left")
        self.cat_var = tk.StringVar()
        self.cat_combo = ttk.Combobox(
            top, textvariable=self.cat_var,
            values=LANG[self.lang]["categories"],
            state="readonly", width=28, font=("Segoe UI", 10)
        )
        self.cat_combo.current(0)
        self.cat_combo.pack(side="left", padx=(5, 18))
        self.cat_combo.bind("<<ComboboxSelected>>", self._on_category)

        self.search_label = tk.Label(top, text=LANG[self.lang]["search"], bg="#f0f0f0", font=("Segoe UI", 10))
        self.search_label.pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._on_search)
        search_entry = tk.Entry(top, textvariable=self.search_var,
                                font=("Segoe UI", 10), width=22, relief="groove", bd=2)
        search_entry.pack(side="left", padx=(5, 0))

        self.fav_btn = tk.Button(top, text=LANG[self.lang]["favorites"], font=("Segoe UI", 10),
                                 command=self._toggle_favorites_panel,
                                 bg="#ffffff", relief="raised", bd=2, padx=12)
        self.fav_btn.pack(side="left", padx=(18, 0))

        self.lang_btn = tk.Button(top, text="PL", font=("Segoe UI", 10),
                                  command=self._switch_language,
                                  bg="#ffffff", relief="raised", bd=2, padx=12)
        self.lang_btn.pack(side="left", padx=(8, 0))

        self.about_btn = tk.Button(top, text=LANG[self.lang]["about"], font=("Segoe UI", 10),
                                   command=self._show_about,
                                   bg="#ffffff", relief="raised", bd=2, padx=12)
        self.about_btn.pack(side="left", padx=(8, 0))

        self.count_label = tk.Label(top, text="", bg="#f0f0f0",
                                    font=("Segoe UI", 9), fg="#777")
        self.count_label.pack(side="right")

        # ── siatka znaków ──
        grid_frame = tk.Frame(self, bg="#f0f0f0", padx=15)
        grid_frame.pack(fill="both", expand=True)

        canvas = tk.Canvas(grid_frame, bg="#f0f0f0", highlightthickness=0)
        scrollbar = ttk.Scrollbar(grid_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)

        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        self.inner = tk.Frame(canvas, bg="#f0f0f0")
        self.canvas_window = canvas.create_window((0, 0), window=self.inner, anchor="nw")

        self.inner.bind("<Configure>",
                        lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.bind("<Configure>",
                    lambda e: canvas.itemconfig(self.canvas_window, width=e.width))
        canvas.bind_all("<MouseWheel>",
                        lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units"))

        self.canvas = canvas

        # ── pasek informacji ──
        info = tk.Frame(self, bg="#e6e6e6", padx=15, pady=10,
                        relief="flat", bd=0)
        info.pack(fill="x", side="bottom")

        self.preview_label = tk.Label(
            info, text="", font=("Segoe UI", 32), bg="#e6e6e6",
            width=2, anchor="center", relief="sunken", bd=2
        )
        self.preview_label.grid(row=0, column=0, rowspan=2, padx=(0, 15), sticky="ns")

        self.name_label = tk.Label(
            info, text=LANG[self.lang]["click_hint"],
            font=("Segoe UI", 11, "bold"), bg="#e6e6e6", anchor="w"
        )
        self.name_label.grid(row=0, column=1, sticky="w")

        self.code_label = tk.Label(
            info, text="", font=("Consolas", 10), bg="#e6e6e6",
            fg="#444", anchor="w"
        )
        self.code_label.grid(row=1, column=1, sticky="w")

        self.copy_btn = tk.Button(
            info, text=LANG[self.lang]["copy_char"], font=("Segoe UI", 10),
            command=self._copy_char, state="disabled",
            bg="#ffffff", relief="raised", bd=2, padx=12
        )
        self.copy_btn.grid(row=0, column=2, rowspan=2, padx=(18, 0), sticky="e")

        self.copy_seq_btn = tk.Button(
            info, text=LANG[self.lang]["copy_seq"], font=("Segoe UI", 10),
            command=self._copy_seq, state="disabled",
            bg="#ffffff", relief="raised", bd=2, padx=10
        )
        self.copy_seq_btn.grid(row=0, column=3, rowspan=2, padx=(8, 0), sticky="e")

        info.columnconfigure(1, weight=1)

    # ── logika ───────────────────────────────────────────────────────────────

    def _load_category(self, idx):
        _, start, end = CATEGORIES[idx]
        self.current_chars = get_chars(start, end)
        self._render_grid(self.current_chars)

    def _on_category(self, event=None):
        idx = self.cat_combo.current()
        self.search_var.set("")
        self._load_category(idx)
        self._clear_selection()

    def _on_search(self, *args):
        q = self.search_var.get().strip().lower()
        
        if self.show_favorites:
            if not q:
                self._render_grid(self.favorites)
                return
            filtered = []
            for cp in self.favorites:
                ch = chr(cp)
                hex_code = f"u+{cp:04x}"
                name = char_name(cp, self.lang).lower()
                if (q in hex_code or q in str(cp) or q in ch.lower() or q in name):
                    filtered.append(cp)
            self._render_grid(filtered)
        else:
            idx = self.cat_combo.current()
            _, start, end = CATEGORIES[idx]
            all_chars = get_chars(start, end)

            if not q:
                self._render_grid(all_chars)
                return

            filtered = []
            for cp in all_chars:
                ch = chr(cp)
                hex_code = f"u+{cp:04x}"
                name = char_name(cp, self.lang).lower()
                if (q in hex_code or q in str(cp) or q in ch.lower() or q in name):
                    filtered.append(cp)
            self._render_grid(filtered)

    def _render_grid(self, chars):
        for btn in self.char_buttons:
            btn.destroy()
        self.char_buttons.clear()
        self.selected_cp = None

        count_text = LANG[self.lang]["count_char"] if len(chars) == 1 else LANG[self.lang]["count_chars"]
        self.count_label.config(text=count_text.format(len(chars)))

        for i, cp in enumerate(chars):
            ch = chr(cp)
            btn = tk.Button(
                self.inner,
                text=ch,
                font=("Segoe UI", 14),
                width=2, height=1,
                relief="raised", bd=2,
                bg="#fff3cd" if cp in self.favorites else "#ffffff",
                activebackground="#cfe2ff",
                cursor="hand2",
                command=lambda c=cp: self._select(c)
            )
            btn.bind("<Button-3>", lambda e, c=cp: self._show_context_menu(e, c))
            btn.grid(row=i // COLS, column=i % COLS, padx=3, pady=3, sticky="nsew")
            self.char_buttons.append(btn)

        for col in range(COLS):
            self.inner.columnconfigure(col, weight=1, minsize=42)

        self.canvas.yview_moveto(0)

    def _select(self, cp):
        self.selected_cp = cp
        ch = chr(cp)
        name = char_name(cp, self.lang)
        hex4 = f"U+{cp:04X}"
        html_ent = f"&#{cp};"
        py_esc = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"

        self.preview_label.config(text=ch)
        self.name_label.config(text=name)
        self.code_label.config(
            text=f"{hex4}   HTML: {html_ent}   Python: {py_esc}   Dziesiętnie: {cp}"
        )
        self.copy_btn.config(state="normal")
        self.copy_seq_btn.config(state="normal")

        # podświetl wybrany przycisk
        for btn in self.char_buttons:
            btn_cp = None
            # Find the code point for this button (we can check current_chars or favorites)
            all_chars = self.favorites if self.show_favorites else self.current_chars
            for cp in all_chars:
                if chr(cp) == btn.cget("text"):
                    btn_cp = cp
                    break
            if btn_cp is not None:
                btn.config(bg="#fff3cd" if btn_cp in self.favorites else "#ffffff")
        for btn in self.char_buttons:
            if btn.cget("text") == ch:
                btn.config(bg="#cfe2ff")
                break

    def _clear_selection(self):
        self.selected_cp = None
        self.preview_label.config(text="")
        self.name_label.config(text=LANG[self.lang]["click_hint"])
        self.code_label.config(text="")
        self.copy_btn.config(state="disabled")
        self.copy_seq_btn.config(state="disabled")

    def _copy_char(self):
        if self.selected_cp is not None:
            self.clipboard_clear()
            self.clipboard_append(chr(self.selected_cp))
            self._flash_btn()

    def _copy_seq(self):
        if self.selected_cp is not None:
            cp = self.selected_cp
            seq = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
            self.clipboard_clear()
            self.clipboard_append(seq)
            self._flash_btn(seq=True)

    def _load_favorites(self):
        if os.path.exists(self.favorites_file):
            with open(self.favorites_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            self.favorites.append(int(line))
                        except ValueError:
                            pass

    def _save_favorites(self):
        with open(self.favorites_file, "w", encoding="utf-8") as f:
            for cp in self.favorites:
                f.write(f"{cp}\n")

    def _toggle_favorite(self, cp):
        if cp in self.favorites:
            self.favorites.remove(cp)
        else:
            self.favorites.append(cp)
        self._save_favorites()
        if self.show_favorites:
            self._render_grid(self.favorites)

    def _toggle_favorites_panel(self):
        self.show_favorites = not self.show_favorites
        self.search_var.set("")
        if self.show_favorites:
            self.fav_btn.config(bg="#fff3cd")
            self.cat_combo.config(state="disabled")
            self._render_grid(self.favorites)
        else:
            self.fav_btn.config(bg="#ffffff")
            self.cat_combo.config(state="readonly")
            self._load_category(self.cat_combo.current())

    def _show_context_menu(self, event, cp):
        menu = tk.Menu(self, tearoff=0)
        if cp in self.favorites:
            menu.add_command(label=LANG[self.lang]["remove_from_fav"], command=lambda: self._toggle_favorite(cp))
        else:
            menu.add_command(label=LANG[self.lang]["add_to_fav"], command=lambda: self._toggle_favorite(cp))
        menu.post(event.x_root, event.y_root)

    def _flash_btn(self, seq=False):
        btn = self.copy_seq_btn if seq else self.copy_btn
        orig = btn.cget("text")
        btn.config(text=LANG[self.lang]["copied"], bg="#d4edda")
        self.after(1200, lambda: btn.config(text=orig, bg="#ffffff"))


if __name__ == "__main__":
    app = TablicaZnakow()
    app.mainloop()
