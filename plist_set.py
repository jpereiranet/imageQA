# -*- coding: utf-8 -*-
from PyQt5 import QtCore


# guarda en /Users/jpereira/Library/Preferences/com.jpereiranet.imageQA.plist
class ProcessSettingsClass:

    def __init__(self):
        ORGANIZACION = "jpereiranet"
        APLICACION = "imageQA"

        self.qsettings = QtCore.QSettings(ORGANIZACION, APLICACION)

        # print(self.qsettings.fileName())

    def save_setting(self, key, value):
        self.qsettings.setValue(key, value)
        self.qsettings.sync()

    def setting_restore(self, key):
        # return self.qsettings.value(key, type=str)
        o = self.qsettings.value(key)
        # print(o)
        return o

    def setting_contains(self, key):
        return self.qsettings.contains(key)

    def settings_restore(self, key):
        self.qsettings.remove(key)
        self.qsettings.sync()
