from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from ui import Ui_MainWindow
from qt_material import apply_stylesheet
import json

notes_base = {
    "Нова нотатка": "Тут буде текст вашої нотатки."
}

class Widget(QMainWindow):
    def   __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.read_notes()
        self.ui.notesList.itemClicked.connect(self.show_note)
        self.ui.saveNote.clicked.connect(self.save_note)

    def read_notes(self):
        self.notes_base = {
            "Нова нотатка": {
                "text": "Тут буде текст вашої нотатки.",
                "tags": [],
            }
        }

        self.ui.notesList.addItems(self.notes_base)

    def show_note(self):
        self.name = self.ui.notesList.selectedItems()[0].text()  
        self.ui.noteTitle.setText(self.name)
        self.ui.NoteText.setText(self.notes_base[self.name]["text"])

    def save_note(self):
        self.notes_base[self.name]["text"] = self.ui.NoteText.toPlainText()
        with open("notes.json", "w", encoding="utf-8") as file:
            json.dump(self.notes_base,file)

app = QApplication([])
ex = Widget()

apply_stylesheet(app, theme='dark_lightgreen.xml')
ex.show()
app.exec_()