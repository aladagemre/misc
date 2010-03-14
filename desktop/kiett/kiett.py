# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'kiett.ui'
#
# Created: Tue Apr 29 23:39:22 2008
#      by: PyQt4 UI code generator 4.3-snapshot-20071219
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from iett import *
import sys

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,490,425).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setObjectName("gridlayout")

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName("vboxlayout")

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName("hboxlayout")

        self.comboBox = QtGui.QComboBox(self.centralwidget)
        self.comboBox.setObjectName("comboBox")
        self.hboxlayout.addWidget(self.comboBox)

        self.pushButton = QtGui.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.hboxlayout.addWidget(self.pushButton)
        self.vboxlayout.addLayout(self.hboxlayout)

        self.tableWidget = QtGui.QTableWidget(self.centralwidget)
        self.tableWidget.setObjectName("tableWidget")
        self.vboxlayout.addWidget(self.tableWidget)
        self.gridlayout.addLayout(self.vboxlayout,0,0,1,1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,490,29))
        self.menubar.setObjectName("menubar")

        self.menuAyarlar = QtGui.QMenu(self.menubar)
        self.menuAyarlar.setObjectName("menuAyarlar")

        self.menu_lemler = QtGui.QMenu(self.menubar)
        self.menu_lemler.setObjectName("menu_lemler")

        self.menuTabloyu_Kaydet = QtGui.QMenu(self.menu_lemler)
        self.menuTabloyu_Kaydet.setObjectName("menuTabloyu_Kaydet")

        self.menuYard_m = QtGui.QMenu(self.menubar)
        self.menuYard_m.setObjectName("menuYard_m")

        self.menuS_k_Kullan_lanlar = QtGui.QMenu(self.menubar)
        self.menuS_k_Kullan_lanlar.setObjectName("menuS_k_Kullan_lanlar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionS_k_Sorulan_Sorular = QtGui.QAction(MainWindow)
        self.actionS_k_Sorulan_Sorular.setObjectName("actionS_k_Sorulan_Sorular")

        self.actionDestek = QtGui.QAction(MainWindow)
        self.actionDestek.setObjectName("actionDestek")

        self.actionHakk_nda = QtGui.QAction(MainWindow)
        self.actionHakk_nda.setObjectName("actionHakk_nda")

        self.actionHTML_olarak = QtGui.QAction(MainWindow)
        self.actionHTML_olarak.setObjectName("actionHTML_olarak")

        self.actionPDF_olarak = QtGui.QAction(MainWindow)
        self.actionPDF_olarak.setObjectName("actionPDF_olarak")

        self.actionS_k_Kullan_lanlara_Ekle = QtGui.QAction(MainWindow)
        self.actionS_k_Kullan_lanlara_Ekle.setObjectName("actionS_k_Kullan_lanlara_Ekle")

        self.action122M = QtGui.QAction(MainWindow)
        self.action122M.setObjectName("action122M")

        self.actionTercihler = QtGui.QAction(MainWindow)
        self.actionTercihler.setObjectName("actionTercihler")
        self.menuAyarlar.addAction(self.actionTercihler)
        self.menuTabloyu_Kaydet.addAction(self.actionHTML_olarak)
        self.menuTabloyu_Kaydet.addAction(self.actionPDF_olarak)
        self.menu_lemler.addAction(self.menuTabloyu_Kaydet.menuAction())
        self.menu_lemler.addAction(self.actionS_k_Kullan_lanlara_Ekle)
        self.menuYard_m.addAction(self.actionS_k_Sorulan_Sorular)
        self.menuYard_m.addAction(self.actionDestek)
        self.menuYard_m.addAction(self.actionHakk_nda)
        self.menuS_k_Kullan_lanlar.addAction(self.action122M)
        self.menubar.addAction(self.menuAyarlar.menuAction())
        self.menubar.addAction(self.menu_lemler.menuAction())
        self.menubar.addAction(self.menuS_k_Kullan_lanlar.menuAction())
        self.menubar.addAction(self.menuYard_m.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pushButton,QtCore.SIGNAL("clicked()"),self.bul)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    def bul(self):
        self.tableWidget.clear()
        hat = Hat(str(self.comboBox.currentText()))        
        hA = hat.merkezA()
        hB = hat.merkezB()
        liste = hat.tumListe()
        self.tableWidget.setColumnCount(6)
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("H.ICI-"+hA)
        self.tableWidget.setHorizontalHeaderItem(0,headerItem)
        
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("H.ICI-"+hB)
        self.tableWidget.setHorizontalHeaderItem(1,headerItem)
        
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("CMT-"+hA)
        self.tableWidget.setHorizontalHeaderItem(2,headerItem)
        
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("CMT-"+hB)
        self.tableWidget.setHorizontalHeaderItem(3,headerItem)        

        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("PAZ-"+hA)
        self.tableWidget.setHorizontalHeaderItem(4,headerItem)
        
        headerItem = QtGui.QTableWidgetItem()
        headerItem.setText("PAZ-"+hB)
        self.tableWidget.setHorizontalHeaderItem(5,headerItem)        
        print liste
        print hat.satirSayisi()
        for i in range(hat.satirSayisi()):
            self.tableWidget.insertRow(i)
            self.tableWidget.setItem(i, 0,  QtGui.QTableWidgetItem(liste[0][i]))
            self.tableWidget.setItem(i, 1,  QtGui.QTableWidgetItem(liste[1][i]))
            self.tableWidget.setItem(i, 2,  QtGui.QTableWidgetItem(liste[2][i]))
            self.tableWidget.setItem(i, 3,  QtGui.QTableWidgetItem(liste[3][i]))
            self.tableWidget.setItem(i, 4,  QtGui.QTableWidgetItem(liste[4][i]))
            self.tableWidget.setItem(i, 5,  QtGui.QTableWidgetItem(liste[5][i]))
            
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "KIETT", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "20D", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "122M", None, QtGui.QApplication.UnicodeUTF8))
        self.comboBox.addItem(QtGui.QApplication.translate("MainWindow", "9A", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("MainWindow", "Bul", None, QtGui.QApplication.UnicodeUTF8))
        self.tableWidget.clear()
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.menuAyarlar.setTitle(QtGui.QApplication.translate("MainWindow", "Ayarlar", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_lemler.setTitle(QtGui.QApplication.translate("MainWindow", "İşlemler", None, QtGui.QApplication.UnicodeUTF8))
        self.menuTabloyu_Kaydet.setTitle(QtGui.QApplication.translate("MainWindow", "Tabloyu Kaydet", None, QtGui.QApplication.UnicodeUTF8))
        self.menuYard_m.setTitle(QtGui.QApplication.translate("MainWindow", "Yardım", None, QtGui.QApplication.UnicodeUTF8))
        self.menuS_k_Kullan_lanlar.setTitle(QtGui.QApplication.translate("MainWindow", "Sık Kullanılanlar", None, QtGui.QApplication.UnicodeUTF8))
        self.actionS_k_Sorulan_Sorular.setText(QtGui.QApplication.translate("MainWindow", "Sık Sorulan Sorular", None, QtGui.QApplication.UnicodeUTF8))
        self.actionDestek.setText(QtGui.QApplication.translate("MainWindow", "Destek", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHakk_nda.setText(QtGui.QApplication.translate("MainWindow", "Hakkında", None, QtGui.QApplication.UnicodeUTF8))
        self.actionHTML_olarak.setText(QtGui.QApplication.translate("MainWindow", "HTML olarak", None, QtGui.QApplication.UnicodeUTF8))
        self.actionPDF_olarak.setText(QtGui.QApplication.translate("MainWindow", "PDF olarak", None, QtGui.QApplication.UnicodeUTF8))
        self.actionS_k_Kullan_lanlara_Ekle.setText(QtGui.QApplication.translate("MainWindow", "Sık Kullanılanlara Ekle", None, QtGui.QApplication.UnicodeUTF8))
        self.action122M.setText(QtGui.QApplication.translate("MainWindow", "122M", None, QtGui.QApplication.UnicodeUTF8))
        self.actionTercihler.setText(QtGui.QApplication.translate("MainWindow", "Tercihler", None, QtGui.QApplication.UnicodeUTF8))


app = QtGui.QApplication(sys.argv)
window = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(window)

window.show()
sys.exit(app.exec_())
