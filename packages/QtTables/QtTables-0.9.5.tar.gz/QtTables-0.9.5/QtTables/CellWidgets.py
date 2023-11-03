from PySide2 import QtWidgets, QtCore

from QtTables.Validators import scientific_validator


class LineEdit(QtWidgets.QLineEdit):
    thisContentChanged = QtCore.Signal(str)

    def __init__(self, table, row, column):
        super().__init__()
        self.table = table
        self.row = row
        self.column = column
        self.setStyleSheet('border: 0px solid')
        self.textEdited.connect(self.thisContentChanged.emit)
        self.editingFinished.connect(self.checkContent)
        self.editingFinished.connect(lambda: self.thisContentChanged.emit(self.content()))

    def checkContent(self):
        content = self.text()
        validator = self.validator()
        if not content:
            if validator is not None:
                content = '0'
            else:
                content = ''
            self.setText(content)
        elif validator == scientific_validator:
            if content.startswith('e'):
                content = '1' + content
            if content.endswith('e'):
                content = content[:-1]
            if content.endswith('+') or content.endswith('-'):
                content += '1'
            self.setText(content)

    def content(self, check_content=False):
        if check_content:
            self.checkContent()
        return self.text()

    def setContent(self, content):
        self.blockSignals(True)
        self.setText(str(content))
        self.blockSignals(False)


class ComboBox(QtWidgets.QComboBox):
    thisContentChanged = QtCore.Signal(int)

    def __init__(self, table, row, column):
        super().__init__()
        self.table = table
        self.row = row
        self.column = column
        self.currentIndexChanged.connect(self.thisContentChanged.emit)

    def checkContent(self):
        ...

    def content(self):
        return [list(self.itemText(i) for i in range(self.count())), self.currentIndex()]

    def setContent(self, content):
        self.blockSignals(True)
        self.clear()
        self.addItems(content[0])
        self.setCurrentIndex(content[1])
        self.blockSignals(False)
    
    def wheelEvent(self, event):
        event.ignore()


class CheckBox(QtWidgets.QWidget):
    thisContentChanged = QtCore.Signal(int)

    def __init__(self, table, row, column):
        super().__init__()
        self.table = table
        self.row = row
        self.column = column
        self.check_box = QtWidgets.QCheckBox()
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.check_box)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.check_box.stateChanged.connect(self.thisContentChanged.emit)

    def checkContent(self):
        ...

    def content(self):
        return self.check_box.isChecked()

    def setContent(self, content):
        self.blockSignals(True)
        if isinstance(content, str):
            if not content or content in ('0', 'False'):
                content = False
            else:
                content = True
        elif not isinstance(content, bool):
            content = bool(content)
        self.check_box.setChecked(content)
        self.blockSignals(False)
