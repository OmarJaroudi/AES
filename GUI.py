# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 16:18:56 2020

@author: ojaro
"""
from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QLineEdit,QHBoxLayout,QVBoxLayout,QSpacerItem
from AES import AES
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
import EncryptWindow
import DecryptWindow
from re import search,compile

class GUI(QWidget):
    hexPattern = compile(r"^[0-9A-Fa-f]+$")


    success_signal = pyqtSignal()
    def __init__(self, plaintext, key):
        super().__init__()
       
        
        
        self.aes = AES()
        
        self.setStyleSheet("QWidget {background-color:#34495e;}")
           
        
        self.text = QLineEdit()
        self.text.setPlaceholderText("Plaintext/Ciphertext")
        self.text.setStyleSheet("QLineEdit {color:white;font-size:25px; border:1px solid white;border-radius:5%;}")
        self.text.setText(plaintext)

        self.key = QLineEdit()
        self.key.setStyleSheet("QLineEdit {color:white;font-size:25px; border:1px solid white;border-radius:5%;}")
        
        self.key.setPlaceholderText("Key")
        self.setFixedSize(500,400)
        self.key.setText(key)
        
        self.encrypt = QPushButton("Encrypt")
        self.encrypt.setStyleSheet("QPushButton {text-decoration: none;border: none;padding: 12px 40px;font-size: 16px;background-color: green;color: #fff;border-radius: 5px;box-shadow: 7px 6px 28px 1px rgba(0, 0, 0, 0.24);cursor: pointer;outline: none;transition: 0.2s all;}  QPushButton::pressed{background-color : #006400;}")
        
        self.decrypt = QPushButton("Decrypt")
        self.decrypt.setStyleSheet("QPushButton {              text-decoration: none;              border: none;              padding: 12px 40px;              font-size: 16px;              background-color: #c0392b;              color: #fff;              border-radius: 5px;              box-shadow: 7px 6px 28px 1px rgba(0, 0, 0, 0.24);              cursor: pointer;              outline: none;              transition: 0.2s all;          }QPushButton::pressed{background-color : #8b0000;} ")

        
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
        
        self.setWindowTitle("AES")
        
        
        
        self.success_signal.connect(lambda:self.cleanUp())
        
    def encryptRequest(self):
        plaintext = self.text.text()
        key = self.key.text()
        if plaintext=="" or key =="":
            self.errorMessage.setText("Error empty field(s)!")
        elif len(key)!=32 and len(key)!=48 and len(key)!=64:
            self.errorMessage.setText("Error invalid key size!")
        elif len(plaintext)!=32:
            self.errorMessage.setText("Error invalid text size!")
       
        elif not search(self.hexPattern, plaintext) or not search(self.hexPattern,key):
            self.errorMessage.setText("Error invalid character(s)!")
        else:
            enc = EncryptWindow.EncryptWindow(plaintext, key)
            self.success_signal.emit()
#        self.aes.Encrypt(plaintext,key)
        
        
        
    
    def decryptRequest(self):
        ciphertext = self.text.text()
        key = self.key.text()
        if ciphertext=="" or key =="":
            self.errorMessage.setText("Error empty field(s)!")
        elif len(key)!=32 and len(key)!=48 and len(key)!=64:
            self.errorMessage.setText("Error invalid key size!")
        elif len(ciphertext)!=32:
            self.errorMessage.setText("Error invalid text size!")
        elif not search(self.hexPattern, ciphertext) or not search(self.hexPattern,key):
            self.errorMessage.setText("Error invalid character(s)!")
        else:
            dec = DecryptWindow.DecryptWindow(ciphertext, key)
            self.success_signal.emit()
#        self.errorMessage.setText(self.aes.Decrypt(ciphertext,key))
        
        
        
    def cleanUp(self):
        self.close()
        self.deleteLater()   
