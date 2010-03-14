#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2007,  Ahmet Emre Aladağ
#
# This program is free software; you can redistribute it and/or modify it under
# the terms of the GNU General Public License as published by the Free
# Software Foundation; either version 2 of the License, or (at your option)
# any later version.
#
# Please read the COPYING file.
#

"""GUI for Main Window"""

from qt import *
from kdecore import KIconLoader,KIcon 
from kdeui import *  #KMessageBox
from kfile import *  #KURLRequester
from about import about #About dialog
import commands #To use xdelta

class Form1(QMainWindow):
    def __init__(self, app, parent = None,name = "kiXdelta",fl = 0,):
        QMainWindow.__init__(self,parent,name,fl)
        self.statusBar()
        self.app = app
        icons = KIconLoader ()
        self.setIcon(icons.loadIcon("kixdelta.png", KIcon.Desktop, 22))
        
        if not name:
            self.setName("Form1")
        
        self.setSizePolicy(QSizePolicy(QSizePolicy.Minimum,QSizePolicy.Minimum,0,0,self.sizePolicy().hasHeightForWidth()))
        self.setMinimumSize(QSize(100,199))
        self.setMaximumSize(QSize(300,300))
        self.setBaseSize(QSize(0,0))

        self.setCentralWidget(QWidget(self,"qt_central_widget"))
        Form1Layout = QHBoxLayout(self.centralWidget(),11,6,"Form1Layout")
        Form1Layout.setResizeMode(QLayout.FreeResize)

        self.toolbox = QToolBox(self.centralWidget(),"toolbox")
        #self.toolbox.setCurrentIndex(0)

        self.page1 = QWidget(self.toolbox,"page1")
        self.page1.setBackgroundMode(QWidget.PaletteBackground)
        page1Layout = QGridLayout(self.page1,1,1,11,6,"page1Layout")

        self.kURLRequester2_2 = KURLRequester(self.page1,"kURLRequester2_2")


        page1Layout.addWidget(self.kURLRequester2_2,1,1)

        self.new_xdelta = QLabel(self.page1,"new_xdelta")

        page1Layout.addWidget(self.new_xdelta,2,0)

        self.kURLRequester2_3 = KURLRequester(self.page1,"kURLRequester2_3")

        page1Layout.addWidget(self.kURLRequester2_3,2,1)

        self.old = QLabel(self.page1,"old")

        page1Layout.addWidget(self.old,0,0)

        self.new = QLabel(self.page1,"new")

        page1Layout.addWidget(self.new,1,0)

        self.kURLRequester2 = KURLRequester(self.page1,"kURLRequester2")

        page1Layout.addWidget(self.kURLRequester2,0,1)

        self.create = QPushButton(self.page1,"create")

        page1Layout.addWidget(self.create,3,1)
        self.toolbox.addItem(self.page1,QString.fromLatin1(""))

        self.page2 = QWidget(self.toolbox,"page2")
        self.page2.setBackgroundMode(QWidget.PaletteBackground)
        page2Layout = QGridLayout(self.page2,1,1,11,6,"page2Layout")

        self.xdelta_file = QLabel(self.page2,"xdelta_file")

        page2Layout.addWidget(self.xdelta_file,0,0)

        self.old_file = QLabel(self.page2,"old_file")

        page2Layout.addWidget(self.old_file,1,0)

        self.new_file = QLabel(self.page2,"new_file")

        page2Layout.addWidget(self.new_file,2,0)

        self.kURLRequester5 = KURLRequester(self.page2,"kURLRequester5")

        page2Layout.addWidget(self.kURLRequester5,0,1)

        self.kURLRequester6 = KURLRequester(self.page2,"kURLRequester6")

        page2Layout.addWidget(self.kURLRequester6,1,1)

        self.kURLRequester7 = KURLRequester(self.page2,"kURLRequester7")

        page2Layout.addWidget(self.kURLRequester7,2,1)

        self.apply_patch = QPushButton(self.page2,"apply_patch")

        page2Layout.addWidget(self.apply_patch,3,1)
        self.toolbox.addItem(self.page2,QString.fromLatin1(""))
        
        self.toolbox.setCurrentIndex(1)

        Form1Layout.addWidget(self.toolbox)

        self.programAboutAction = QAction(self,"programAboutAction")
        self.programExitAction = QAction(self,"programExitAction")
        self.MenuBar = QMenuBar(self,"MenuBar")


        self.Program = QPopupMenu(self)
        self.Program.insertSeparator()
        self.Program.insertSeparator()
        self.programAboutAction.addTo(self.Program)
        self.programExitAction.addTo(self.Program)
        self.MenuBar.insertItem(QString(""),self.Program,1)

        self.MenuBar.insertSeparator(2)


        self.languageChange()

        self.resize(QSize(300,256).expandedTo(self.minimumSizeHint()))
        self.clearWState(Qt.WState_Polished)

        self.connect(self.programExitAction,SIGNAL("activated()"),self.close)
        self.connect(self.programAboutAction,SIGNAL("activated()"),self.showabout)
        self.connect(self.create, SIGNAL("clicked()"),self.fcreate)
        self.connect(self.apply_patch, SIGNAL("clicked()"),self.fapply_patch)
	

        self.setTabOrder(self.kURLRequester2,self.kURLRequester2_2)
        self.setTabOrder(self.kURLRequester2_2,self.kURLRequester2_3)
        self.setTabOrder(self.kURLRequester2_3,self.create)
        self.setTabOrder(self.create,self.kURLRequester5)
        self.setTabOrder(self.kURLRequester5,self.kURLRequester6)
        self.setTabOrder(self.kURLRequester6,self.kURLRequester7)
        self.setTabOrder(self.kURLRequester7,self.apply_patch)


    def languageChange(self):
        self.setCaption(self.__tr("kiXdelta"))
        self.new_xdelta.setText(self.__tr("xdelta File:"))
        self.old.setText(self.__tr("Old File:"))
        self.new.setText(self.__tr("New File:"))
        self.create.setText(self.__tr("&Create xdelta"))
        self.create.setAccel(QKeySequence(self.__tr("Alt+C")))
        self.toolbox.setItemLabel(self.toolbox.indexOf(self.page1),self.__tr("Create xdelta"))
        self.xdelta_file.setText(self.__tr("xdelta File:"))
        self.old_file.setText(self.__tr("Old File:"))
        self.new_file.setText(self.__tr("New File:"))
        self.apply_patch.setText(self.__tr("Apply Patc&h"))
        self.apply_patch.setAccel(QKeySequence(self.__tr("Alt+H")))
        self.toolbox.setItemLabel(self.toolbox.indexOf(self.page2),self.__tr("Apply patch"))
        self.programAboutAction.setText(self.__tr("About"))
        self.programAboutAction.setMenuText(self.__tr("About"))
        self.programExitAction.setText(self.__tr("Exit"))
        self.programExitAction.setMenuText(self.__tr("E&xit"))
        if self.MenuBar.findItem(1):
            self.MenuBar.findItem(1).setText(self.__tr("&Program"))

    #def showabout(self):
     #   w = QtGui.QDialog(self.mainWindow)
      #  about().__init__(w)
       # w.show()

    def showabout(self):
        mDialog = about()
        #mDialog.setModal(true)
        mDialog.show()
        mDialog.exec_loop()
    def fcreate(self): 
	'''function for creating xdelta diff.'''
        import commands
        old_file = self.kURLRequester2.url()
        new_file = self.kURLRequester2_2.url()
        xdelta_file = self.kURLRequester2_3.url()
        com =  "xdelta delta "+old_file+" "+new_file+" "+xdelta_file
        dprint(com)
        self.statusBar().message("Please wait, this process might last too long.")
        print commands.getoutput(str(com))
        self.statusBar().message("")
        #from kdeui import KMessageBox
        KMessageBox.information(self, ("The xdelta of %s and %s\n has been created as %s" % (old_file, new_file, xdelta_file)),"Finished")
        
    def fapply_patch(self):
	'''function for applying an xdelta patch to an existing file.'''
        xdelta_file_p = self.kURLRequester5.url()
        old_file_p = self.kURLRequester6.url()
        new_file_p = self.kURLRequester7.url()        
        com =  "xdelta patch "+xdelta_file_p+" "+old_file_p+" "+new_file_p
        dprint(com)
        self.statusBar().message("Please wait, this process might last too long.")
        print commands.getoutput(str(com))
        self.statusBar().message("")
        KMessageBox.information(self, ("The patch has been applied and new file\n%s has been created" % xdelta_file_p),"Finished")

    def dprint(message):
        debug=1 #FIXME: Make the debug option available with parameter
        if debug==1:
            print message


    def __tr(self,s,c = None):
        return qApp.translate("Form1",s,c)
    
    def closeEvent(self, QCloseEvent):
	 self.deleteLater()
	 #app.quit() 
	 #I can not understand why does this not work? Check out the main file(kixdelta)