from PyQt4.QtCore import *
from PyQt4.QtGui import *

import sys

class DataTableWidget(QWidget):
    def __init__(self, filename, parent=None, flags=Qt.Widget):
        QWidget.__init__(self, parent, flags)
        self.ready = False
        self.fontSize = 12
        self.width = 800 # Only drawing area
        self.height = 400
        self.leftMargin = 30
        self.topMargin = 30
        self.notchMargin = 3
        self.filename = filename
        self.importDataFile(filename)
        self.drawTable()
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        #sizePolicy.setHorizontalStretch(100)
        #sizePolicy.setVerticalStretch(0)
        #sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setMaximumSize(QSize(self.width + self.leftMargin + 100 , self.height + self.topMargin + 100))
    def minimumSizeHint(self):
        return QSize(self.width + self.leftMargin + 100 , self.height + self.topMargin + 100)
    def maximumSizeHint(self):
        return QSize(self.width + self.leftMargin + 100 , self.height + self.topMargin + 100)
    
    def contextMenuEvent(self, event):
        menu = QMenu()
        saveImage = menu.addAction("Save As Image")
        #print dir(event)
        action = menu.exec_(event.globalPos())
        if action == saveImage:
            filename = QFileDialog.getSaveFileName(self, "Save Image",
                            self.filename.split(".")[0]+".png", "Images (*.png *.xpm *.jpg)")
            self.image.save(filename)

    def setColumns(self, columns):
        self.columns = [str(column) for column in columns]
        maxLen = 0
        for column in self.columns:
            if len(str(column)) > maxLen:
                maxLen = len(str(column))
        

    def setRows(self, rows):
        self.rows = [str(row) for row in rows]
        maxLen = 0
        for row in self.rows:
            if len(str(row)) > maxLen:
                maxLen = len(str(row))
        

    def setMatrix(self, matrix):
        self.matrix = matrix
        
    def importDataFile(self, filename):
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


    def __findSpaces(self):
        self.colspace = self.width / float(len(self.columns) - 1)
    def __findMinMax(self):
        self.maxs = [] # Maximum value for each column.
        self.mins = [] # Minimum value for each column.
        
        for col in range(len(self.columns)):
            # Go col by col
            maxval = float("-inf")
            minval = float("inf")
            for row in range(len(self.rows)):
                value = self.matrix[row][col]

                if value > maxval:
                    maxval = value
                if value < minval:
                    minval = value
                
            self.maxs.append(maxval)
            self.mins.append(minval)


            
                
    def __findVerticalLines(self):
        """Creates the vertical QLineFs."""
        self.verticalLines = []
        
        for i in range(len(self.columns)):
            x1 = self.leftMargin + i * self.colspace
            y1 = self.topMargin - 10
            x2 = x1
            y2 = self.topMargin + self.height + 10
            line = QLineF(x1, y1, x2, y2)
            self.verticalLines.append(line)
            # start notch
            line = QLineF(x1 - self.notchMargin, y1+10, x1 + self.notchMargin, y1+10)
            self.verticalLines.append(line)
            # end notch
            line = QLineF(x1 - self.notchMargin, y2-10, x1 + self.notchMargin, y2-10)
            self.verticalLines.append(line)



    def __scaleMatrix(self):
        for col in range(len(self.columns)):
            # Go col by col
            maxval = self.maxs[col]
            minval = self.mins[col]
            for row in range(len(self.rows)):
                value = self.matrix[row][col]
                self.matrix[row][col] = (self.height * (maxval - value)) / (maxval - minval)
                

    def __findPlotLines(self):
        self.plotLines = []
        for row in range(len(self.rows)):
            for col in range(len(self.columns) - 1):
                y1 = self.matrix[row][col]
                y2 = self.matrix[row][col + 1]
                line = QLineF(self.leftMargin + col * self.colspace, self.topMargin + y1, self.leftMargin + (col + 1 ) * self.colspace, self.topMargin + y2 )
                self.plotLines.append( line )

                

    def drawTable(self):
        self.__findSpaces()
        self.__findMinMax()
        self.__findVerticalLines()
        self.__scaleMatrix()
        self.__findPlotLines()

        
        self.ready = True
    def __drawVerticalLines(self, painter):
        painter.setPen(QPen(QColor(Qt.gray)))
        for line in self.verticalLines:
            painter.drawLine(line)
    def __drawPlotLines(self, painter):
        pen = QPen(QColor(Qt.red))
        painter.setPen(pen)
        for line in self.plotLines:
            painter.drawLine(line)

    def __printLabels(self, painter):
        painter.setPen(QColor(Qt.black))
        painter.rotate(90)
        painter.drawText(QPoint(-15,15), "Heyo")
        for col in range(len(self.columns)):
            painter.drawText(QPoint(self.topMargin + self.height + 12, -1 * (self.leftMargin - 2 + col * self.colspace )), self.columns[col])
        painter.rotate(-90)
    def __printMaxMinLabels(self, painter):
        for i in range(len(self.columns)):
            x1 = self.leftMargin + i * self.colspace
            y1 = self.topMargin - 10
            x2 = x1
            y2 = self.topMargin + self.height + 10
            painter.drawText(QPoint(x1 + self.notchMargin + 1, y1 + 10), str(self.maxs[i]))
            painter.drawText(QPoint(x1 + self.notchMargin + 2, y2 - 10), str(self.mins[i]))
            """# start notch
            line = QLineF(x1 - self.notchMargin, y1+10, x1 + self.notchMargin, y1+10)
            self.verticalLines.append(line)
            # end notch
            line = QLineF(x1 - self.notchMargin, y2-10, x1 + self.notchMargin, y2-10)
            self.verticalLines.append(line)"""


    def paintEvent(self, event=None):
        image= QImage(self.width + self.leftMargin + 50, self.height + self.topMargin + 100,  QImage.Format_ARGB32_Premultiplied)
        self.image = image
        imagePainter = QPainter(image)
        imagePainter.initFrom(self)
        imagePainter.setRenderHint(QPainter.Antialiasing, True)
        imagePainter.setRenderHint(QPainter.Antialiasing)
        imagePainter.setRenderHint(QPainter.TextAntialiasing)
        #imagePainter.setPen(self.palette().color(QPalette.Mid))
        #imagePainter.setBrush(self.palette().brush(QPalette.AlternateBase))
        imagePainter.setBackground(QBrush(QColor(Qt.white)))
        imagePainter.eraseRect(self.rect())
        if self.ready:
            self.__drawVerticalLines(imagePainter)
            self.__drawPlotLines(imagePainter)
            self.__printLabels(imagePainter)
            self.__printMaxMinLabels(imagePainter)
        imagePainter.end()
        painter = QPainter(self)
        painter.drawImage(0, 0, image)

if __name__ =="__main__":
    app = QApplication(sys.argv)
    h = DataTableWidget("out5.txt")
    h.resize(900, 500)
    h.setWindowTitle('Data Table')

    h.show()
    sys.exit(app.exec_())

