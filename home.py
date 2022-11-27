# -*- coding: utf-8 -*-

import os
import sys
import time

from PyQt5 import QtCore, QtGui, QtWidgets

from app_paths import DefinePathsClass
from camera_information_guid import CameraInfoUI
from charts import ChartPatternsClass
from confing_gui import ConfigUI
from deltas_class import GetDeltasClass
from deltas_guid import DeltaeUI
from getImageColors import getImageColors
from license import LicenseClass
from main import MainDialogUI
#from mtf_class import GetMTFClass
from mtf_guid import MtfUI
from spd_guid import spdUI
from mtf_rgb import GetMTFClassRGB
from multiple_class import MultipleTestClass
from neutralidad_class import GetFallOffClass
from neutralidad_guid import FallOffUI
from noise_class import GetNoiseClass
from noise_guid import deltaNoiseUI
from spd_class import GetSPDClass
from oecf_class import GetOECFClass
from oecf_guid import GetOECFUI
from plist_set import ProcessSettingsClass
from readCGATS import GetCGATSClass
from warning_class import AppWarningsClass
from imgdiff_class import ImgDiffClass
from imgdiff_guid import ImgDiffGui
from abcromatic_class import GetAbCromatic
from distortion_class import GetDistortion
from lens_guid import caberrationUI
from os import path
from log import log_Dialog
import traceback


class HomeUI(QtWidgets.QDialog):

    def __init__(self, parent=None):

        super(HomeUI, self).__init__(parent)
        self.ui = MainDialogUI()
        self.ui.setupUi(self)

        self.ui.DeltasDialog.clicked.connect(self.open_delta_e)
        self.ui.openNeutrality.clicked.connect(self.open_lightfalloff)
        self.ui.openMTF.clicked.connect(self.open_mtf)
        self.ui.openNoise.clicked.connect(self.open_noise)
        self.ui.openMultiple.clicked.connect(self.open_multiple_test)
        self.ui.openOECF.clicked.connect(self.open_oecf)
        self.ui.BtopenConf.clicked.connect(self.open_configuration)
        self.ui.openCameraInfo.clicked.connect(self.open_camera_info)
        self.ui.openSPD.clicked.connect(self.open_power_spectrum)
        self.ui.openDIFFstats.clicked.connect(self.open_img_diff)
        self.ui.openLensAberr.clicked.connect(self.open_lens_aberration)

        # self.chartType = self.ui.comboBox.currentIndex()
        self.chars = ChartPatternsClass()
        #self.check_license()

        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        self.conf_default = False
        if not path.exists(path_conf_file):
            return AppWarningsClass.critical_warn("Configuration file does not exist, errors is coming!")


    def open_camera_info(self):

        dialog = QtWidgets.QDialog()
        dialog.ui = CameraInfoUI(self.ui.rule_distance)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def open_configuration(self):

        dialog = QtWidgets.QDialog()
        dialog.ui = ConfigUI()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def check_license(self):

        status = LicenseClass()
        std = status.checkLicense()[0]
        if std:
            print("expied!")
            self.ui.openFile.setEnabled(False)

    def open_multiple_test(self):

        try:

            if not (hasattr(self.ui, 'coordenadasReales') or hasattr(self.ui, 'roiCoordinates')):
                return AppWarningsClass.critical_warn("Move the ROI pattern to select the area of interest")

            is_roi = self.chars.is_roi(self.ui.chartIndex)

            if is_roi:
                img_coordinates = self.ui.roiCoordinates
            else:
                img_coordinates = self.ui.coordenadasReales

            if not self.validate_coordinates(img_coordinates):
                return AppWarningsClass.critical_warn("Region Of Interest is outside!")


            dialog = QtWidgets.QDialog()
            dialog.ui = MultipleTestClass(img_coordinates, self.ui.multipleFiles, self.ui.CEGATSpath, self.ui.newICCprofile,
                                          self.ui.chartIndex)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_oecf(self):

        if not hasattr(self.ui, 'coordenadasReales'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the area of interest")

        if not self.validate_coordinates(self.ui.coordenadasReales):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        if not os.path.isfile(self.ui.CEGATSpath):
            return AppWarningsClass.critical_warn("Please load a CGATS reference file")

        if self.ui.imMode != "RGB":
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB!")

        try:
            colors = getImageColors(self.ui.coordenadasReales, self.ui.imgFileName, self.ui.newICCprofile)

            valoresReferencia = GetCGATSClass(self.ui.CEGATSpath)  # mandar ruta del archivo d referencia

            if len(colors.get_rgb_values()) != len(valoresReferencia.labCGATS):
                return AppWarningsClass.critical_warn("Number of samples in reference file does not match with image samples")

            oecf_values = GetOECFClass(colors.get_rgb_values(), colors.get_lab_values(),valoresReferencia.labCGATS )


            if self.ui.imMode == "RGB":

                de_values = [
                    ("OECF", oecf_values.get_oecf_values("OECF")),
                    ("RGB", oecf_values.get_oecf_values("RGB")),
                    ("RED", oecf_values.get_oecf_values("RED")),
                    ("GREEN", oecf_values.get_oecf_values("GREEN")),
                    ("BLUE", oecf_values.get_oecf_values("BLUE")),
                    ("DEV", oecf_values.get_oecf_values("DEV")),
                    ("WB", oecf_values.get_oecf_values("WB")),
                    ("LGAIN", oecf_values.getGain()),
                    ("VISUAL", colors.get_visual_roi(valoresReferencia.labCGATS)),
                    ("ROI", colors.get_roi_image())  ##se confunden estos dos ultimos graficos no se por que

                ]

            #elif self.ui.imMode == "L":

            #    de_values = [
            #        ("OECF", oecf_values.get_oecf_values("OECF")),
            #        ("DEV", oecf_values.get_oecf_values("DEV")),
            #        ("VISUAL", colors.get_visual_roi(valoresReferencia.RGB)),
            #        ("ROI", colors.get_roi_image())
            #   ]

            dialog = QtWidgets.QDialog()
            dialog.ui = GetOECFUI(de_values)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog( error )
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_delta_e(self):

        if not hasattr(self.ui, 'coordenadasReales'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the area of interest")

        if not self.validate_coordinates(self.ui.coordenadasReales):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        if not os.path.isfile(self.ui.CEGATSpath):
            return AppWarningsClass.critical_warn("Please load a CGATS reference file")

        if self.ui.imMode != "RGB":
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB!")

        try:
            lab_values = getImageColors(self.ui.coordenadasReales, self.ui.imgFileName, self.ui.newICCprofile)

            reference_values = GetCGATSClass(self.ui.CEGATSpath)  # mandar ruta del archivo d referencia

            deltas = GetDeltasClass(lab_values.get_lab_values(), reference_values.labCGATS)


            if self.ui.imMode == "RGB":
                de_values = [("CIE76", deltas.get_cie76()),
                             ("CIE00", deltas.get_cie00()),
                             ("CIE94", deltas.get_cie94()),
                             ("CMC", deltas.get_cmc()),
                             ("DEC", deltas.get_d_chroma()),
                             ("DEL", deltas.get_d_lightness()),
                             ("DEH", deltas.get_d_hue()),
                             ("ROI", lab_values.get_roi_image()),
                             ("VISUAL", lab_values.get_visual_roi(reference_values.labCGATS))
                             ]

                dialog = QtWidgets.QDialog()
                dialog.ui = DeltaeUI(de_values)
                dialog.ui.setupUi(dialog)
                dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_noise(self):

        if not hasattr(self.ui, 'coordenadasReales'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the region of interest")

        if not self.validate_coordinates(self.ui.coordenadasReales):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        formatsAvailable = ["RGB"]
        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB or grayscale")

        if not os.path.isfile(self.ui.CEGATSpath):
            return AppWarningsClass.critical_warn("Please load a CGATS reference file")

        try:
            valoresReferencia = GetCGATSClass(self.ui.CEGATSpath)  # mandar ruta del archivo d referencia

            lab_values = getImageColors(self.ui.coordenadasReales, self.ui.imgFileName, self.ui.newICCprofile)

            if len(lab_values.get_rgb_values()) != len(valoresReferencia.labCGATS):
                return AppWarningsClass.critical_warn("Number of samples in reference file does not match with image samples")

            #noise = GetNoiseClass(lab_values.get_rgb_values(), valoresReferencia.labCGATS )
            noise = GetNoiseClass(lab_values.get_rgb_values() )

            #(self.ui.imMode)

            if self.ui.imMode == "RGB":

                de_values = [("SNR-RGB", noise.getRGB()),
                             ("SNR", noise.getSNR()),
                             ("C_NOISE", noise.getCromaNoise()),
                             #("RDEV", noise.getDR())
                             ]

            elif self.ui.imMode == "L":

                de_values = [
                    ("SNR", noise.getSNR()),
                    #("RDEV", noise.getDR())
                ]

            dialog = QtWidgets.QDialog()
            dialog.ui = deltaNoiseUI(de_values)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_img_diff(self):

        formatsAvailable = ["RGB","L"]
        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB or grayscale")

        if len(self.ui.multipleFiles) > 2:
            return AppWarningsClass.informative_warn("You have chosen " + str(len(self.ui.multipleFiles)) + "files, you must choose only two files")

        try:

            imgDiffStats = ImgDiffClass(self.ui.multipleFiles)

            dialog = QtWidgets.QDialog()
            dialog.ui = ImgDiffGui(imgDiffStats.image_stats(), imgDiffStats.np_im)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_lens_aberration(self):

        formatsAvailable = ["RGB","L"]

        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB or grayscale")

        try:
            cromatic = GetAbCromatic(self.ui.imgFileName)

            if cromatic.width > 1500:
                return AppWarningsClass.critical_warn("Upload an image that is less than 1500 px width")

            distortion = GetDistortion()

            CA = cromatic.getAberration()
            DIS = distortion.getDistortion(self.ui.imgFileName)

            if CA is None or  DIS is None:
                return AppWarningsClass.critical_warn("Could not detect circles")


            values = [ ("CARG", CA),
                       ("CABGr", CA),
                       ("DISTORTION", DIS ),
                       ("VISUAL-CABG", cromatic.imageBG),
                       ("VISUAL-CARG", cromatic.imageRG),
                       ("VISUAL-DIST", distortion.imgDistortion)
                              ]

            dialog = QtWidgets.QDialog()
            dialog.ui = caberrationUI(values)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()



    def open_power_spectrum(self):

        if not hasattr(self.ui, 'roiCoordinates'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the region of interest")

        if not self.validate_coordinates(self.ui.roiCoordinates):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        formatsAvailable = ["RGB","L"]

        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB or grayscale")

        try:

            spd = GetSPDClass(self.ui.imgFileName, self.ui.roiCoordinates)

            spd_values = [("NPS_RGB_X", spd.getPSD(1)),
                          ("NPS_RGB_Y", spd.getPSD(0)),
                          ("HISTO", spd.histogram())
                              ]

            dialog = QtWidgets.QDialog()
            dialog.ui = spdUI(spd_values)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def open_mtf(self):

        if not hasattr(self.ui, 'roiCoordinates'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the region of interest")

        if not self.validate_coordinates(self.ui.roiCoordinates):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        formatsAvailable = ["RGB","L"]

        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, only RGB or grayscale")

        try:

            get_mtf_rgb = GetMTFClassRGB(self.ui.imgFileName, self.ui.roiCoordinates)
            values = get_mtf_rgb.get_mtf_esf_lsf()


            #print(values["channel_esf"])
            if type(values) is dict:
                mtf_values = [("MTF", values["channel_mtf"]),
                              ("ESF", values["channel_esf"]),
                              ("LSF", values["channel_lsf"]),
                              #("MODE", values["mode"]),
                              #("BORDER", get_mtf.edges),
                              ("ROI", get_mtf_rgb.compute_roi())]

                dialog = QtWidgets.QDialog()
                dialog.ui = MtfUI(mtf_values)
                dialog.ui.setupUi(dialog)
                dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()


    def open_lightfalloff(self):

        if not hasattr(self.ui, 'roiCoordinates'):
            return AppWarningsClass.critical_warn("Move the ROI pattern to select the region of interest")

        elif not self.validate_coordinates(self.ui.roiCoordinates):
            return AppWarningsClass.critical_warn("Region Of Interest is outside!")

        formatsAvailable = ["RGB"]

        if self.ui.imMode not in formatsAvailable :
            return AppWarningsClass.critical_warn("Color mode "+self.ui.imMode+" != support, just RGB mode")

        try:
            get_neutral = GetFallOffClass(self.ui.roiCoordinates, self.ui.imgFileName)

            dialog = QtWidgets.QDialog()
            dialog.ui = FallOffUI(get_neutral.image_stats(), get_neutral.np_im)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        except:

            error = traceback.format_exc()

            print(error)

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def validate_coordinates(self, coordenadas):

        if isinstance(coordenadas[0], list):
            std = True
            for x in range(len(coordenadas)):
                for y in range(len(coordenadas[x])):
                    if coordenadas[x][y] < 0:
                        std = False
        else:
            std = True
            for x in range(len(coordenadas)):
                if coordenadas[x] < 0:
                    std = False

        return std




if __name__ == '__main__':

    root = QtGui.QApplication(sys.argv)

    # --- splash screen

    # application_path = os.path.dirname(sys.argv[0])
    # createIconPath = os.path.join(application_path,"line-icons", 'splash.jpg' )

    pixmap = QtGui.QPixmap(DefinePathsClass.create_resource_path('splash.jpg'), 'JPEG')
    splash_screen = QtGui.QSplashScreen(pixmap, QtCore.Qt.WindowStaysOnTopHint)

    #status = LicenseClass()
    #splash_screen.showMessage(status.betaXpires()[1], QtCore.Qt.AlignTop, QtCore.Qt.black)

    splash_screen.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
    splash_screen.setEnabled(False)
    Bar = QtGui.QProgressBar(splash_screen)
    Bar.setMaximum(10)
    Bar.setGeometry(0, pixmap.height() - 20, pixmap.width(), 20)

    splash_screen.show()

    params = ProcessSettingsClass()
    version = params.setting_restore("release")

    texto = ["", "", "", "", "", version, version ]
    #aqui va un rango de 1,7
    for i in range(1, 3):
        Bar.setValue(i)
        t = time.time()
        if i > 4 and texto[i] in texto:
            splash_screen.showMessage(texto[i], QtCore.Qt.AlignTop, QtCore.Qt.black)
        # se puede introducir el retraso en la splash
        while time.time() < t + 1:
            root.processEvents()

    # splash_screen.close()
    # --- splash screen
    try:
        app = HomeUI()
        app.show()
        splash_screen.finish(app)
        sys.exit(root.exec_())

    except Exception as e:

        error = traceback.format_exc()
        print(error)
        dialog = QtWidgets.QDialog()
        dialog.ui = log_Dialog(error)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
