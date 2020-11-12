# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:18:56 2020

@author: ojaro
"""
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QLineEdit,QHBoxLayout,QVBoxLayout,QSpacerItem
from AES import AES
from PyQt5.QtCore import Qt

class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.aes = AES()
        
        self.setStyleSheet("QWidget {background-color:#34495e;}")
        
        self.text = QLineEdit()
        self.text.setPlaceholderText("Plaintext/Ciphertext")
        self.text.setStyleSheet("QLineEdit {color:white;font-size:25px;}")

        self.key = QLineEdit()
        self.key.setStyleSheet("QLineEdit {color:white;font-size:25px;}")
        
        self.key.setPlaceholderText("Key")
        self.setFixedSize(500,400)
        
        self.encrypt = QPushButton("Encrypt")
        self.encrypt.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        
        
        self.decrypt = QPushButton("Decrypt")
        self.decrypt.setStyleSheet("QPushButton {background-color: #c0392b;font-size:20px;}")

        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.encrypt)
        self.hbox.addItem(QSpacerItem(20,5))
        self.hbox.addWidget(self.decrypt)
        

        self.vbox = QVBoxLayout()
        self.vbox.addItem(QSpacerItem(100,50))

        self.vbox.addWidget(self.text)
        self.vbox.addItem(QSpacerItem(100,50))

        self.vbox.addWidget(self.key)
        self.vbox.addItem(QSpacerItem(100,50))

        self.vbox.addItem(self.hbox)

        
        self.errorMessage = QLabel("")
        self.errorMessage.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.errorMessage.setAlignment(Qt.AlignCenter) 
        self.vbox.addWidget(self.errorMessage)
        self.setLayout(self.vbox)
        
        self.encrypt.clicked.connect(lambda:self.encryptRequest())
        self.decrypt.clicked.connect(lambda:self.decryptRequest())
        
        self.show()
        
    def encryptRequest(self):
        plaintext = self.text.text()
        key = self.key.text()
        if plaintext=="" or key =="":
            self.errorMessage.setText("Error empty field(s)!")
        self.aes.Encrypt(plaintext,key)
    
    def decryptRequest(self):
        ciphertext = self.text.text()
        key = self.key.text()
        if ciphertext=="" or key =="":
            self.errorMessage.setText("Error empty field(s)!")
        self.errorMessage.setText(self.aes.Decrypt(ciphertext,key))
        
        
        
