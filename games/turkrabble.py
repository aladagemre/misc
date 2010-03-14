#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtCore import (QRectF, QSize, Qt, SIGNAL, QString)
from PyQt4.QtGui import (QApplication, QPainter, QPen, QSizePolicy,QFont, QMessageBox, QWidget)

BLANK, X, O, TIE= range(4)
SIZE = 10

class CountersWidget(QWidget):

    def __init__(self, parent=None):
        super(CountersWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))
        self.grid = [[BLANK] * SIZE for i in range(SIZE)]
        self.selected = [0, 0]
	self.setMinimumSize(self.minimumSizeHint())
	self.player = 1


    def sizeHint(self):
        return QSize(500, 500)


    def minimumSizeHint(self):
        return QSize(400, 400)


    def mousePressEvent(self, event):
        xOffset = self.width() / SIZE
        yOffset = self.height() / SIZE
        if event.x() < xOffset:
            x = 0
        elif event.x() < (SIZE-1) * xOffset:
            x = 1
        else:
            x = SIZE-1
        if event.y() < yOffset:
            y = 0
        elif event.y() < (SIZE-1) * yOffset:
            y = 1
        else:
            y = SIZE-1
        cell = self.grid[x][y]
	
        if cell == BLANK:
	    ps = self.getPlayerLetter()
            cell = ps
        self.grid[x][y] = cell
        self.selected = [x, y]
        self.update()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.selected[0] = (SIZE-1 if self.selected[0] == 0
                               else self.selected[0] - 1)
        elif event.key() in (Qt.Key_Right, Qt.Key_Tab):
            self.selected[0] = (0 if self.selected[0] == SIZE-1
                                else self.selected[0] + 1)
        elif event.key() == Qt.Key_Up:
            self.selected[1] = (SIZE-1 if self.selected[1] == 0
                                else self.selected[1] - 1)
        elif event.key() in (Qt.Key_Down, Qt.Key_Return):
            self.selected[1] = (0 if self.selected[1] == SIZE-1
                                else self.selected[1] + 1)
	else:
	    
	    qstr = QString(event.key())
	    print(qstr)
	    ascii_code = event.key()
	    
	    if (ascii_code >= 65 and ascii_code <=90) or ascii_code in [199, 214, 220, 286, 304, 350]:
		character = qstr
		print( character )
		x,y = self.selected
		cell = self.grid[x][y]
		
		if cell == BLANK:
		    print(cell)
		    cell = character
		    self.grid[x][y] = cell
        self.update()


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        xOffset = self.width() / SIZE
        yOffset = self.height() / SIZE
        for x in range(SIZE):
            for y in range(SIZE):
                cell = self.grid[x][y]
                rect = (QRectF(x * xOffset, y * yOffset,
                        xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5))
		great_rect = QRectF(x * xOffset, y * yOffset,
                        xOffset, yOffset)
                
                if cell != BLANK:
                    painter.save()
                    painter.setPen(Qt.black)
		    font = QFont()
		    font.setPointSize(20)
		    painter.setFont(font)
		    painter.drawText(rect, Qt.AlignCenter, cell)
                    painter.restore()
                if [x, y] == self.selected:
                    painter.setPen(QPen(Qt.blue, SIZE))
                else:
                    painter.setPen(Qt.black)
                painter.drawRect(rect)
if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = CountersWidget()
    form.setWindowTitle("Turkrabble")
    form.show()
    app.exec_()