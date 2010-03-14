from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

class HeatMapWidget(QWidget):
    def __init__(self, filename, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)        
        self.ready = False
        self.fontSize = 12
        self.filename = filename
        self.importHeatmapFile(filename)
        self.drawHeatmap()
        #self.setSizePolicy ( QSizePolicy.Minimum , QSizePolicy.Maximum)
        sizePolicy = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        #sizePolicy.setHorizontalStretch(100)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.resize(self.minimumSizeHint())
        
        self.setMaximumSize(QSize(self.leftMargin + 20 * len(self.columns) + 20, self.topMargin + 20 * len(self.rows) + 10))

    def contextMenuEvent(self, event):
        menu = QMenu()
        saveImage = menu.addAction("Save As Image")
        #print dir(event)
        action = menu.exec_(event.globalPos())
        if action == saveImage:
            filename = QFileDialog.getSaveFileName(self, "Save Image",
                            self.filename.split(".")[0]+".png", "Images (*.png *.xpm *.jpg)")
            self.image.save(filename)
            

            
    def minimumSizeHint(self):
        return QSize(self.leftMargin + 20 * len(self.columns) + 20, self.topMargin + 20 * len(self.rows) + 10)
    def setColumns(self, columns):
        self.columns = [str(column) for column in columns]
        maxLen = 0
        for column in self.columns:
            if len(str(column)) > maxLen:
                maxLen = len(str(column))
        self.topMargin = maxLen * (self.fontSize - 4) + 20
        
    def setRows(self, rows):
        self.rows = [str(row) for row in rows]
        maxLen = 0
        for row in self.rows:
            if len(str(row)) > maxLen:
                maxLen = len(str(row))
        self.leftMargin = maxLen * (self.fontSize - 4) + 5
        
    def setMatrix(self, matrix):
        self.matrix = matrix
    def __findMiddle(self):
        valueList = []
        for row in self.matrix:
            for value in row:
                valueList.append(value)

        valueList = list(set(valueList))
        valueList.sort()
        
        lenV = len(valueList)
        if len(valueList) % 2 == 1:
            self.medianIndex =  (lenV+1)/2-1
        else:
            lower = lenV/2-1
            #upper = valueList[lenV/2]
            self.medianIndex = int(lower) #(float(lower + upper)) / 2
        
        self.medianElement = valueList[self.medianIndex]

        self.numGreen = self.medianIndex
        self.ratioGreen = 255.0 / self.numGreen
        self.numRed = lenV - self.medianIndex - 1
        self.ratioRed = 255.0 / self.numRed

        self.colorDict = {}
        colorValue = 0
        for value in valueList[:self.medianIndex]:
            colorValue += self.ratioGreen
            colorValue = int(round(colorValue))
            self.colorDict[value] = QColor(0, 255 - colorValue, 0)

        self.colorDict[self.medianElement] = QColor(0, 0, 0)

        colorValue = 0
        for value in valueList[self.medianIndex+1:]:
            colorValue += self.ratioRed
            colorValue = int(round(colorValue))
            self.colorDict[value] = QColor(colorValue, 0, 0)
        """
        print valueList[:self.medianIndex+1]
        print "value:", self.matrix[self.rows.index("YFL054C")][0]
        print "median value:", self.medianElement
        print "greennum:", self.numGreen
        print self.colorDict[self.matrix[self.rows.index("YFL054C")][0]].getRgb()"""
        #for key in self.colorDict:
            #print key, self.colorDict[key].getRgb()
    def __assignColors(self):
        rowCount = len(self.matrix)
        for rowNum in range(rowCount):
            colCount = len(self.matrix[rowNum])
            for colNum in range(colCount):
                value = self.matrix[rowNum][colNum]
                self.matrix[rowNum][colNum] = self.colorDict[value]

    def importMatrixFile(self, filename):
        matrix = []
        f = open(filename)
        for line in f:
            matrix.append([double(value) for value in line.strip().split()])
        self.matrix = matrix

    def importHeatmapFile(self, filename):
        matrix = []
        f = open(filename)
        r, c = f.readline().strip().split()
        self.setColumns(f.readline().strip().split()[1:])

        rows = []
        for line in f:
            lineList = line.strip().split()
            rows.append(lineList[0])
            #print "genename:", lineList[0]
            #print "data", [float(value) for value in lineList[1:]]
            matrix.append([float(value) for value in lineList[1:]])

        self.setRows(rows)
        self.setMatrix(matrix)
        
    def test(self):
        cols = ["ABCD","EFGH","IJKL"]
        rows = ["YAL001C","YAL021C-A","YAL001C-ABC","EYAL001C2-303r3fe"]

        #self.matrix = [ [1,2,3], [4,5,6], [7,8,9], [10,11,12]]
        self.importMatrixFile("matrix.txt")
        
        self.setColumns(cols)
        self.setRows(rows)
        #self.setMatrix(self.matrix)

        self.__findMiddle()
        self.__assignColors()

        self.ready = True

    def drawHeatmap(self):
        self.__findMiddle()
        self.__assignColors()
        self.ready = True
        
    def paintEvent(self, event=None):
        image= QImage(self.minimumSizeHint().width(), self.minimumSizeHint().height(),  QImage.Format_ARGB32_Premultiplied)
        self.image = image
        imagePainter = QPainter(image)
        imagePainter.initFrom(self)
        imagePainter.setRenderHint(QPainter.Antialiasing, True)
        imagePainter.setRenderHint(QPainter.Antialiasing)
        imagePainter.setRenderHint(QPainter.TextAntialiasing)
        imagePainter.setPen(self.palette().color(QPalette.Mid))
        imagePainter.setBrush(self.palette().brush(QPalette.AlternateBase))
        imagePainter.eraseRect(self.rect())
        if self.ready:
            imagePainter.setPen(QColor(Qt.black))
            imagePainter.setBrush(QColor(Qt.black))
            imagePainter.rotate(-90)
            yval = self.leftMargin + 35
            for column in self.columns:
                imagePainter.drawText(QPoint(-self.topMargin + 3, yval), column)
                yval += 20
            imagePainter.rotate(90)
            
            
            rowCount = len(self.matrix)
            for rowNum in range(rowCount):
                # Print row labels
                imagePainter.setPen(QColor(Qt.black))
                imagePainter.drawText(QRectF(10, self.topMargin + rowNum*20, self.leftMargin, 20), (Qt.AlignRight|Qt.AlignVCenter), self.rows[rowNum])

                # Display colors

                colCount = len(self.matrix[rowNum])
                for colNum in range(colCount):
                    value = self.matrix[rowNum][colNum]
                    imagePainter.setBrush(value)
                    imagePainter.setPen(value)
                    imagePainter.drawRect(20 + self.leftMargin + colNum*20, self.topMargin + rowNum*20, 20, 20)



        #draw(imagePainter)
        imagePainter.end()
        painter = QPainter(self)
        painter.drawImage(0, 0, image)
        """
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(self.palette().color(QPalette.Mid))
        painter.setBrush(self.palette().brush(QPalette.AlternateBase))
        painter.setClipping(True)

        if self.ready:
            painter.setPen(QColor(Qt.black))
            painter.rotate(-90.0)
            
            painter.drawText(QPointF(self.leftMargin+5, 0), "Hede")
            painter.rotate(90.0)
            

            rowCount = len(self.matrix)
            for rowNum in range(rowCount):
                # Print row labels
                painter.setPen(QColor(Qt.black))
                painter.drawText(QRectF(0, self.topMargin + rowNum*20, self.leftMargin-10, 20), (Qt.AlignRight|Qt.AlignVCenter), self.rows[rowNum])

                # Display colors
                
                colCount = len(self.matrix[rowNum])
                for colNum in range(colCount):
                    value = self.matrix[rowNum][colNum]
                    painter.setBrush(value)
                    painter.setPen(value)
                    painter.drawRect(self.leftMargin + colNum*20, self.topMargin + rowNum*20, 20, 20)"""



if __name__ =="__main__":
    app = QApplication(sys.argv)
    h = HeatMapWidget("out0.txt")
    h.resize(250, 150)
    h.setWindowTitle('Heatmap')
    
    h.show()
    sys.exit(app.exec_())

    