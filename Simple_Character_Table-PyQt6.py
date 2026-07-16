#!/usr/bin/env python3
"""
Tablica Znaków Unicode
Alternatywa dla windowsowskiego charmap.exe w PyQt6
"""

import sys
import os
import unicodedata
import webbrowser
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QIcon, QFont, QCursor
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QLineEdit, QPushButton, QScrollArea, QGridLayout,
    QMessageBox, QDialog, QMenu
)

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


class AboutDialog(QDialog):
    def __init__(self, parent, lang):
        super().__init__(parent)
        self.lang = lang
        self.setWindowTitle(LANG[self.lang]["about_title"])
        self.setFixedSize(360, 240)
        self.setStyleSheet("""
            QDialog { background-color: #f8f9fa; }
            QLabel { font-family: 'Segoe UI', Arial; color: #212529; }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #ced4da;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 60px;
            }
            QPushButton:hover { background-color: #e9ecef; }
        """)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QHBoxLayout()
        icon_label = QLabel()
        png_path = get_resource_path("tz-png.png")
        if os.path.exists(png_path):
            icon_label.setPixmap(QIcon(png_path).pixmap(32, 32))
            header_layout.addWidget(icon_label)

        title_label = QLabel(LANG[self.lang]["program_name"])
        title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        layout.addLayout(header_layout)

        author_label = QLabel(f"{LANG[self.lang]['author']} Sebastian Januchowski")
        author_label.setStyleSheet("font-size: 11px;")
        layout.addWidget(author_label)

        mail_label = QLabel(f"{LANG[self.lang]['mail']} <a href='mailto:polsoft.its@mail.com' style='color: #0d6efd; text-decoration: none;'>polsoft.its@mail.com</a>")
        mail_label.setStyleSheet("font-size: 11px;")
        mail_label.setOpenExternalLinks(True)
        layout.addWidget(mail_label)

        github_label = QLabel(f"{LANG[self.lang]['github']} <a href='https://github.com/polsoft-IT' style='color: #0d6efd; text-decoration: none;'>polsoft.ITS™</a>")
        github_label.setStyleSheet("font-size: 11px;")
        github_label.setOpenExternalLinks(True)
        layout.addWidget(github_label)

        layout.addStretch()

        ok_btn = QPushButton("OK")
        ok_btn.clicked.connect(self.accept)
        layout.addWidget(ok_btn, alignment=Qt.AlignmentFlag.AlignCenter)


class TablicaZnakow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "en"
        self.selected_cp = None
        self.current_chars = []
        self.favorites = []
        self.favorites_file = os.path.join(os.path.dirname(__file__), "ulubione.txt")
        self.show_favorites = False
        self.buttons_map = {}  # cp -> QPushButton

        self._load_favorites()
        self._init_window()
        self._build_ui()
        self._load_category(0)

    def _init_window(self):
        self.setWindowTitle(LANG[self.lang]["title"])
        self.resize(950, 650)
        self.setMinimumSize(780, 500)

        # Ustawienie ikony aplikacji
        ico_path = get_resource_path("tz-ico.ico")
        png_path = get_resource_path("tz-png.png")
        if os.path.exists(ico_path):
            self.setWindowIcon(QIcon(ico_path))
        elif os.path.exists(png_path):
            self.setWindowIcon(QIcon(png_path))

        # Stylizacja stylesheet całej aplikacji
        self.setStyleSheet("""
            QMainWindow { background-color: #f3f4f6; }
            QWidget { font-family: 'Segoe UI', Helvetica, Arial; }
            QLabel { color: #374151; }
            QPushButton {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 6px 12px;
                font-size: 12px;
                color: #374151;
            }
            QPushButton:hover {
                background-color: #f9fafb;
                border-color: #9ca3af;
            }
            QPushButton:pressed {
                background-color: #f3f4f6;
            }
            QComboBox {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 12px;
                min-width: 180px;
            }
            QLineEdit {
                background-color: #ffffff;
                border: 1px solid #d1d5db;
                border-radius: 6px;
                padding: 4px 10px;
                font-size: 12px;
            }
        """)

    def _build_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)

        # --- Pasek Górny ---
        top_bar = QHBoxLayout()
        top_bar.setSpacing(10)

        self.cat_label = QLabel(LANG[self.lang]["category"])
        top_bar.addWidget(self.cat_label)

        self.cat_combo = QComboBox()
        self.cat_combo.addItems(LANG[self.lang]["categories"])
        self.cat_combo.currentIndexChanged.connect(self._on_category)
        top_bar.addWidget(self.cat_combo)

        self.search_label = QLabel(LANG[self.lang]["search"])
        top_bar.addWidget(self.search_label)

        self.search_entry = QLineEdit()
        self.search_entry.textChanged.connect(self._on_search)
        top_bar.addWidget(self.search_entry)

        self.fav_btn = QPushButton(LANG[self.lang]["favorites"])
        self.fav_btn.clicked.connect(self._toggle_favorites_panel)
        top_bar.addWidget(self.fav_btn)

        self.lang_btn = QPushButton("PL" if self.lang == "en" else "EN")
        self.lang_btn.clicked.connect(self._switch_language)
        top_bar.addWidget(self.lang_btn)

        self.about_btn = QPushButton(LANG[self.lang]["about"])
        self.about_btn.clicked.connect(self._show_about)
        top_bar.addWidget(self.about_btn)

        top_bar.addStretch()

        self.count_label = QLabel("")
        self.count_label.setStyleSheet("color: #6b7280; font-size: 11px;")
        top_bar.addWidget(self.count_label)

        main_layout.addLayout(top_bar)

        # --- Grid Znaków w ScrollArea ---
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #ffffff;
                border: 1px solid #e5e7eb;
                border-radius: 8px;
            }
        """)

        self.grid_widget = QWidget()
        self.grid_widget.setObjectName("GridWidget")
        self.grid_widget.setStyleSheet("#GridWidget { background-color: #ffffff; }")
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(4)
        self.grid_layout.setContentsMargins(10, 10, 10, 10)

        self.scroll_area.setWidget(self.grid_widget)
        main_layout.addWidget(self.scroll_area)

        # --- Pasek Informacyjny ---
        info_panel = QWidget()
        info_panel.setStyleSheet("""
            QWidget {
                background-color: #f9fafb;
                border-top: 1px solid #e5e7eb;
            }
        """)
        info_layout = QHBoxLayout(info_panel)
        info_layout.setContentsMargins(10, 15, 10, 10)

        # Podgląd dużego znaku
        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedSize(70, 70)
        self.preview_label.setFont(QFont("Segoe UI", 28))
        self.preview_label.setStyleSheet("""
            background-color: #ffffff;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
        """)
        info_layout.addWidget(self.preview_label)

        # Tekstowe opisy
        text_info_layout = QVBoxLayout()
        text_info_layout.setSpacing(4)
        self.name_label = QLabel(LANG[self.lang]["click_hint"])
        self.name_label.setStyleSheet("font-size: 13px; font-weight: bold; color: #111827;")
        self.code_label = QLabel("")
        self.code_label.setStyleSheet("font-family: 'Consolas', monospace; font-size: 11px; color: #4b5563;")
        text_info_layout.addWidget(self.name_label)
        text_info_layout.addWidget(self.code_label)
        info_layout.addLayout(text_info_layout)

        info_layout.addStretch()

        # Przyciski kopiowania
        self.copy_btn = QPushButton(LANG[self.lang]["copy_char"])
        self.copy_btn.setEnabled(False)
        self.copy_btn.clicked.connect(self._copy_char)
        info_layout.addWidget(self.copy_btn)

        self.copy_seq_btn = QPushButton(LANG[self.lang]["copy_seq"])
        self.copy_seq_btn.setEnabled(False)
        self.copy_seq_btn.clicked.connect(self._copy_seq)
        info_layout.addWidget(self.copy_seq_btn)

        main_layout.addWidget(info_panel)

    # --- Logika Funkcjonalna ---

    def _show_about(self):
        dialog = AboutDialog(self, self.lang)
        dialog.exec()

    def _switch_language(self):
        self.lang = "pl" if self.lang == "en" else "en"
        self.setWindowTitle(LANG[self.lang]["title"])
        self._update_ui_text()
        if self.show_favorites:
            self._render_grid(self.favorites)
        else:
            self._load_category(self.cat_combo.currentIndex())

    def _update_ui_text(self):
        self.cat_label.setText(LANG[self.lang]["category"])
        self.search_label.setText(LANG[self.lang]["search"])
        self.fav_btn.setText(LANG[self.lang]["favorites"])
        self.lang_btn.setText("PL" if self.lang == "en" else "EN")
        self.about_btn.setText(LANG[self.lang]["about"])
        if self.selected_cp is None:
            self.name_label.setText(LANG[self.lang]["click_hint"])
        self.copy_btn.setText(LANG[self.lang]["copy_char"])
        self.copy_seq_btn.setText(LANG[self.lang]["copy_seq"])

        # Update combobox categories without triggering changes
        self.cat_combo.blockSignals(True)
        curr_idx = self.cat_combo.currentIndex()
        self.cat_combo.clear()
        self.cat_combo.addItems(LANG[self.lang]["categories"])
        self.cat_combo.setCurrentIndex(curr_idx)
        self.cat_combo.blockSignals(False)

    def _load_category(self, idx):
        if idx < 0:
            return
        _, start, end = CATEGORIES[idx]
        self.current_chars = get_chars(start, end)
        self._render_grid(self.current_chars)

    def _on_category(self, idx):
        self.search_entry.blockSignals(True)
        self.search_entry.clear()
        self.search_entry.blockSignals(False)
        self._load_category(idx)
        self._clear_selection()

    def _on_search(self):
        q = self.search_entry.text().strip().lower()
        source = self.favorites if self.show_favorites else self.current_chars

        if not q:
            self._render_grid(source)
            return

        filtered = []
        for cp in source:
            ch = chr(cp)
            hex_code = f"u+{cp:04x}"
            name = char_name(cp, self.lang).lower()
            if q in hex_code or q in str(cp) or q in ch.lower() or q in name:
                filtered.append(cp)
        self._render_grid(filtered)

    def _render_grid(self, chars):
        # Czyszczenie starego gridu
        self.buttons_map.clear()
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        count_text = LANG[self.lang]["count_char"] if len(chars) == 1 else LANG[self.lang]["count_chars"]
        self.count_label.setText(count_text.format(len(chars)))

        for i, cp in enumerate(chars):
            ch = chr(cp)
            btn = QPushButton(ch)
            btn.setFont(QFont("Segoe UI", 13))
            btn.setFixedSize(42, 42)
            btn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
            
            # Kolor przycisku, jeśli jest w ulubionych
            if cp in self.favorites:
                btn.setStyleSheet("background-color: #fef3c7; border-color: #f59e0b;")
            else:
                btn.setStyleSheet("background-color: #ffffff;")

            # Obsługa kliknięć (lewy i prawy)
            btn.clicked.connect(lambda checked, c=cp: self._select(c))
            btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
            btn.customContextMenuRequested.connect(lambda pos, c=cp: self._show_context_menu(pos, c))

            row = i // COLS
            col = i % COLS
            self.grid_layout.addWidget(btn, row, col)
            self.buttons_map[cp] = btn

        # Reset pozycji suwaka do góry
        self.scroll_area.verticalScrollBar().setValue(0)

    def _select(self, cp):
        # Reset starych stylów przed zmianą zaznaczenia
        if self.selected_cp in self.buttons_map:
            old_btn = self.buttons_map[self.selected_cp]
            if self.selected_cp in self.favorites:
                old_btn.setStyleSheet("background-color: #fef3c7; border-color: #f59e0b;")
            else:
                old_btn.setStyleSheet("background-color: #ffffff;")

        self.selected_cp = cp
        ch = chr(cp)
        name = char_name(cp, self.lang)
        hex4 = f"U+{cp:04X}"
        html_ent = f"&#{cp};"
        py_esc = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"

        self.preview_label.setText(ch)
        self.name_label.setText(name)
        self.code_label.setText(f"{hex4}   HTML: {html_ent}   Python: {py_esc}   Dec: {cp}")

        self.copy_btn.setEnabled(True)
        self.copy_seq_btn.setEnabled(True)

        # Wizualne podświetlenie nowego aktywnego przycisku
        if cp in self.buttons_map:
            self.buttons_map[cp].setStyleSheet("background-color: #dbeafe; border-color: #2563eb;")

    def _clear_selection(self):
        self.selected_cp = None
        self.preview_label.clear()
        self.name_label.setText(LANG[self.lang]["click_hint"])
        self.code_label.clear()
        self.copy_btn.setEnabled(False)
        self.copy_seq_btn.setEnabled(False)

    def _copy_char(self):
        if self.selected_cp is not None:
            QApplication.clipboard().setText(chr(self.selected_cp))
            self._flash_btn(self.copy_btn)

    def _copy_seq(self):
        if self.selected_cp is not None:
            cp = self.selected_cp
            seq = f"\\u{cp:04X}" if cp <= 0xFFFF else f"\\U{cp:08X}"
            QApplication.clipboard().setText(seq)
            self._flash_btn(self.copy_seq_btn)

    def _flash_btn(self, btn):
        orig_text = btn.text()
        btn.setText(LANG[self.lang]["copied"])
        btn.setStyleSheet("background-color: #d1fae5; border-color: #10b981; color: #065f46;")
        
        # Przywrócenie pierwotnego wyglądu przycisku po 1.2s przy użyciu QTimer
        from PyQt6.QtCore import QTimer
        QTimer.singleShot(1200, lambda: self._reset_btn_style(btn, orig_text))

    def _reset_btn_style(self, btn, text):
        btn.setText(text)
        btn.setStyleSheet("")

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
        else:
            # Zaktualizuj styl konkretnego przycisku bez przeładowywania siatki
            if cp in self.buttons_map:
                btn = self.buttons_map[cp]
                if cp in self.favorites:
                    btn.setStyleSheet("background-color: #fef3c7; border-color: #f59e0b;")
                else:
                    btn.setStyleSheet("background-color: #ffffff;")

    def _toggle_favorites_panel(self):
        self.show_favorites = not self.show_favorites
        self.search_entry.clear()
        if self.show_favorites:
            self.fav_btn.setStyleSheet("background-color: #fef3c7; border-color: #f59e0b;")
            self.cat_combo.setEnabled(False)
            self._render_grid(self.favorites)
        else:
            self.fav_btn.setStyleSheet("")
            self.cat_combo.setEnabled(True)
            self._load_category(self.cat_combo.currentIndex())

    def _show_context_menu(self, pos, cp):
        menu = QMenu(self)
        menu.setStyleSheet("""
            QMenu { background-color: #ffffff; border: 1px solid #e5e7eb; }
            QMenu::item { padding: 6px 20px; }
            QMenu::item:selected { background-color: #f3f4f6; color: #111827; }
        """)
        
        if cp in self.favorites:
            action = menu.addAction(LANG[self.lang]["remove_from_fav"])
        else:
            action = menu.addAction(LANG[self.lang]["add_to_fav"])
            
        action.triggered.connect(lambda: self._toggle_favorite(cp))
        menu.exec(QCursor.pos())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TablicaZnakow()
    window.show()
    sys.exit(app.exec())