#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Sorts the citations that are unordered.
Reqires two inputs:
1. LaTeX bibitem list: newman2010, lamport94, erdos95
2. Outputing number list: 3, 2, 1

Outputs: erdos95, lamport94, newman2010
"""
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *


class BibWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		
	def setupGUI(self):
		self.bib_label = QLabel("Bibitems (ex: newman2010, lamport94, erdos95):")
		self.num_label = QLabel("Numbers (ex: 3,2,1):")
		self.sorted_label = QLabel("Sorted bibitems:")
		self.bibitem_box = QLineEdit()
		self.numbers_box = QLineEdit()
		self.ordered_box = QLineEdit()
		self.ordered_box.setReadOnly(True)
		
		self.button = QPushButton("Sort")
		
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.bib_label)
		self.layout.addWidget(self.bibitem_box)
		self.layout.addWidget(self.num_label)
		self.layout.addWidget(self.numbers_box)
		self.layout.addWidget(self.button)
		self.layout.addWidget(self.sorted_label)
		self.layout.addWidget(self.ordered_box)
		
		
		
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.setCentralWidget(self.widget)
		
		self.setWindowTitle("Citation Sorter")
		self.connect_slots()
		
	def connect_slots(self):
		self.bibitem_box.returnPressed.connect(self.sort)
		self.numbers_box.returnPressed.connect(self.sort)
		self.button.clicked.connect(self.sort)
		
		
	def sort(self):
		bibitems = str( self.bibitem_box.text() ).strip().split(",")
		numbers = map(int, str( self.numbers_box.text() ).strip().split(","))
		
		pairs = list(zip(numbers, bibitems))
		pairs.sort()
		names = [ name.strip() for num,name in pairs ]
		self.ordered_box.setText(", ".join(names))
		self.copy()
		reply = QMessageBox.information(self, 'Copied to clipboard',
            "Ordered bibitems are copied to the clipboard.", QMessageBox.Ok)
	
	def copy(self):
		clipboard = QApplication.clipboard()
		clipboard.setText( str(self.ordered_box.text()) )
		
def main():
    app = QApplication(sys.argv)
    
    mainWindow = BibWindow()
    mainWindow.setupGUI()
    mainWindow.show()
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()
