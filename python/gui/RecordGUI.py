# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'database.ui'
#
# Created: Tue Jun 28 11:13:49 2016
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIntValidator, QDoubleValidator
from PyQt5.QtWidgets import *

class MainScreen(QMainWindow):
   interfaces = {}
   ## @brief Create the initial window
   #
   # This function creates the intial window and 
   def __init__(self):
      self.mainWindow = QMainWindow
      self.mainWindow.__init__(self)

   ## @brief resize the window
   def resize(self, width, height):
      print("Resizing to "+str(width) +":"+str(height))
#      self.mainWindow.resize(QWidget.resize(width, height))


   ## @brief Adds an object of the given value based on the template
   def addObject( self, template, value ):
      print("Adding Object")
      objects = 0
      if( template["type"] == "string"):
         objects = objects + self.addTextBox( template, value )
         return objects
      else:
         print ("Undefined type: "+str(template["type"]))
         return -1

   ## @brief Adds a text box
   #
   def addTextBox( self, template, value ):
      self.interfaces["test"] =QLineEdit(self)
      self.interfaces["test"].move(20,20)
      return 1



#class Ui_Dialog(object):
#    def setupUi(self, Dialog):
#        Dialog.resize(1000, 1000)
#        self.formLayout = QtWidgets.QFormLayout(Dialog)
#        QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#class Ui_Dialog2(object):
#    def setupUi(self, Dialog):
#        Dialog.resize(500, 500)
#        self.formLayout = QtWidgets.QFormLayout(Dialog)
#        QtCore.QMetaObject.connectSlotsByName(Dialog)
#
#class RecordGUI(object):
#
#    edits = list()
#    labels = list()
#    tags = list()
#
#    def setupUi(self, MainWindow):
#        MainWindow.setObjectName("MainWindow")
#        MainWindow.resize(650, 650)
#        self.centralwidget = QtWidgets.QWidget(MainWindow)
#        self.centralwidget.setObjectName("centralwidget")
#        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
#
#        #self.horizontalLayout.addWidget(self.centralwidget)
#
#        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
#        self.tab = QtWidgets.QWidget()
#
#
#        self.record = QtWidgets.QToolButton(self.tab)
#        self.record.setGeometry(QtCore.QRect(120, 360, 61, 51))
#        font = QtGui.QFont()
#        font.setPointSize(20)
#        font.setBold(True)
#        font.setWeight(75)
#        self.record.setFont(font)
#        self.record.setObjectName("record")
#        self.record.setStyleSheet("selection-color: red")
#        self.live = QtWidgets.QPushButton(self.tab)
#        self.live.setGeometry(QtCore.QRect(120, 440, 80, 27))
#        self.live.setText("Live")
#        self.label = QtWidgets.QLabel(self.tab)
#        self.label.setGeometry(QtCore.QRect(190, 380, 66, 17))
#        self.label.setObjectName("label")
#        self.start = QtWidgets.QLabel(self.tab)
#        self.stop = QtWidgets.QLabel(self.tab)
#        self.send = QtWidgets.QPushButton(self.tab)
#        self.send.setGeometry(QtCore.QRect(290, 400, 131, 27))
#        self.send.setObjectName("send")
#        self.error = QtWidgets.QLabel(self.tab)
#        self.error.setGeometry(QtCore.QRect(290, 440, 550, 17))
#        
#        self.tabWidget.addTab(self.tab, "")
#        self.horizontalLayout.addWidget(self.tabWidget)
#        MainWindow.setCentralWidget(self.centralwidget)
#        self.menubar = QtWidgets.QMenuBar(MainWindow)
#        self.menubar.setGeometry(QtCore.QRect(0, 0, 587, 25))
#        self.menubar.setObjectName("menubar")
#        MainWindow.setMenuBar(self.menubar)
#        self.statusbar = QtWidgets.QStatusBar(MainWindow)
#        self.statusbar.setObjectName("statusbar")
#        MainWindow.setStatusBar(self.statusbar)
#        self.pic = QtWidgets.QLabel(self.tab)
#        self.pic.setGeometry(470, 0, 100, 100)
#        self.pixmap = QtGui.QPixmap('q.jpg')
#        self.pixmap = self.pixmap.scaledToHeight(100)
#        self.pic.setPixmap(self.pixmap)
#	
#        self.tab2 = QtWidgets.QWidget() 
#        
#        
#        self.pic2 = QtWidgets.QLabel(self.tab2)
#        self.pic2.setGeometry(470, 0, 100, 100)
#        self.pixmap2 = QtGui.QPixmap('q.jpg')
#        self.pixmap2 = self.pixmap2.scaledToHeight(100)
#        self.pic2.setPixmap(self.pixmap2)
#        self.search = QtWidgets.QPushButton(self.tab2)
#        self.search.setGeometry(QtCore.QRect(200, 400, 130, 27))
#        self.tabWidget.addTab(self.tab2, "")
#
#
#        self.retranslateUi(MainWindow)
#        QtCore.QMetaObject.connectSlotsByName(MainWindow)
#
#    def retranslateUi(self, MainWindow):
#        _translate = QtCore.QCoreApplication.translate
#        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
#        self.record.setText(_translate("MainWindow", "O"))
#        self.label.setText(_translate("MainWindow", "Rec"))
#
#        self.send.setText(_translate("MainWindow", "Send to Database"))
#
#        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Record"))
#        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab2), _translate("MainWindow", "Database"))
#        
#        self.search.setText("Search Database")
