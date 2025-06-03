from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QTextEdit, QPushButton, QMenuBar, QMenu, QFileDialog, QFrame)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QTextCursor, QAction, QFont
import requests
import re

class PikiIDE(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PikiScript Editor")
        self.setGeometry(100, 100, 900, 600)
        
        self.theme_dark = True
        self.autocomplete_words = [
            "init():", "end", "getuser.from(", "style.output:",
            "print.age(", "print.own(", "print.cont(", "print.likes(", "print.url(", "print_sep("
        ]
        
        self.init_ui()
        self.set_theme()
    
    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        self.create_menu()
        
        toolbar = QFrame()
        toolbar.setObjectName("toolbar")
        toolbar_layout = QHBoxLayout(toolbar)
        toolbar_layout.setContentsMargins(5, 5, 5, 5)
        
        self.run_button = QPushButton(" Run PikiScript")
        self.run_button.setObjectName("runButton")
        self.run_button.clicked.connect(self.run_script)
        
        self.theme_button = QPushButton("Toggle Theme")
        self.theme_button.setObjectName("themeButton")
        self.theme_button.clicked.connect(self.toggle_theme)
        
        toolbar_layout.addWidget(self.run_button)
        toolbar_layout.addWidget(self.theme_button)
        toolbar_layout.addStretch()
        
        main_layout.addWidget(toolbar)
        
        splitter = QFrame()
        splitter.setFrameShape(QFrame.Shape.StyledPanel)
        splitter_layout = QVBoxLayout(splitter)
        splitter_layout.setContentsMargins(0, 0, 0, 0)
        splitter_layout.setSpacing(0)
        
        self.editor = QTextEdit()
        self.editor.setObjectName("editor")
        editor_font = QFont("Courier New", 12)
        self.editor.setFont(editor_font)
        self.editor.setStyleSheet("font-size: 12pt;")
        
        self.output = QTextEdit()
        self.output.setObjectName("output")
        output_font = QFont("Courier New", 10)
        self.output.setFont(output_font)
        self.output.setStyleSheet("font-size: 10pt;")
        self.output.setReadOnly(True)
        
        splitter_layout.addWidget(self.editor, 70)
        splitter_layout.addWidget(self.output, 30)
        
        main_layout.addWidget(splitter, 1)
    
    def create_menu(self):
        menubar = self.menuBar()
        
        file_menu = menubar.addMenu("File")
        
        open_action = QAction("Open .apiki", self)
        open_action.triggered.connect(self.load_file)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save .apiki", self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)
    
    def run_script(self):
        self.output.clear()
        script = self.editor.toPlainText()
        
        if "init():" in script and "end" in script:
            username_match = re.search(r'getuser\.from\((.*?)\)', script)
            if username_match:
                url = username_match.group(1).strip().strip('"').strip("'")
                try:
                    response = requests.get(url)
                    data = response.json()
                    posts = data.get("posts", [])
                    
                    for post in posts:
                        if "print.age" in script:
                            self.output.insertPlainText(f"AGE: {post.get('createdAt', 'N/A')}\n")
                        if "print.own" in script:
                            self.output.insertPlainText(f"BY: {post.get('author', 'N/A')}\n")
                        if "print.cont" in script:
                            self.output.insertPlainText(f"{post.get('content', '')}\n")
                        if "print.likes" in script:
                            self.output.insertPlainText(f"Likes: {post.get('likes', 0)}\n")
                        if "print.url" in script:
                            self.output.insertPlainText(f"URL: {post.get('url', '')}\n")
                        if "print_sep" in script:
                            self.output.insertPlainText("-----------------------------\n")
                except Exception as e:
                    self.output.insertPlainText(f"Error: {str(e)}\n")
            else:
                self.output.insertPlainText("No valid 'getuser.from(URL)' found.\n")
        else:
            self.output.insertPlainText("Missing init(): or end\n")
    
    def load_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "PikiScript Files (*.piki)")
        if file_path:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                self.editor.setPlainText(content)
    
    def save_file(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save File", "", "Pikiscript Files (*.apiki)")
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
    
    def toggle_theme(self):
        self.theme_dark = not self.theme_dark
        self.set_theme()
    
    def set_theme(self):
        if self.theme_dark:
            self.setStyleSheet("""
                QWidget {
                    background-color: #2b2b2b;
                }
                #editor {
                    background-color: #1e1e1e;
                    color: #ffffff;
                    selection-background-color: #3d3d3d;
                    border: none;
                    font-size: 12pt;
                }
                #output {
                    background-color: #000000;
                    color: #ffffff;
                    selection-background-color: #3d3d3d;
                    border-top: 1px solid #444;
                    font-size: 10pt;
                }
                #toolbar {
                    background-color: #333;
                    border-bottom: 1px solid #444;
                }
                QPushButton {
                    background-color: #444;
                    color: #fff;
                    border: 1px solid #555;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #555;
                }
                QPushButton:pressed {
                    background-color: #666;
                }
                QMenuBar {
                    background-color: #333;
                    color: #fff;
                }
                QMenuBar::item {
                    background-color: transparent;
                    padding: 5px 10px;
                }
                QMenuBar::item:selected {
                    background-color: #444;
                }
                QMenu {
                    background-color: #333;
                    color: #fff;
                    border: 1px solid #444;
                }
                QMenu::item:selected {
                    background-color: #444;
                }
            """)
        else:
            self.setStyleSheet("""
                QWidget {
                    background-color: #f0f0f0;
                }
                #editor {
                    background-color: #ffffff;
                    color: #000000;
                    selection-background-color: #b5d6fd;
                    border: none;
                    font-size: 12pt;
                }
                #output {
                    background-color: #f0f0f0;
                    color: #000000;
                    selection-background-color: #b5d6fd;
                    border-top: 1px solid #ddd;
                    font-size: 10pt;
                }
                #toolbar {
                    background-color: #e0e0e0;
                    border-bottom: 1px solid #ddd;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    color: #000;
                    border: 1px solid #ccc;
                    padding: 5px 10px;
                    border-radius: 4px;
                }
                QPushButton:hover {
                    background-color: #d0d0d0;
                }
                QPushButton:pressed {
                    background-color: #c0c0c0;
                }
                QMenuBar {
                    background-color: #e0e0e0;
                    color: #000;
                }
                QMenuBar::item {
                    background-color: transparent;
                    padding: 5px 10px;
                }
                QMenuBar::item:selected {
                    background-color: #d0d0d0;
                }
                QMenu {
                    background-color: #e0e0e0;
                    color: #000;
                    border: 1px solid #ccc;
                }
                QMenu::item:selected {
                    background-color: #d0d0d0;
                }
            """)

if __name__ == "__main__":
    app = QApplication([])
    window = PikiIDE()
    window.show()
    app.exec()
