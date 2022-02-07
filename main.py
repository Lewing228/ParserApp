import sys
import os
import csv
import tkinter as tk
from tkinter import ttk
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *

from Сайты.Sulpak import ThreadS
from Сайты.Mechta import ThreadM

from pickle import TRUE



class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(700, 700)
        font = QtGui.QFont()
        font.setPointSize(1)
        Form.setFont(font)
        Form.setLayoutDirection(QtCore.Qt.LeftToRight)
        Form.setStyleSheet("background: rgb(112, 112, 112);")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(200, 400, 300, 61))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("    QPushButton{\n"
"\n"
"background: rgb(61,181,233);\n"
"    height: 50px;\n"
"    border-radius: 10px;\n"
"    text-align: center;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QPushButton:hover{\n"
"background: rgb(52, 148, 189)\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.lineEdit = QtWidgets.QLineEdit(Form)
        self.lineEdit.setGeometry(QtCore.QRect(180, 320, 340, 50))
        self.lineEdit.setStyleSheet("    QLineEdit{\n"
"    border-radius: 10px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"    background: white;\n"
"}\n"
"\n"
"    QLineEdit:hover {\n"
"    border: 3px solid rgb(61,181,233);\n"
"    }")
        self.lineEdit.setInputMask("")
        self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(Form)
        self.lineEdit_2.setGeometry(QtCore.QRect(180, 240, 340, 50))
        self.lineEdit_2.setStyleSheet("    QLineEdit{\n"
"    border-radius: 10px;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"    background: white;\n"
"}\n"
"\n"
"    QLineEdit:hover {\n"
"    border: 3px solid rgb(61,181,233);\n"
"    }")
        self.lineEdit_2.setInputMask("")
        self.lineEdit_2.setAlignment(QtCore.Qt.AlignCenter)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(175, 130, 350, 60))
        font = QtGui.QFont()
        font.setPointSize(1)
        font.setBold(True)
        font.setWeight(75)
        self.comboBox.setFont(font)
        self.comboBox.setMouseTracking(False)
        self.comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setStyleSheet("QComboBox{\n"
"    border-radius: 30px;\n"
"    padding-left: 140px;\n"
"    background:rgb(56, 56, 56);\n"
"    border-bottom: 5px solid rgb(89, 133, 255);\n"
"    font-size: 20px;\n"
"    color: #fff;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    text-align: center;\n"
"    border-radius: 20px;\n"
"    background-color:rgb(56, 56, 56);\n"
"    color: white;\n"
"}\n"
"\n"
"QComboBox::drop-down {\n"
"    width: 25px;\n"
"    height: 25px;\n"
"    top: 15px;\n"
"    right: 15px;\n"
"}")
        self.comboBox.setInputMethodHints(QtCore.Qt.ImhNone)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")

        self.widget = QtWidgets.QTextEdit(Form)
 
        self.widget.setGeometry(QtCore.QRect(150, 499, 400, 151))
        font = QtGui.QFont()
        font.setPointSize(12)                                         
        self.widget.setFont(font)
        self.widget.setStyleSheet("background: #fff;\n"
"color: black;")
        self.widget.setObjectName("widget")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.pushButton.setText(_translate("Form", "Начать"))
        self.lineEdit.setPlaceholderText(_translate("Form", "Введите URL каталога"))
        self.lineEdit_2.setPlaceholderText(_translate("Form", "Введите название файла"))
        self.comboBox.setCurrentText(_translate("Form", "Sulpak"))
        self.comboBox.setItemText(0, _translate("Form", "Sulpak"))
        self.comboBox.setItemText(1, _translate("Form", "Мечта"))



class MainWindow(QtWidgets.QWidget, Ui_Form):
    HEADERS = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'accept' : '*/*'
    }
    
    def __init__(self):
        super().__init__()   
        self.setupUi(self)
        
        self.pushButton.clicked.connect(self.btn)
        self.comboBox.currentTextChanged.connect(self.on_combobox_changed)
        self.lineEdit_2.setText(''  + '.csv')

    def on_combobox_changed(self, index):
        index = self.comboBox.currentIndex()
        print (index)

        self.url = self.lineEdit.text()
        self.file = self.lineEdit_2.text()

        if index == 0:
            self.thread = ThreadS(self.url, self.file, self.HEADERS)
        elif index == 1:
            self.thread = ThreadM(self.url, self.file, self.HEADERS)


    def btn(self):
        if not self.lineEdit.text() or not self.lineEdit_2.text():
            msg = QMessageBox.information(self, 'Внимание', 'Заполните поля ввода.')
            return
        
        
        self.pushButton.setEnabled(False)
 
        self.thread.stepChanged.connect(self.onStepChanged)
        self.thread.finished.connect(self.save_file)
        self.thread.error.connect(self.error)
        
        self.thread.start()  

    def error(self, error):
        self.widget.append(error) 
        msg = QMessageBox.information(self, 'Error', error)
        self.pushButton.setEnabled(True)
        
    def onStepChanged(self, page, pages_count):
        self.widget.append(f'Парсинг страницы {page} из {pages_count}...')    

    def save_file(self, items):
        with open(self.file, 'w', newline='') as file:
            writer = csv.writer(file, delimiter=';')
            writer.writerow(['Модель', 'Цена', 'Цена без скидки'])
            for item in items:
                writer.writerow([item['title'], item['price'], item['old price']])
                
        self.widget.append(f'Получено {len(items)} товаров')
        self.pushButton.setEnabled(True)
        os.startfile(self.file)            
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())     