# coding: utf8
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys

clr=lambda l:l.strip() 

class Segment:
	__slots__= ["start","real_start","real_end","end"]
	def __init__(self, text):
		self.text = text
		self.start = ""
		self.real_start = ""
		self.real_end = ""
		self.end = ""
		self.process()
	def process(self):
		s,e = map(clr, self.text.split("-"))
		if "(" in s:
			self.start, real_start = s.split("(")
			self.real_start = real_start[:real_start.find(")")]
		else:
			self.real_start = s
			
		if "(" in e:
			self.real_end, end = e.split("(")
			self.end= end[:end.find(")")]
		else:
			self.real_end = e
	def get_slots(self):
		try:
			h,m = map(int, self.start.split("."))
			a = h*60+m
		except:
			a = None
		
		try:
			h,m = map(int, self.real_start.split("."))
			b = h*60+m
		except:
			b = None
		try:
			h,m = map(int, self.real_end.split("."))
			c = h*60+m
		except:
			c = None
		
		try:
			h,m = map(int, self.end.split("."))
			d = h*60+m
		except:
			d = None
		
		return a,b,c,d
	def __repr__(self):
		return "%s (%s) - %s (%s)" % ( self.start, self.real_start, self.real_end, self.end )

class Headers(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
	def paintEvent(self, event):
		painter = QPainter(self)
		pen = QPen(QColor("#FF0000"))
		font = QFont()
		font.setBold(False)
		painter.setPen(pen)
		painter.setFont(font)
		for i in range(0,14):
			painter.drawText(i*20, 10, QString(str(i)))
			
class SegmentLine(QWidget):
	def __init__(self, segments, parent=None):
		QWidget.__init__(self, parent)
		#self.segments = segments
		self.slots = [segment.get_slots() for segment in segments]
		
		print self.slots
	def paintEvent(self, event):
		painter = QPainter(self)
		
		for slotgroup in self.slots:
			#print slotgroup
			a,b,c,d = slotgroup
			if a:
				painter.setBrush(QBrush(QColor("#0033FF")))
				rect = (a/3, 0, (b-a)/3, 10)
				print "Drawing presleep:", rect
				painter.drawRect(*rect)
				
			painter.setBrush(QBrush(QColor("#003333")))
			rect = b/3, 0, (c-b)/3, 10
			print "Drawing sleep:", rect
			painter.drawRect(*rect)
			
			
			if d:
				painter.setBrush(QBrush(QColor("#0033FF")))
				rect = c/3, 0, (d-c)/3, 10
				painter.drawRect(*rect)
				print "Drawing postsleep:",rect
				
			
			

class SleepMonitor(QWidget):
	def __init__(self, parent=None):
		QWidget.__init__(self, parent)
		layout = QGridLayout()
		self.setLayout(layout)
		
		
	def read_from_file(self, filename):
		f = open(filename)
		lines = f.readlines()
		for i, line in enumerate(lines):
			day, times = line.split(":")
			segments = map(clr, times.split("&") )
			segs = [Segment(segment) for segment in segments ]
			self.layout().addWidget(QLabel("Saatler"), 0, 0, Qt.AlignRight)
			self.layout().addWidget(Headers(), 0, 1)
			self.layout().addWidget(QLabel(QString(day)), i+1, 0, Qt.AlignRight)
			self.layout().addWidget(SegmentLine(segs), i+1, 1)


def main():
	app = QApplication(sys.argv)
	mainWindow = SleepMonitor() #SegmentLine([Segment("00.00 - 09.00 (10.00)")])# , Segment("11.00 - 15.00")])
	mainWindow.read_from_file("uyku.txt")
	mainWindow.show()
	mainWindow.resize(1024,768)
	sys.exit(app.exec_())
	
if __name__ == "__main__":
	main()