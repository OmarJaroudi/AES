# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:18:56 2020

@author: ojaro
"""
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QLineEdit,QHBoxLayout,QVBoxLayout
from AES import AES


class GUI(QWidget):
    def __init__(self):
        super().__init__()
        self.aes = AES()

        self.setStyleSheet(r"styling/styling.css")
        
        self.text = QLineEdit()
        self.text.setPlaceholderText("Plaintext/Ciphertext")
        
        self.key = QLineEdit()
        self.key.setPlaceholderText("Key")
        
        self.encrypt = QPushButton("Encrypt")
        self.decrypt = QPushButton("Decrypt")
        
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.encrypt)
        self.hbox.addWidget(self.decrypt)
        
        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.key)
        self.vbox.addItem(self.hbox)
        
        self.errorMessage = QLabel("")
        self.setLayout(self.vbox)
        
        self.encrypt.clicked.connect(lambda:self.encryptRequest())
        self.decrypt.clicked.connect(lambda:self.decryptRequest())
        
        self.show()
        
    def encryptRequest(self):
        plaintext = self.text.text()
        key = self.key.text()
        self.aes.Encrypt(plaintext,key)
    
    def decryptRequest(self):
        ciphertext = self.text.text()
        key = self.key.text()
        self.errorMessage.setText(self.aes.Decrypt(ciphertext,key))
        
        
        
