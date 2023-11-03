from QtTables.CellWidgets import *


class Index:
    def __init__(self, index):
        self.index = index

    def __repr__(self):
        return str(self.index)

    def __str__(self):
        return str(self.index)


def customCreator(cell_widget, *args, func_after=None, content=None, **kwargs):
    if not callable(cell_widget):
        raise TypeError(f'{cell_widget} is not a callable')
    while True:
        table, row, column = yield
        cell_widget_instance = cell_widget(table, Index(row), Index(column), *args, **kwargs)
        if not hasattr(cell_widget_instance, 'content'):
            raise AttributeError(f'{cell_widget} has not \'content\' attribute')
        if not hasattr(cell_widget_instance, 'setContent'):
            raise AttributeError(f'{cell_widget} has not \'setContent\' attribute')
        if not hasattr(cell_widget_instance, 'thisContentChanged'):
            raise AttributeError(f'{cell_widget} has not \'thisContentChanged\' attribute')
        if not hasattr(cell_widget_instance, 'checkContent'):
            raise AttributeError(f'{cell_widget} has not \'checkContent\' attribute')
        cell_widget_instance.setContent(content)
        if callable(func_after):
            func_after(cell_widget_instance)
        yield cell_widget_instance


def lineEditCreator(validator=None, mask=None, func_after=None, password=False, read_only=False, content=''):
    while True:
        table, row, column = yield
        line_edit = LineEdit(table, Index(row), Index(column))
        if password:
            line_edit.setEchoMode(LineEdit.Password)
        line_edit.setValidator(validator)
        line_edit.setMask(mask)
        line_edit.setReadOnly(read_only)
        line_edit.setContent(content)
        if callable(func_after):
            func_after(line_edit)
        yield line_edit


def comboBoxCreator(func_after=None, content=((), -1)):
    while True:
        table, row, column = yield
        combo_box = ComboBox(table, Index(row), Index(column))
        combo_box.setContent(content)
        if callable(func_after):
            func_after(combo_box)
        yield combo_box


def checkBoxCreator(func_after=None, content=False):
    while True:
        table, row, column = yield
        check_box = CheckBox(table, Index(row), Index(column))
        check_box.setContent(content)
        if callable(func_after):
            func_after(check_box)
        yield check_box
