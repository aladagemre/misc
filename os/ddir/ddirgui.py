# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ddirgui.ui'
#
# Created: Thu May 21 16:00:34 2009
#      by: PyQt4 UI code generator 4.4.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(620, 583)
        self.gridLayout = QtGui.QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtGui.QLabel(Form)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.lineDirectory = QtGui.QLineEdit(Form)
        self.lineDirectory.setObjectName("lineDirectory")
        self.gridLayout.addWidget(self.lineDirectory, 0, 1, 1, 1)
        self.buttonStart = QtGui.QPushButton(Form)
        self.buttonStart.setObjectName("buttonStart")
        self.gridLayout.addWidget(self.buttonStart, 0, 5, 1, 1)
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.buttonLocate = QtGui.QToolButton(Form)
        self.buttonLocate.setObjectName("buttonLocate")
        self.gridLayout.addWidget(self.buttonLocate, 0, 2, 1, 1)
        self.spinSize = QtGui.QSpinBox(Form)
        self.spinSize.setMinimumSize(QtCore.QSize(58, 0))
        self.spinSize.setWrapping(False)
        self.spinSize.setMinimum(0)
        self.spinSize.setMaximum(100000000)
        self.spinSize.setSingleStep(1000)
        self.spinSize.setProperty("value", QtCore.QVariant(1000))
        self.spinSize.setObjectName("spinSize")
        self.gridLayout.addWidget(self.spinSize, 0, 3, 1, 1)
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 0, 4, 1, 1)
        self.table = QtGui.QTableWidget(Form)
        self.table.setAlternatingRowColors(True)
        self.table.setWordWrap(False)
        self.table.setObjectName("table")
        self.table.setColumnCount(3)
        self.table.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 6)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Duplicate Directory Finder", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Directory:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonStart.setText(QtGui.QApplication.translate("Form", "Start", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "Total:", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonLocate.setText(QtGui.QApplication.translate("Form", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Bytes", None, QtGui.QApplication.UnicodeUTF8))
        self.table.setSortingEnabled(True)
        self.table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Form", "Size", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Form", "Dir Name", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Form", "Path", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

