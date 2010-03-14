#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2008 Qtrac Ltd. All rights reserved.
# This program or module is free software: you can redistribute it and/or
# modify it under the terms of the GNU General Public License as published
# by the Free Software Foundation, either version 2 of the License, or
# version 3 of the License, or (at your option) any later version. It is
# provided for educational purposes and is distributed in the hope that
# it will be useful, but WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
# the GNU General Public License for more details.

from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from future_builtins import *

from PyQt4.QtCore import (QRectF, QSize, Qt, SIGNAL)
from PyQt4.QtGui import (QApplication, QPainter, QPen, QSizePolicy,QFont, QMessageBox,
        QWidget)

BLANK, X, O, TIE= range(4)


class CountersWidget(QWidget):

    def __init__(self, parent=None):
        super(CountersWidget, self).__init__(parent)
        self.setSizePolicy(QSizePolicy(QSizePolicy.Expanding,
                                       QSizePolicy.Expanding))
        self.grid = [[BLANK] * 3 for i in range(3)]
        self.selected = [0, 0]
	self.setMinimumSize(self.minimumSizeHint())
	self.player = 1

    def getPlayerLetter(self):
	if self.player == 1:
	    self.player = 2
	    return X
	else:
	    self.player = 1
	    return O

    def isTriple(self, t):
	if (t[0]==t[1]==t[2]) and t[0]!=BLANK:
	    return t[0]
	else:
	    return False
	   
    def checkForGameEnd(self):
	# Tie Check
	flag = 0
	for i in range(3):
	    for j in range(3):
		if self.grid[i][j] == BLANK:
		    flag = 1
	if flag == 0:
	    return TIE
	    
	# Horizontal Check
	for row in range(3):
	    result = self.isTriple(self.grid[row])
	    if result:
		return result
	
	# Vertical Check
	for col in range(3):
	    result = self.isTriple([self.grid[0][col], self.grid[1][col], self.grid[2][col]])
	    if result:
		return result
	
	# Diagonal Check 1
	l = []
	for i in range(3):
	    l.append(self.grid[i][i])
	result1 = self.isTriple(l)
	if result1:
	    return result1
	# Diagonal Check 2
	l = []
	for i in range(3):
	    l.append(self.grid[i][2-i])
	result2 = self.isTriple(l)
	if result2:
	    return result2


    def endGame(self, result):
	if result == TIE:
	    QMessageBox.information(self, "Oyun bitti!","Sonuç berabere!")
	else:
	    QMessageBox.information(self, "Oyun bitti!","Oyuncu %s kazandı." % result)
	self.grid = [[BLANK] * 3 for i in range(3)]
        self.selected = [0, 0]
	self.player = 1
	
    def sizeHint(self):
        return QSize(200, 200)


    def minimumSizeHint(self):
        return QSize(100, 100)


    def mousePressEvent(self, event):
        xOffset = self.width() / 3
        yOffset = self.height() / 3
        if event.x() < xOffset:
            x = 0
        elif event.x() < 2 * xOffset:
            x = 1
        else:
            x = 2
        if event.y() < yOffset:
            y = 0
        elif event.y() < 2 * yOffset:
            y = 1
        else:
            y = 2
        cell = self.grid[x][y]
	
        if cell == BLANK:
	    ps = self.getPlayerLetter()
            cell = ps
        self.grid[x][y] = cell
        self.selected = [x, y]
        self.update()


    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.selected[0] = (2 if self.selected[0] == 0
                                else self.selected[0] - 1)
        elif event.key() == Qt.Key_Right:
            self.selected[0] = (0 if self.selected[0] == 2
                                else self.selected[0] + 1)
        elif event.key() == Qt.Key_Up:
            self.selected[1] = (2 if self.selected[1] == 0
                                else self.selected[1] - 1)
        elif event.key() == Qt.Key_Down:
            self.selected[1] = (0 if self.selected[1] == 2
                                else self.selected[1] + 1)
        elif event.key() == Qt.Key_Space:
            x, y = self.selected
            cell = self.grid[x][y]
	    
	    
	    if cell == BLANK:
		ps = self.getPlayerLetter()
		cell = ps

            
            self.grid[x][y] = cell
        self.update()


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing, True)
        xOffset = self.width() / 3
        yOffset = self.height() / 3
        for x in range(3):
            for y in range(3):
                cell = self.grid[x][y]
                rect = (QRectF(x * xOffset, y * yOffset,
                        xOffset, yOffset).adjusted(0.5, 0.5, -0.5, -0.5))
		great_rect = QRectF(x * xOffset, y * yOffset,
                        xOffset, yOffset)
                textToDraw = None
                if cell == X:
                    textToDraw = "X"
                elif cell == O:
                    textToDraw = "O"
                if textToDraw is not None:
                    painter.save()
                    painter.setPen(Qt.black)
                    #painter.setBrush(color)
                    #painter.drawEllipse(rect.adjusted(2, 2, -2, -2))
		    font = QFont()
		    font.setPointSize(20)
		    painter.setFont(font)
		    painter.drawText(rect, Qt.AlignCenter, textToDraw)
                    painter.restore()
                if [x, y] == self.selected:
                    painter.setPen(QPen(Qt.blue, 3))
                else:
                    painter.setPen(Qt.black)
                painter.drawRect(rect)
	result = self.checkForGameEnd()
	if result:
	    self.update()
	    self.endGame(result)
	    self.update()

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    form = CountersWidget()
    form.setWindowTitle("XOX")
    form.show()
    app.exec_()

