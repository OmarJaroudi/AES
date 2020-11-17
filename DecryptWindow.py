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


class DecryptWindow(QWidget):
    success_signal = pyqtSignal()
    
    def __init__(self, ciphertext, key):
        super().__init__()
        
        
        
        self.aes = AES()
        self.ciphertext = ciphertext
        self.key = key
        self.setStyleSheet("QWidget {background-color:#34495e;}")
    
        self.aes.Decrypt(ciphertext,key)
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
#        self.next_round = QPushButton("Next Round")
#        self.next_round.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")       
        self.output = QTextEdit("Press Next Round to Show AES Results")
        self.output.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.output)
        self.hbox.addWidget(self.RoundOutputs)
#        self.vbox = QVBoxLayout()
#        self.vbox.addItem(QSpacerItem(100,50))
##        self.vbox.addWidget(self.next_round)
#        self.vbox.addItem(QSpacerItem(100,50))
        
        
        #KEY EXPANSION STEPS HERE
        self.keyOutput = QTextEdit("")
        self.keyOutput.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
#        self.next_word = QPushButton("Next Word")
#        self.next_word.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
#        self.skip = QPushButton("Next 3 words")
#        self.skip.setStyleSheet("QPushButton {background-color: #1abc9c;font-size:20px;}")
        self.keyexp = QTextEdit("Press Next Round to Show Key Results")
        self.keyexp.setStyleSheet("QTextEdit {color:white;font-size:15px;}")
        self.hboxkey = QHBoxLayout()
        self.hboxkey.addWidget(self.keyexp)
        self.hboxkey.addWidget(self.keyOutput)
#        self.vboxkey = QVBoxLayout()
#        self.vboxkey.addItem(QSpacerItem(100,50))
#        self.vboxkey.addWidget(self.next_word)
#        self.vboxkey.addWidget(self.skip)
#        self.vboxkey.addItem(QSpacerItem(100,50))
        
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
#        self.masterHBOX.addLayout(self.vbox)
#        self.masterHBOX.addLayout(self.vboxkey)
        self.masterVBOX.addLayout(self.labelhbox)
        self.masterVBOX.addLayout(self.outputHbox)
        self.masterVBOX.addLayout(self.masterHBOX)
        
        self.next = QPushButton("Next Word")
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
        
#        self.next_round.clicked.connect(lambda:self.encryptRequest())
        
        self.back.clicked.connect(lambda:self.backB())
        
        self.next.clicked.connect(lambda: self.decryptrequest())
        
#        self.next_word.clicked.connect(lambda: self.NextWord())
#        self.skip.clicked.connect(lambda: self.NextThreeWords())
        
        self.show()
        
        self.setWindowTitle("AES Encryption")
        
        
        
        self.success_signal.connect(lambda:self.cleanUp())
        
    def decryptrequest(self):
        
        if(self.counter < len(self.aes.decryptrounds)):
            self.aesRounds.setText("Round " + str(self.counter + 1) + ": ")
            self.output.setText(self.aes.decryptrounds[self.counter])
            self.RoundOutputs.setText(self.RoundOutputs.toPlainText() + str(self.aes.decOutput[self.counter] + "\n"))
            
        else:
            self.errorMessage.setText("This is the final round")
        self.counter += 1
        words = "Words: "
        wordsexp = ""
        if(self.counterkey  +3 < len(self.aes.keySteps)):
            self.aeskeyexp.setText("")
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
        
        
    def NextWord(self):

        if(self.counterkey < len(self.aes.keySteps)):
            self.aeskeyexp.setText("Word " + str(self.counterkey + 3) + ": ")
            self.keyexp.setText(self.aes.keySteps[self.counterkey])
            self.keyOutput.setText(self.keyOutput.toPlainText() + str(self.aes.keyOutput[self.counterkey] + "\n"))
        else:
            self.errorMessage.setText("End of word expansion")
        
        
        
        
        self.counterkey += 1
        self.repaint()
        self.resize(self.minimumSizeHint())
    
    def NextThreeWords(self):
    
        wordsexp = ""
        if(self.counterkey + 3 < len(self.aes.keySteps)):
            self.aeskeyexp.setText("")
            for i in range(3):
                self.aeskeyexp.setText(self.aeskeyexp.text() + "Word " + str(self.counterkey + 3) + ", ")
                wordsexp += self.aes.keySteps[self.counterkey] + "\n\n"
                self.keyOutput.setText(self.keyOutput.toPlainText() + str(self.aes.keyOutput[self.counterkey] + "\n"))
                self.counterkey += 1
            self.keyexp.setText(wordsexp)
        else:
            self.errorMessage.setText("Out of bounds for 3 words")
            
    def backB(self):
        gui = GUI.GUI(self.ciphertext, self.key)
        self.success_signal.emit()
        
    def cleanUp(self):
        self.close()
        self.deleteLater()   
