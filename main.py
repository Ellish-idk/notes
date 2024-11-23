from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QListWidgetItem
from ui import Ui_MainWindow
from qt_material import apply_stylesheet
import json
from datetime import datetime


notes_base = {
    "Нова нотатка": "Тут буде текст вашої нотатки."
}

class Widget(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.name = "Нова нотатка"
        self.load_notes()
        self.ui.notesList.itemClicked.connect(self.show_note)
        self.ui.saveNote.clicked.connect(self.save_note)
        self.ui.createNote.clicked.connect(self.new_note)
        self.ui.deleteNote.clicked.connect(self.del_note)
        # self.ui.searchButton.clicked.connect(self.search_note) # ця кнопка не існує
        self.ui.searchNoteTxt.textChanged.connect(self.search_note)

    def load_notes(self):
        self.ui.notesList.clear()
        try:
            with open("notes.json", "r", encoding="utf-8") as file:
                self.notes_base = json.load(file)
        except FileNotFoundError:
            self.notes_base = {
                "Нова нотатка": {
                    "text": "Тут буде текст вашої нотатки.",
                },
            }
        self.show_notesList(self.notes_base)

    def show_notesList(self, notes):
        for title, note in notes.items():
            item = QListWidgetItem(title)
            if "datetime" in note:
                tip = f"Збережено: {note["datetime"]}"
                item.setToolTip(tip)
            self.ui.notesList.addItem(item)

    def show_note(self):
        self.name = self.ui.notesList.selectedItems()[0].text()
        self.ui.noteTitle.setText(self.name)
        self.ui.NoteText.setText(self.notes_base[self.name]["text"])
        
    def new_note(self):
        self.ui.noteTitle.clear()
        self.ui.NoteText.clear()
        self.name = "Нова нотатка"

    def del_note(self):
        if self.name in self.notes_base:
            del self.notes_base[self.name]
            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(self.notes_base,file,ensure_ascii=False)
            self.load_notes()
        self.new_note()

    def save_note(self):
        title = self.ui.noteTitle.text().strip()
        if title != "":
            if title != self.name:
                if self.name in self.notes_base:
                    del self.notes_base[self.name]
                self.name = title
                self.notes_base[title] = {}
                self.notes_base[title]["text"] = self.ui.NoteText.toPlainText()
            else:
                self.notes_base[self.name]["text"] = self.ui.NoteText.toPlainText()

            now = datetime.now().strftime("%d.%m.%Y %H:%M")
            self.notes_base[self.name]['datetime'] = now

            with open("notes.json", "w", encoding="utf-8") as file:
                json.dump(self.notes_base,file, ensure_ascii=False)

            self.load_notes()
        else:
            errorMessage = QMessageBox()
            errorMessage.setWindowTitle("Помилка")
            errorMessage.setText("Додайте назву нотатки")
            errorMessage.setIcon(QMessageBox.Warning)
            errorMessage.exec_()

    def search_note(self):
        search = self.ui.searchNoteTxt.text().strip().lower()
        result = {}
        if search != "":
            title_list = self.notes_base.keys()
            for title in title_list:
                if search in title.lower():
                    result[title] = self.notes_base[title]

            self.ui.notesList.clear()
            self.show_notesList(result)
        else:
            self.ui.notesList.clear()
            self.show_notesList(self.notes_base)


app = QApplication([])
ex = Widget()

apply_stylesheet(app, theme='dark_lightgreen.xml')
ex.show()
app.exec_()