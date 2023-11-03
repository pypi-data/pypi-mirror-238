from PySide2.QtGui import QRegExpValidator
from PySide2.QtCore import QRegExp

int_validator = QRegExpValidator(QRegExp('[0-9]*'))
negative_int_validator = QRegExpValidator(QRegExp('-?[0-9]*'))
double_validator = QRegExpValidator(QRegExp('[0-9]*\.?[0-9]*'))
negative_double_validator = QRegExpValidator(QRegExp('-?[0-9]*\.?[0-9]*'))
scientific_validator = QRegExpValidator(QRegExp('-?[0-9]*\.?[0-9]*e[-+]?[0-9]*'))
