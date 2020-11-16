# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:42:57 2020

@author: WarPeace101
"""

from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QSpacerItem, QPlainTextEdit, QTextEdit 
from AES import AES
from PyQt5.QtCore import Qt
import GUI
from PyQt5.QtCore import pyqtSignal


class EncryptWindow(QWidget):
    success_signal = pyqtSignal()
    def __init__(self, plaintext, key):
        super().__init__()
        self.aes = AES()
        self.plaintext = plaintext
        self.key = key
        self.setStyleSheet("QWidget {background-color:#34495e;}")
    
        self.aes.Encrypt(plaintext,key)
            
        self.setFixedSize(600,600)
        
        self.RoundOutputs = QLabel("")
        self.RoundOutputs.setStyleSheet("QLabel {color:white;font-size:15px;}")
        
        
        self.next_round = QPushButton("Next Round")
        self.next_round.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        self.back = QPushButton("Back")
        self.back.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        
        
        self.output = QTextEdit("Press Next Round to Show Results")
        self.output.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
#        self.output.setAlignment(Qt.AlignCenter) 
        
        
#        self.scrollArea.setWidget(self.output)
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.output)
        self.hbox.addWidget(self.RoundOutputs)
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
#        self.vbox.addWidget(self.output)
        self.vbox.addItem(QSpacerItem(100,50))
        self.vbox.addWidget(self.next_round)
        self.vbox.addItem(QSpacerItem(100,50))
        self.vbox.addWidget(self.back)
        
        self.counter = 0
        
        self.errorMessage = QLabel("")
        self.errorMessage.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.errorMessage.setAlignment(Qt.AlignCenter) 
        self.vbox.addWidget(self.errorMessage)
        self.setLayout(self.vbox)
        
        self.next_round.clicked.connect(lambda:self.encryptRequest())
        
        self.back.clicked.connect(lambda:self.backB())
        
        self.show()
        
        self.success_signal.connect(lambda:self.cleanUp())
        
    def encryptRequest(self):
        
        if(self.counter == 0):
            self.RoundOutputs.setText("Round Outputs: \n")
        if(self.counter < len(self.aes.encryptrounds)):
            self.output.setText("Round " + str(self.counter) + ": \n" + self.aes.encryptrounds[self.counter])
            self.RoundOutputs.setText(self.RoundOutputs.text() + str(self.aes.encOutput[self.counter] + "\n"))
            
        else:
            self.errorMessage.setText("This is the final round")
        self.counter += 1
        self.repaint()
        self.resize(self.minimumSizeHint())
        
        
    def backB(self):
        gui = GUI.GUI(self.plaintext, self.key)
        self.success_signal.emit()
        
    def cleanUp(self):
        self.close()
        self.deleteLater()   
