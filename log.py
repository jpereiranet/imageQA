# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets

class log_Dialog(object):

    def __init__(self, error):
        self.error = error

    def setupUi(self, Dialog):

        Dialog.setObjectName("Dialog")
        Dialog.resize(420, 342)

        font = QtGui.QFont()
        font.setPointSize(12)
        colorFuente = "color: rgb(10, 10, 10)"

        self.label = QtGui.QLabel(Dialog)
        self.label.setFont(font)
        self.label.setStyleSheet(colorFuente)
        self.label.setGeometry(QtCore.QRect(10, 60, 401, 221))
        self.label.setObjectName("error")
        self.label.setWordWrap(True);
        self.label.setStyleSheet("background-color: white")
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)


        self.label2 = QtGui.QLabel(Dialog)
        self.label2.setFont(font)
        self.label2.setStyleSheet(colorFuente)
        self.label2.setGeometry(QtCore.QRect(160, 300, 241, 16))
        self.label2.setObjectName("info")


        self.label3 = QtGui.QLabel(Dialog)
        self.label3.setFont(font)
        self.label3.setStyleSheet(colorFuente)
        self.label3.setGeometry(QtCore.QRect(10, 10, 401, 41))
        self.label3.setObjectName("info2")
        self.label3.setWordWrap(True);
        self.label3.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.label3.setFont(font)
        self.label3.setStyleSheet(colorFuente)

        self.Copy_Button = QtWidgets.QToolButton(Dialog)
        self.Copy_Button.setGeometry(QtCore.QRect(10, 300, 61, 22))
        self.Copy_Button.setObjectName("Copy_Button")
        self.Copy_Button.clicked.connect(self.addToClipBoard)

        self.Close_Button = QtWidgets.QToolButton(Dialog)
        self.Close_Button.setGeometry(QtCore.QRect(80, 300, 61, 22))
        self.Close_Button.setObjectName("Close_Button")
        self.Close_Button.clicked.connect(Dialog.close)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Error Window"))
        self.Copy_Button.setText(_translate("Dialog", "Copiar"))
        self.Close_Button.setText(_translate("Dialog", "Cerrar"))

        self.label3.setText("Oops! We have a bug, copy it and send it to info@jpereira.net, to try to solve it!")
        self.label.setText(self.error)

    def addToClipBoard(self):
        cb = QtGui.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.error, mode=cb.Clipboard)
        self.label2.setText("Copied to clipboard ")



