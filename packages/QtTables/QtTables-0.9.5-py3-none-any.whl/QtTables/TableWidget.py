from PySide2 import QtWidgets, QtCore
from itertools import zip_longest


class Table(QtWidgets.QTableWidget):
    def __init__(self, parent, columns, horizontal_labels=(), rows=0, section_resize_mode=QtWidgets.QHeaderView.Stretch):
        super().__init__(parent)
        self.columns = columns
        self.columns_length = len(self.columns)
        self.setColumnCount(self.columns_length)
        self.setHorizontalHeaderLabels(horizontal_labels)
        self.horizontalHeader().setSectionResizeMode(section_resize_mode)
        self.ids_names = {i: value for i, value in enumerate(horizontal_labels)}
        self.setVerticalScrollBarPolicy(self.verticalScrollBarPolicy().ScrollBarAlwaysOn)
        for _ in range(rows):
            self.addRow()
        self.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
    
    def disable(self, disable):
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                cell_widget = self.cellWidget(i, j)
                if cell_widget is not None:
                    cell_widget.setDisabled(disable)

    def setColumns(self, columns, horizontal_labels=()):
        self.columns = columns
        self.columns_length = len(columns)
        self.setColumnCount(self.columns_length)
        for j in range(self.rowCount()):
            for i in range(self.columns_length):
                cell_widget = self.cellWidget(j, i)
                next(self.columns[i])
                new_cell_widget = self.columns[i].send((self, j, i))
                if cell_widget is not None:
                    new_cell_widget.setContent(cell_widget.content())
                    cell_widget.deleteLater()
                self.setCellWidget(j, i, new_cell_widget)
        self.setHorizontalHeaderLabels(horizontal_labels)
        self.ids_names = {i: value for i, value in enumerate(horizontal_labels)}

    def addRow(self, index=-1, contents=()):
        if index < 0:
            index = self.rowCount() + index + 1
        self.insertRow(index)
        for i, (column, content) in enumerate(zip_longest(self.columns, contents, fillvalue=None)):
            if column is not None:
                next(column)
                widget = column.send((self, index, i))
                if content is not None:
                    widget.setContent(content)
                self.setCellWidget(index, i, widget)

    def setRowContents(self, index, contents):
        for i in range(self.columns_length):
            cell_widget = self.cellWidget(index, i)
            cell_widget.setContents(contents[i])

    def removeRow(self, index=-1, current_row=False):
        if current_row:
            index = self.currentRow()
        else:
            if index < 0:
                index = self.rowCount() + index + 1
        if index != -1:
            for j in range(self.columns_length):
                self.cellWidget(index, j).deleteLater()
            super().removeRow(index)
            for i in range(index, self.rowCount()):
                for j in range(self.columns_length):
                    self.cellWidget(i, j).row.index -= 1

    def getAllContents(self):
        all_contents = []
        for i in range(self.rowCount()):
            contents = []
            for j in range(self.columns_length):
                contents.append(
                    self.cellWidget(i, j).content()
                )
            all_contents.append(contents)
        return all_contents

    def setAllContents(self, all_contents):
        self.clear()
        for contents in all_contents:
            self.addRow(contents=contents)

    def clear(self):
        for i in range(self.rowCount()):
            for j in range(self.columns_length):
                self.cellWidget(i, j).deleteLater()
        self.setRowCount(0)


class ControlLayout(QtWidgets.QHBoxLayout):
    added = QtCore.Signal()
    removed = QtCore.Signal()
    loaded = QtCore.Signal()
    saved = QtCore.Signal()

    def __init__(self, add=True, remove=True, load=False, save=False, icons=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.allWidgets = {}

        if not isinstance(icons, dict):
            icons = {}
        if 'Add' in icons:
            add_args = icons['Add'], '', self.parent()
        else:
            add_args = 'Add', self.parent()
        if 'Remove' in icons:
            remove_args = icons['Remove'], '', self.parent()
        else:
            remove_args = 'Remove', self.parent()
        if 'Save' in icons:
            save_args = icons['Save'], '', self.parent()
        else:
            save_args = 'Save', self.parent()
        if 'Load' in icons:
            load_args = icons['Load'], '', self.parent()
        else:
            load_args = 'Load', self.parent()

        if add:
            add_button = QtWidgets.QPushButton(*add_args)
            add_button.setFixedSize(24, 24)
            add_button.clicked.connect(self.added.emit)
            add_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.addWidget(add_button)
            self.allWidgets['Add'] = add_button
        if remove:
            remove_button = QtWidgets.QPushButton(*remove_args)
            remove_button.setFixedSize(24, 24)
            remove_button.clicked.connect(self.removed.emit)
            remove_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.addWidget(remove_button)
            self.allWidgets['Remove'] = remove_button
        if save:
            save_button = QtWidgets.QPushButton(*save_args)
            save_button.setFixedSize(24, 24)
            save_button.clicked.connect(self.saved.emit)
            save_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.addWidget(save_button)
            self.allWidgets['Save'] = save_button
        if load:
            load_button = QtWidgets.QPushButton(*load_args)
            load_button.setFixedSize(24, 24)
            load_button.clicked.connect(self.loaded.emit)
            load_button.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
            self.addWidget(load_button)
            self.allWidgets['Load'] = load_button
        self.addStretch(False)

    def setDisabled(self, disable):
        for widget in self.allWidgets.values():
            widget.setDisabled(disable)
