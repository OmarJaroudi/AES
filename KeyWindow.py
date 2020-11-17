# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 12:29:10 2020

@author: WarPeace101
"""

from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout,QVBoxLayout,QSpacerItem, QTextEdit
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal


class KeyWindow(QWidget):
    success_signal = pyqtSignal()
    def __init__(self, keyExpansion, keyoutput):
        super().__init__()
        
        self.keyExpansion = keyExpansion
        self.keyOUTPUT = keyoutput
        
        self.setStyleSheet("QWidget {background-color:#34495e;}")
    
        self.setFixedSize(600,600)
        
        self.RoundOutputs = QLabel("")
        self.RoundOutputs.setStyleSheet("QLabel {color:white;font-size:15px;}")
        
        
        self.next_round = QPushButton("Next Word")
        self.next_round.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
           
        self.output = QTextEdit("Press Next Round to Show Results")
        self.output.setStyleSheet("QTextEdit {color:white;font-size:15px;}")

        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.output)
        self.hbox.addWidget(self.RoundOutputs)
        
        self.vbox = QVBoxLayout()
        self.vbox.addLayout(self.hbox)
#        self.vbox.addWidget(self.output)
        self.vbox.addItem(QSpacerItem(100,50))
        self.vbox.addWidget(self.next_round)
        self.vbox.addItem(QSpacerItem(100,50))
        
        
        self.counter = 0
        
        self.errorMessage = QLabel("")
        self.errorMessage.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.errorMessage.setAlignment(Qt.AlignCenter) 
        self.vbox.addWidget(self.errorMessage)
        self.setLayout(self.vbox)
        
        self.next_round.clicked.connect(lambda:self.encryptRequest())
        
        
        self.success_signal.connect(lambda:self.cleanUp())
        self.show()
        
    def cleanUp(self):
        self.close()
        self.deleteLater() 