# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:56:38 2020

@author: WarPeace101
"""

from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QLineEdit,QHBoxLayout,QVBoxLayout,QSpacerItem
from AES import AES
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
import GUI

class DecryptWindow(QWidget):
    success_signal = pyqtSignal()
    def __init__(self, ciphertext, key):
        super().__init__()
        self.aes = AES()
        
        self.setStyleSheet("QWidget {background-color:#34495e;}")
        self.ciphertext = ciphertext
        self.key = key
#        self.setFixedSize(350,200)
        
        self.aes.Decrypt(self.ciphertext, self.key)
        
        self.next_round = QPushButton("Next Round")
        self.next_round.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        self.back = QPushButton("Back")
        self.back.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        
        
        self.output = QLabel("Press Next Round to Show Results")
        self.output.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.output.setAlignment(Qt.AlignCenter) 
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.output)
        self.vbox.addItem(QSpacerItem(100,50))
        self.vbox.addWidget(self.next_round)
        self.vbox.addItem(QSpacerItem(100,50))
        self.vbox.addWidget(self.back)
        
      
        
        self.errorMessage = QLabel("")
        self.errorMessage.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.errorMessage.setAlignment(Qt.AlignCenter) 
        self.vbox.addWidget(self.errorMessage)
        self.setLayout(self.vbox)
        
        self.next_round.clicked.connect(lambda:self.decryptrequest())
        self.back.clicked.connect(lambda:self.backB())
        
        
        self.show()
        self.counter = 0
        self.success_signal.connect(lambda:self.cleanUp())
        
    def decryptrequest(self):
        if(self.counter < len(self.aes.decryptrounds)):
            self.output.setText(self.aes.decryptrounds[self.counter])
        else:
            self.errorMessage.setText("This is the final round")
        self.counter += 1
        
        
    def backB(self):
        gui = GUI.GUI(self.ciphertext, self.key)
        self.success_signal.emit()
        
    def cleanUp(self):
        self.close()
        self.deleteLater()   