# -*- coding: utf-8 -*-
import os

from PyQt5 import QtCore, QtWidgets

from license import LicenseClass
from plist_set import ProcessSettingsClass
from warning_class import AppWarningsClass

try:
    _fromUtf8 = QtWidgets.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class ConfigUI(object):

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setFixedSize(403, 198)
        Dialog.setWindowTitle(_translate("Dialog", "Settings", None))

        self.lineEditUser = QtWidgets.QLineEdit(Dialog)
        self.lineEditUser.setGeometry(QtCore.QRect(10, 40, 141, 21))
        self.lineEditUser.setObjectName(_fromUtf8("lineEditUser"))
        self.lineEditUser.setFocusPolicy(QtCore.Qt.StrongFocus)

        self.labelUser = QtWidgets.QLabel(Dialog)
        self.labelUser.setGeometry(QtCore.QRect(10, 20, 111, 16))
        self.labelUser.setObjectName(_fromUtf8("labelUser"))
        self.labelUser.setText(_translate("Dialog", "User", None))

        self.lineEditKey = QtWidgets.QLineEdit(Dialog)
        self.lineEditKey.setGeometry(QtCore.QRect(160, 40, 171, 21))
        self.lineEditKey.setObjectName(_fromUtf8("lineEditKey"))

        self.labelKey = QtWidgets.QLabel(Dialog)
        self.labelKey.setGeometry(QtCore.QRect(160, 20, 111, 16))
        self.labelKey.setObjectName(_fromUtf8("labelKey"))
        self.labelKey.setText(_translate("Dialog", "Key", None))

        self.btSaveUserKey = QtWidgets.QToolButton(Dialog)
        self.btSaveUserKey.setGeometry(QtCore.QRect(340, 40, 41, 22))
        self.btSaveUserKey.setObjectName(_fromUtf8("btSaveUserKey"))
        self.btSaveUserKey.setText(_translate("Dialog", "save", None))
        self.btSaveUserKey.clicked.connect(self.saveUserKey)

        self.lineEditICCPath = QtWidgets.QLineEdit(Dialog)
        self.lineEditICCPath.setGeometry(QtCore.QRect(10, 100, 271, 21))
        self.lineEditICCPath.setObjectName(_fromUtf8("lineEditICCPath"))

        self.btSaveICCPath = QtWidgets.QToolButton(Dialog)
        self.btSaveICCPath.setGeometry(QtCore.QRect(340, 100, 41, 22))
        self.btSaveICCPath.setObjectName(_fromUtf8("btSaveIICPath"))
        self.btSaveICCPath.setText(_translate("Dialog", "save", None))
        self.btSaveICCPath.clicked.connect(self.save_icc_path)

        self.btExplore = QtWidgets.QToolButton(Dialog)
        self.btExplore.setGeometry(QtCore.QRect(290, 100, 41, 22))
        self.btExplore.setObjectName(_fromUtf8("btSaveIICPath"))
        self.btExplore.setText(_translate("Dialog", "find", None))
        self.btExplore.clicked.connect(self.find_icc_folder)

        self.labelICCRepo = QtWidgets.QLabel(Dialog)
        self.labelICCRepo.setGeometry(QtCore.QRect(10, 80, 141, 16))
        self.labelICCRepo.setObjectName(_fromUtf8("labelICCRepo"))
        self.labelICCRepo.setText(_translate("Dialog", "ICC Profile Repository", None))

        self.btClose = QtWidgets.QPushButton(Dialog)
        self.btClose.setGeometry(QtCore.QRect(280, 160, 113, 32))
        self.btClose.setObjectName(_fromUtf8("btClose"))
        self.btClose.setText(_translate("Dialog", "Close", None))

        self.btClose.clicked.connect(Dialog.close)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.params = ProcessSettingsClass()
        self.license = LicenseClass()
        self.lock_interface()
        self.show_icc_path()

    def find_icc_folder(self):

        fn = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a ICC directory')
        self.lineEditICCPath.setText(fn)

    def show_icc_path(self):

        path = self.params.setting_restore("iccFolder")
        self.lineEditICCPath.setText(path)

    def lock_interface(self):

        o = self.license.checkKey()

        if not o[0]:
            data = self.license.getKeyUser()
            self.lineEditUser.setText(data[0])
            self.lineEditKey.setText(data[1])

            self.lineEditKey.setStyleSheet("color: grey;")
            self.lineEditUser.setStyleSheet("color: grey;")

            self.lineEditKey.setEnabled(False)
            self.lineEditUser.setEnabled(False)

            self.btSaveUserKey.setEnabled(False)

    def saveUserKey(self):
        AppWarningsClass.status_warn("Disable en beta release")
        """
        user = self.lineEditUser.text()
        key = self.lineEditKey.text()        
        self.license.saveKeyUser(key, user)

        o = self.license.checkKey()

        if o[0]:
            my_Warning.statusWarning("Wrong user o key, remove!")
            license.saveKeyUser("", "")
        else:
            my_Warning.statusWarning("User and key ok, saved!")
        """

    def save_icc_path(self):
        path = self.lineEditICCPath.text()
        if path != "":
            if os.path.isdir(path):
                self.params.save_setting("iccFolder", path)
                AppWarningsClass.status_warn("Path was saved!")
                print(path)
            else:
                AppWarningsClass.status_warn("Path not exists")
        else:
            AppWarningsClass.status_warn("Path cannot empty")
