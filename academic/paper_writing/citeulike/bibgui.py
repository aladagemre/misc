#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
GUI for bibtex fetcher. You can search for a paper. Double click to see its bibtex. Click on save to append the bibtex to references.bib
"""
import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from fetch_bibtex import *

class BibWindow(QMainWindow):
	def __init__(self):
		QMainWindow.__init__(self)
		
		
	def setupGUI(self):
		self.term_label = QLabel("Search Term:")
		self.query_box = QLineEdit()
		self.result_list = QListWidget()
		
		self.layout = QVBoxLayout()
		self.layout.addWidget(self.term_label)
		self.layout.addWidget(self.query_box)
		self.layout.addWidget(self.result_list)
		
		
		self.widget = QWidget()
		self.widget.setLayout(self.layout)
		self.setCentralWidget(self.widget)
		
		self.setWindowTitle("BibFetcher")
		self.connect_slots()
		
	def connect_slots(self):
		self.query_box.returnPressed.connect(self.query)
		self.result_list.itemDoubleClicked.connect(self.display)
		
	def query(self):
		term = self.query_box.text()
		self.result_list.clear()
		self.pairs = dict( search(term) )
		for title in sorted(self.pairs):
			self.result_list.addItem(title)
		
	def display(self, item):
		title = str(item.text())
		url = self.pairs[title]
		content = fetch_content(url)
		self.a = AppendWidget()
		self.a.show_bib(content)
		self.a.show()


class AppendWidget(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self,parent)
		layout = QVBoxLayout()
		self.setLayout(layout)
		self.setGeometry(100,100,800,600)
		self.box = QTextEdit()
		self.button = QPushButton("Save")
		layout.addWidget(self.box)
		layout.addWidget(self.button)
		
		self.button.pressed.connect(self.append)
		
	def show_bib(self, text):
		self.box.setText(text)

	def append(self):
		content = str(self.box.toPlainText())
		append_content("references.bib", content)
		self.close()
def main():
    app = QApplication(sys.argv)
    mainWindow = BibWindow()
    mainWindow.setupGUI()
    mainWindow.showMaximized()
    sys.exit(app.exec_())

if __name__ == "__main__":

    main()
