from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QLabel, QMessageBox, \
    QRadioButton, QGroupBox, QButtonGroup, QListWidget, QLineEdit, QTextEdit, QInputDialog
import json

# Создаем приложение
app = QApplication([])
notes = []
"""Интерфейс приложения"""
window = QWidget()
window.setWindowTitle('Smart note')
window.resize(900, 600)

# Виджеты окна приложения
list_notes = QListWidget()
list_note_label = QLabel('Список заметок')

btn_create_note = QPushButton('Создать заметку')
btn_delete_note = QPushButton('Удалить заметку')
btn_save_note = QPushButton('Сохранить заметку')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Введите тег...')
field_text = QTextEdit()

btn_add_tag = QPushButton('Добавить к заметке')
btn_del_tag = QPushButton('Открепить от заметки')
btn_search_tag = QPushButton('Искать заметку по тегу')

list_tags = QListWidget()
list_tag_label = QLabel('Список тегов')

# Расположение виджетов по лэйаутам
layout_notes = QHBoxLayout()
col1 = QVBoxLayout()
col1.addWidget(field_text)

col2 = QVBoxLayout()
col2.addWidget(list_note_label)
col2.addWidget(list_notes)

row1 = QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_delete_note)

row2 = QHBoxLayout()
row2.addWidget(btn_save_note)

col2.addLayout(row1)
col2.addLayout(row2)

col2.addWidget(list_tag_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)

row3 = QHBoxLayout()
row3.addWidget(btn_add_tag)
row3.addWidget(btn_del_tag)

row4 = QHBoxLayout()
row4.addWidget(btn_search_tag)

col2.addLayout(row3)
col2.addLayout(row4)

layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)

window.setLayout(layout_notes)

"""Функционал приложения"""

"""работа с текстом заметки"""


def add_note():
    note_name, ok = QInputDialog.getText(window, 'Добавить заметку', 'Название заметки')
    if ok and note_name != '':
        notes[note_name] = {"текст": "", "теги": []}
        list_notes.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)


# запись в json

def show_note():
    """получаем текст из заметки с выделенным названием и отображаем его в поле редактирования"""
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)
        with open('notes_data.json', 'w', encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('заметка для удаления не выбрана')


def save_note():
    """сохраняет изменения в заметку"""
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        notes[key]["текст"] = field_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print('заметка для сохранения не выбрана')


"""работа с тегами"""


def add_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]['теги']:
            notes[key]['теги'].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
            with open("notes_data.json", "w", encoding="utf-8") as file:
                json.dump(notes, file, sort_keys=True, ensure_ascii=False)
            print(notes)
        else:
            print('заметка для добавления тега не выбрана')

def del_tag():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open('notes_data.json', 'w', encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print('тег для удаления не выбран')

def search_tag():
    tag = field_tag.text()
    if btn_search_tag.text() == 'Искать заметку по тегу' and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        btn_search_tag.setText('Сбросить поиск')
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes_filtered)
        print(btn_search_tag.text())
    elif btn_search_tag.text() == 'Сбросить поиск':
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        btn_search_tag.setText('Искать заметку по тегу')
        print(btn_search_tag.text())



"""запуск приложения"""
# подключение обработки событий
btn_create_note.clicked.connect(add_note)
btn_save_note.clicked.connect(save_note)
list_notes.itemClicked.connect(show_note)
btn_delete_note.clicked.connect(del_note)
btn_del_tag.clicked.connect(del_tag)
btn_add_tag.clicked.connect(add_tag)
btn_search_tag.clicked.connect(search_tag)

window.show()

with open('notes_data.json', 'r', encoding="utf-8") as file:
    notes = json.load(file)
list_notes.addItems(notes)

app.exec_()
