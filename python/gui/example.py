#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidget import *


class MainScreen(QMainWindow):

   def __init__(self):
      QMainWindow.__init__(self)

app = QApplication( sys.argv )

template = {"type":"string", "value":"test"}
window = MainScreen()
print("Adding Object")
window.addObject(template, "test")
window.show()
sys.exit(app.exec_())
