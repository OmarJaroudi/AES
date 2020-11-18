# -*- coding: utf-8 -*-
"""
Created on Mon Nov 16 10:42:57 2020

@author: WarPeace101
"""

from PyQt5.QtWidgets import QWidget,QLabel,QPushButton,QHBoxLayout,QVBoxLayout, QTextEdit 
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
        self.setFixedSize(1200,600)
        
        self.masterVBOX = QVBoxLayout()
        
        self.aesRounds = QLabel("Round :")
        self.aesRounds.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.aesOutput = QLabel("Rounds Output: ")
        self.aesOutput.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.aeskeyexp = QLabel("Words: ")
        self.aeskeyexp.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.aeskeyoutput = QLabel("Words Output:")
        self.aeskeyoutput.setStyleSheet("QLabel {color:white;font-size:15px;}")
        
        #AES STEPS HERE
        self.RoundOutputs = QTextEdit("")
        self.RoundOutputs.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.RoundOutputs.setReadOnly(True)
       
        self.output = QTextEdit("Press Next Round to Show AES Results")
        self.output.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.output.setReadOnly(True)
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.output)
        self.hbox.addWidget(self.RoundOutputs)

        
        
        #KEY EXPANSION STEPS HERE
        self.keyOutput = QTextEdit("")
        self.keyOutput.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.keyOutput.setReadOnly(True)

        self.keyexp = QTextEdit("Press Next Round to Show Key Results")
        self.keyexp.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.keyexp.setReadOnly(True)
        self.hboxkey = QHBoxLayout()
        self.hboxkey.addWidget(self.keyexp)
        self.hboxkey.addWidget(self.keyOutput)

        
        #LABELS
        self.labelhbox = QHBoxLayout()
        self.labelhbox.addWidget(self.aesRounds)
        self.labelhbox.addWidget(self.aesOutput)
        self.labelhbox.addWidget(self.aeskeyexp)
        self.labelhbox.addWidget(self.aeskeyoutput)
        
        #MASTER BOXES
        self.outputHbox = QHBoxLayout()
        self.outputHbox.addLayout(self.hbox)
        self.outputHbox.addLayout(self.hboxkey)
        self.masterHBOX = QHBoxLayout()

        self.masterVBOX.addLayout(self.labelhbox)
        self.masterVBOX.addLayout(self.outputHbox)
        self.masterVBOX.addLayout(self.masterHBOX)
        
        self.next = QPushButton("Next")
        self.next.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        
        self.back = QPushButton("Back")
        self.back.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
      
        self.masterVBOX.addWidget(self.next)
        self.masterVBOX.addWidget(self.back)
        
        self.counter = 0    
        self.counterkey = 0
        self.errorMessage = QLabel("")
        self.errorMessage.setStyleSheet("QLabel {color:white;font-size:15px;}")
        self.errorMessage.setAlignment(Qt.AlignCenter) 
        self.masterVBOX.addWidget(self.errorMessage)
        self.setLayout(self.masterVBOX)
        

        
        self.back.clicked.connect(lambda:self.backB())
        
        self.next.clicked.connect(lambda: self.encryptRequest())

        
        self.show()
        
        self.setWindowTitle("AES Encryption")
        
        
        
        self.success_signal.connect(lambda:self.cleanUp())
        
    def encryptRequest(self):
        
        if(self.counter < len(self.aes.encryptrounds)):
            self.aesRounds.setText("Round " + str(self.counter + 1) + ": ")
            self.output.setText(self.aes.encryptrounds[self.counter])
            self.RoundOutputs.setText(self.RoundOutputs.toPlainText() + str(self.aes.encOutput[self.counter] + "\n"))
            
        else:
            self.errorMessage.setText("This is the final round")
        self.counter += 1
        words = "Words: "
        wordsexp = ""
        if(self.counterkey  +3 < len(self.aes.keySteps)):
            self.aeskeyexp.setText("Words: ")
            if(self.counterkey == 0):
                for i in range(8):
                    words +=  str(self.counterkey+1) + " / "
                    wordsexp += self.aes.keySteps[self.counterkey] + "\n\n"
                    self.keyOutput.setText(self.keyOutput.toPlainText() + str(self.aes.keyOutput[self.counterkey] + "\n"))
                    self.counterkey += 1
                self.aeskeyexp.setText(words)
                self.keyexp.setText(wordsexp)
            else:
                for i in range(4):
                    words +=  str(self.counterkey+1) + " / "
                    wordsexp += self.aes.keySteps[self.counterkey] + "\n\n"
                    self.keyOutput.setText(self.keyOutput.toPlainText() + str(self.aes.keyOutput[self.counterkey] + "\n"))
                    self.counterkey += 1
                self.aeskeyexp.setText(words)
                self.keyexp.setText(wordsexp)
        
        
        
        self.repaint()
        self.resize(self.minimumSizeHint())
        

            
    def backB(self):
        gui = GUI.GUI(self.plaintext, self.key)
        self.success_signal.emit()
        
    def cleanUp(self):
        self.close()
        self.deleteLater()   
