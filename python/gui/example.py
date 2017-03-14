#!/usr/bin/python3

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class MainScreen(QMainWindow):

   def __init__(self):
      QMainWindow.__init__(self)
app = QApplication( sys.argv )
window = MainScreen()
window.show()
sys.exit(app.exec_())
