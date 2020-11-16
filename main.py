# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:20:00 2020

@author: ojaro
"""
import sys
from PyQt5.QtWidgets import QApplication
from GUI import GUI

def run():
   app = QApplication(sys.argv)
   gui = GUI("", "")
   gui.show()
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   run()