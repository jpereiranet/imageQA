# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from camera_information_class import CameraInformationClass
from plist_set import ProcessSettingsClass

import string


class CameraInfoUI(object):

    def __init__(self, rule_distance):

        if rule_distance is None:
            rule_distance = ""
        self.rule_distance = rule_distance
        self.params = ProcessSettingsClass()
        self.camerainfo = CameraInformationClass()

    def setupUi(self, Dialog):

        _translate = QtCore.QCoreApplication.translate
        Dialog.setObjectName("Dialog")
        Dialog.setFixedSize(281, 350)

        Dialog.setWindowTitle(_translate("Dialog", "Camera information"))

        values = self.camerainfo.get_metadata()

        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(70, 10, 131, 16))
        self.label.setObjectName("label")
        self.label.setText(_translate("Dialog", "Camera Information"))

        self.labelSensorWidth = QtWidgets.QLabel(Dialog)
        self.labelSensorWidth.setGeometry(QtCore.QRect(10, 40, 141, 16))
        self.labelSensorWidth.setObjectName("labelSensorWidth")
        self.labelSensorWidth.setText(_translate("Dialog", "Sensor Width (mm)"))

        self.labelSensorHeight = QtWidgets.QLabel(Dialog)
        self.labelSensorHeight.setGeometry(QtCore.QRect(10, 70, 141, 16))
        self.labelSensorHeight.setObjectName("labelSensorHeight")
        self.labelSensorHeight.setText(_translate("Dialog", "Sensor Height (mm)"))

        self.labelPixelesWidth = QtWidgets.QLabel(Dialog)
        self.labelPixelesWidth.setGeometry(QtCore.QRect(10, 110, 141, 16))
        self.labelPixelesWidth.setObjectName("labelPixelesWidth")
        self.labelPixelesWidth.setText(_translate("Dialog", "Image Width (pixeles)"))

        self.labelPixelesHeght = QtWidgets.QLabel(Dialog)
        self.labelPixelesHeght.setGeometry(QtCore.QRect(10, 140, 141, 16))
        self.labelPixelesHeght.setObjectName("labelPixelesHeght")
        self.labelPixelesHeght.setText(_translate("Dialog", "Image Height (pixeles)"))

        self.labelPitch = QtWidgets.QLabel(Dialog)
        self.labelPitch.setGeometry(QtCore.QRect(10, 180, 141, 16))
        self.labelPitch.setObjectName("labelPitch")
        self.labelPitch.setText(_translate("Dialog", "Pixel pitch (µm)"))

        self.input_width = QtWidgets.QLineEdit(Dialog)
        self.input_width.setGeometry(QtCore.QRect(162, 40, 101, 21))
        self.input_width.setObjectName("input_width")
        self.input_width.setText(str(values["widthSensor"]))
        self.input_width.textChanged.connect(self.get_pitch)

        self.input_height = QtWidgets.QLineEdit(Dialog)
        self.input_height.setGeometry(QtCore.QRect(162, 70, 101, 21))
        self.input_height.setObjectName("input_height")
        self.input_height.setText(str(values["heightSensor"]))

        self.input_pixel_height = QtWidgets.QLineEdit(Dialog)
        self.input_pixel_height.setGeometry(QtCore.QRect(162, 140, 101, 21))
        self.input_pixel_height.setObjectName("input_pixel_height")
        self.input_pixel_height.setText(str(values["imgHeight"]))

        self.input_pixel_width = QtWidgets.QLineEdit(Dialog)
        self.input_pixel_width.setGeometry(QtCore.QRect(162, 110, 101, 21))
        self.input_pixel_width.setObjectName("input_pixel_width")
        self.input_pixel_width.setText(str(values["imgWidth"]))
        self.input_pixel_width.textChanged.connect(self.get_pitch)

        self.input_pixel_pitch = QtWidgets.QLineEdit(Dialog)
        self.input_pixel_pitch.setGeometry(QtCore.QRect(162, 180, 101, 21))
        self.input_pixel_pitch.setObjectName("input_pixel_pitch")
        self.input_pixel_pitch.setText(str(values["pitch"]))


        #----rule info

        self.labelRule = QtWidgets.QLabel(Dialog)
        self.labelRule.setGeometry(QtCore.QRect(10, 220, 141, 16))
        self.labelRule.setObjectName("labelPixelesWidth")
        self.labelRule.setText(_translate("Dialog", "Rule (pixel|mm)"))

        self.input_rule_pixel = QtWidgets.QLineEdit(Dialog)
        self.input_rule_pixel.setGeometry(QtCore.QRect(162, 220, 48, 21))

        rulePixel = self.rule_distance

        if self.rule_distance is "":
            rulePixel = values["rulePixel"]

        #elif values["rulePixel"] is "":
        #    rulePixel = self.rule_distance

        self.input_rule_pixel.setObjectName("rule_pixel_distance")
        self.input_rule_pixel.setText(str( rulePixel))
        self.input_rule_pixel.setEnabled(False)

        self.input_rule_real = QtWidgets.QLineEdit(Dialog)
        self.input_rule_real.setGeometry(QtCore.QRect(212, 220, 48, 21))
        self.input_rule_real.setObjectName("rule_real_distance")
        self.input_rule_real.setText(str(values["ruleReal"]))
        self.input_rule_real.textChanged.connect(self.get_resolution)
        self.input_rule_real.setEnabled(False)

        if self.input_rule_pixel.text() is not "":
            self.input_rule_real.setEnabled(True)


        self.labelPPIResolution = QtWidgets.QLabel(Dialog)
        self.labelPPIResolution.setGeometry(QtCore.QRect(10, 260, 141, 16))
        self.labelPPIResolution.setObjectName("resolutionPPI")
        self.labelPPIResolution.setText(_translate("Dialog", "Resolution (PPI)"))

        self.input_ppi_resolution = QtWidgets.QLineEdit(Dialog)
        self.input_ppi_resolution.setGeometry(QtCore.QRect(162, 260, 101, 21))
        self.input_ppi_resolution.setObjectName("resolution")
        self.input_ppi_resolution.setText(str(values["resolution"]))

        #---- close & save
        self.CancelBT = QtWidgets.QPushButton(Dialog)
        self.CancelBT.setGeometry(QtCore.QRect(140, 300, 113, 32))
        self.CancelBT.setObjectName("CancelBT")
        self.CancelBT.setText(_translate("Dialog", "Close"))
        self.CancelBT.clicked.connect(Dialog.close)

        self.saveBT = QtWidgets.QPushButton(Dialog)
        self.saveBT.setGeometry(QtCore.QRect(30, 300, 113, 32))
        self.saveBT.setObjectName("saveBT")
        self.saveBT.setText(_translate("Dialog", "Save"))
        # self.saveBT.clicked.connect(self.saveValues)
        self.saveBT.clicked.connect(lambda state, x=Dialog: self.save_new_camera_values(x))

        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def clean_chars(self, value):

        #return ''.join(filter(str.isdigit, value))
        return value


        #all = string.maketrans('', '')
        #nodigs = all.translate(all, string.digits)
        #return value.translate(all, nodigs)

    def get_resolution(self):
        #img_width = self.input_pixel_width.text()
        #img_height = self.input_pixel_height.text()

        #diagonal = math.sqrt( (img_width*img_width) + (img_height*img_height) )

        rule_pixel = self.clean_chars(self.input_rule_pixel.text())
        rule_real = float(self.clean_chars(self.input_rule_real.text())) / 25.4

        ppi = int( float(rule_pixel) / float(rule_real) )
        self.input_ppi_resolution.setText( str(ppi) )



    def get_pitch(self):

        width_sensor = self.clean_chars(self.input_width.text())
        img_width = self.clean_chars(self.input_pixel_width.text())

        if self.camerainfo.check_if_number(width_sensor) and self.camerainfo.check_if_number(img_width):

            if width_sensor is not "" and img_width is not "":

                if float(width_sensor) > 0 and float(img_width) > 0:
                    pitch = round((float(width_sensor) / float(img_width)) * 1000, 2)
                    self.input_pixel_pitch.setText(str(pitch))

    def non_empty(self,value):

        if value.strip() == "":
            s = 0
        else:
            s = value.strip()
        return s

    def save_new_camera_values(self, x):

        o = {"widthSensor": self.clean_chars(int(float(self.non_empty(self.input_width.text())))),
             "heightSensor": self.clean_chars(int(float(self.non_empty(self.input_height.text())))),
             "imgWidth": self.clean_chars(int(float(self.non_empty(self.input_pixel_width.text())))),
             "imgHeight": self.clean_chars(int(float(self.non_empty(self.input_pixel_height.text())))),
             "pitch": self.non_empty(self.input_pixel_pitch.text()),
             "rulePixel": self.clean_chars(self.non_empty(self.input_rule_pixel.text())),
             "ruleReal": self.clean_chars(self.non_empty(self.input_rule_real.text())),
             "resolution": self.clean_chars(self.non_empty(self.input_ppi_resolution.text()))


             }

        s = self.camerainfo.save_camera_values(o)

        if s:
            x.close()
