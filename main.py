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
   
   gui = GUI("b7bf3a5df43989dd97f0fa97ebce2f4a", "603deb1015ca71be2b73aef0857d77811f352c073b6108d72d9810a30914dff4")
   gui.show()
   
   sys.exit(app.exec_())
	
if __name__ == '__main__':
   run()