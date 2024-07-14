# -*- coding: utf-8 -*-

import os
import pyqtgraph as pg
from PIL import ImageCms
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QComboBox, QGraphicsPixmapItem, QApplication
from ImgTransformClass import ImgTransformClass
from app_paths import DefinePathsClass
from camera_information_class import CameraInformationClass
from charts import ChartPatternsClass
from imgInfo import GetImgInfo
from plist_set import ProcessSettingsClass
from warning_class import AppWarningsClass
from pathlib import Path
from log import log_Dialog
import traceback
import time



try:
    _encoding = QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)


class MainDialogUI(object):

    def __init__(self):

        # PATH = "/Users/jpereira/Library/ColorSync/Profiles/"
        self.WIDTH_VIEWER = 600
        self.HIGHT_VIEWER = 400
        self.WIDTH_ROI = 230
        self.HIGHT_ROI = 150
        ##para centrar x_roi y y_roi pueden tomar el valor 230 y 150 pero la escala y la rotación se vuelve loca
        self.X_ROI = 0
        self.Y_ROI = 0

        self.x_orig = 0
        self.y_orig = 0

        self.chartIndex = 0

        try:
            self.chars = ChartPatternsClass()

            self.params = ProcessSettingsClass()

            self.camerainfo = CameraInformationClass()

            self.iccFolder = DefinePathsClass.get_icc_folder_path()

        except:

            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(traceback.format_exc())
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

        # se usan para calcular las MTF
        self.imgWidth = None
        self.imgHeight = None
        self.sensorWidth = None
        self.sensorHeight = None
        self.pitch = None
        self.rule_distance = None

        self.credits = "By José Pereira www.jpereira.net"

    def setupUi(self, Dialog):

        version = self.params.setting_restore("release")

        Dialog.setObjectName("Color Analyzer")

        Dialog.setFixedSize(690, 600)

        Dialog.setWindowFlags(
            QtCore.Qt.WindowMaximizeButtonHint | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

        Dialog.setWindowTitle(_translate("Dialog", "Image Quality Analysis", None))

        Dialog.setWindowIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('icon.ico')))

        self.newICCprofile = False

        # estilos
        font = QtGui.QFont()
        font.setPointSize(10)
        colorFuente = "color: rgb(155, 155, 155)"
        # --- botones ----

        #OPEN FILE
        self.openFile = QtWidgets.QToolButton(Dialog)
        self.openFile.setGeometry(QtCore.QRect(10, 10, 61, 51))
        self.openFile.setObjectName("openFile")
        self.openFile.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('picture_64px.png')))
        self.openFile.setIconSize(QtCore.QSize(30, 30))
        self.openFile.setToolTip("Open Image")
        self.openFile.clicked.connect(self.get_test_image)

        #EXECUTE DELTA-E
        self.DeltasDialog = QtWidgets.QToolButton(Dialog)
        self.DeltasDialog.setGeometry(QtCore.QRect(80, 10, 61, 51))
        self.DeltasDialog.setObjectName("btDeltas")
        self.DeltasDialog.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('bargraph_64px.png')))
        self.DeltasDialog.setIconSize(QtCore.QSize(40, 40))
        self.DeltasDialog.setToolTip("Open Delta-e")

        #OPEN CGATS
        self.openCGATS = QtWidgets.QToolButton(Dialog)
        self.openCGATS.setGeometry(QtCore.QRect(150, 10, 61, 51))
        self.openCGATS.setObjectName("btCGATS")
        self.openCGATS.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('document_64px.png')))
        self.openCGATS.setIconSize(QtCore.QSize(40, 40))
        self.openCGATS.setToolTip("Open CGATS")
        self.openCGATS.clicked.connect(self.get_cgats)

        #OPEN LIGTH FALLOFF
        self.openNeutrality = QtWidgets.QToolButton(Dialog)
        self.openNeutrality.setGeometry(QtCore.QRect(220, 10, 61, 51))
        self.openNeutrality.setObjectName("btNeutral")
        self.openNeutrality.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('neutral_64px.png')))
        self.openNeutrality.setIconSize(QtCore.QSize(40, 40))
        self.openNeutrality.setToolTip("Open Neutrality")

        #OPEN MTF
        self.openMTF = QtWidgets.QToolButton(Dialog)
        self.openMTF.setGeometry(QtCore.QRect(290, 10, 61, 51))
        self.openMTF.setObjectName("btMTF")
        self.openMTF.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('linegraph_64px.png')))
        self.openMTF.setIconSize(QtCore.QSize(30, 30))
        self.openMTF.setToolTip("Open MTF")

        #OPEN NOISE
        self.openNoise = QtWidgets.QToolButton(Dialog)
        self.openNoise.setGeometry(QtCore.QRect(360, 70, 61, 51))
        self.openNoise.setObjectName("btNoise")
        self.openNoise.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('noise_64px.png')))
        self.openNoise.setIconSize(QtCore.QSize(30, 30))
        self.openNoise.setToolTip("Open Noise")

        #OPEN OECF
        self.openOECF = QtWidgets.QToolButton(Dialog)
        self.openOECF.setGeometry(QtCore.QRect(360, 10, 61, 51))
        self.openOECF.setObjectName("openOECF")
        self.openOECF.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('oecf_64px.png')))
        self.openOECF.setIconSize(QtCore.QSize(40, 40))
        self.openOECF.setToolTip("Open OECF")

        #OPEN MULTIPLE
        self.openMultiple = QtWidgets.QToolButton(Dialog)
        self.openMultiple.setGeometry(QtCore.QRect(620, 140, 61, 51))
        self.openMultiple.setObjectName("btMultiple")
        self.openMultiple.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('batch_64px.png')))
        self.openMultiple.setIconSize(QtCore.QSize(40, 40))
        self.openMultiple.setToolTip("Open bach")
        self.openMultiple.setEnabled(False)

        #OPEN CONFIGURATION
        self.BtopenConf = QtWidgets.QToolButton(Dialog)
        self.BtopenConf.setGeometry(QtCore.QRect(620, 200, 61, 51))
        self.BtopenConf.setObjectName("btConf")
        self.BtopenConf.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('conf_64px.png')))
        self.BtopenConf.setIconSize(QtCore.QSize(40, 40))
        self.BtopenConf.setToolTip("Open Configuration")
        self.BtopenConf.setEnabled(True)
        # self.BtopenConf.clicked.connect(self.openConf)

        #OPEN CAMERA INFO
        self.openCameraInfo = QtWidgets.QToolButton(Dialog)
        self.openCameraInfo.setGeometry(QtCore.QRect(620, 260, 61, 51))
        self.openCameraInfo.setObjectName("btConf")
        self.openCameraInfo.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('camerainfo_64px.png')))
        self.openCameraInfo.setIconSize(QtCore.QSize(40, 40))
        self.openCameraInfo.setToolTip("Open Camera Info")
        self.openCameraInfo.setEnabled(False)


        #OPEN SPD
        self.openSPD = QtWidgets.QToolButton(Dialog)
        self.openSPD.setGeometry(QtCore.QRect(620, 10, 61, 51))
        self.openSPD.setObjectName("btSPD")
        self.openSPD.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('psd_64px.png')))
        self.openSPD.setIconSize(QtCore.QSize(40, 40))
        self.openSPD.setToolTip("Open power spectrum")
        self.openSPD.setEnabled(False)

        #OPEN DIFF
        self.openDIFFstats = QtWidgets.QToolButton(Dialog)
        self.openDIFFstats.setGeometry(QtCore.QRect(620, 70, 61, 51))
        self.openDIFFstats.setObjectName("btDIFF")
        self.openDIFFstats.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('smooth_64px.png')))
        self.openDIFFstats.setIconSize(QtCore.QSize(40, 40))
        self.openDIFFstats.setToolTip("Open Image DIFF")
        self.openDIFFstats.setEnabled(False)

        #OPEN LENS
        self.openLensAberr = QtWidgets.QToolButton(Dialog)
        self.openLensAberr.setGeometry(QtCore.QRect(620, 320, 61, 51))
        self.openLensAberr.setObjectName("btLens")
        self.openLensAberr.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('lens_64px.png')))
        self.openLensAberr.setIconSize(QtCore.QSize(40, 40))
        self.openLensAberr.setToolTip("Open Lens Aberrations")
        self.openLensAberr.setEnabled(False)

        # --- fin botones ----

        # marcos-----
        self.frame = QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(430, 10, 181, 51))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frComboROI")

        self.frame_2 = QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(430, 70, 181, 51))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frComboICCProfiles")

        # marcos-----

        # --- combo ----
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(colorFuente)
        self.label_4.setGeometry(QtCore.QRect(10, 0, 91, 20))
        self.label_4.setText(_translate("Dialog", "Target type", None))

        self.comboBox = QComboBox(self.frame)
        self.comboBox.setFont(font)
        self.comboBox.setGeometry(QtCore.QRect(10, 20, 161, 26))
        self.comboBox.setObjectName("comboTargetType")
        self.comboBox.addItems(sorted(self.chars.chartsType.keys()))
        self.comboBox.currentIndexChanged.connect(self.update_chart)
        # --- fin combo ----

        # ------perfiles adicionales
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setFont(font)
        self.label_6.setStyleSheet(colorFuente)
        self.label_6.setGeometry(QtCore.QRect(10, 0, 91, 20))
        self.label_6.setText(_translate("Dialog", "Optional Profile", None))

        self.comboBox_2 = QtWidgets.QComboBox(self.frame_2)
        self.comboBox_2.setGeometry(QtCore.QRect(10, 20, 161, 26))
        self.comboBox_2.setObjectName("comboOptionalProfile")
        self.comboBox_2.setFont(font)
        self.comboBox_2.currentIndexChanged.connect(self.update_preview)
        # ------

        # ------- label footer ----

        self.label_footer = QtWidgets.QLabel(Dialog)
        # self.label_footer = QtWidgets.QLineEdit(Dialog)
        self.label_footer.setGeometry(QtCore.QRect(10, 576, 601, 20))
        self.label_footer.setFont(font)
        self.label_footer.setStyleSheet(colorFuente)
        # self.label_footer.setStyleSheet("color:#ff4100;")
        self.label_footer.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_footer.setObjectName("label_footer")
        self.label_footer.setText(_translate("Dialog", self.credits, None))

        self.label_coordinates = QtWidgets.QLabel(Dialog)
        # self.label_footer = QtWidgets.QLineEdit(Dialog)
        self.label_coordinates.setGeometry(QtCore.QRect(620, 576, 81, 20))
        self.label_coordinates.setFont(font)
        self.label_coordinates.setStyleSheet(colorFuente)
        # self.label_footer.setStyleSheet("color:#ff4100;")
        self.label_coordinates.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.label_coordinates.setObjectName("label_coordinates")


        # --- etiquetas ----
        # rotulos
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(0, 70, 71, 16))
        self.label_7.setFont(font)
        self.label_7.setStyleSheet(colorFuente)
        self.label_7.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName("label_7")
        self.label_7.setText(_translate("Dialog", "ICC Profile:", None))

        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(0, 90, 71, 16))
        self.label_8.setFont(font)
        self.label_8.setStyleSheet(colorFuente)
        self.label_8.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName("label_8")
        self.label_8.setText(_translate("Dialog", "File:", None))

        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(0, 110, 71, 16))
        self.label_9.setFont(font)
        self.label_9.setStyleSheet(colorFuente)
        self.label_9.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName("label_9")
        self.label_9.setText(_translate("Dialog", "Reference:", None))
        # ----

        # laber icc
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setFont(font)
        self.label.setStyleSheet(colorFuente)
        self.label.setGeometry(QtCore.QRect(90, 70, 221, 16))
        self.label.setObjectName("lbProfileName")
        # label filename
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(colorFuente)
        self.label_2.setGeometry(QtCore.QRect(90, 90, 221, 16))
        self.label_2.setObjectName("lbFileName")
        # label referencia
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(colorFuente)
        self.label_3.setGeometry(QtCore.QRect(90, 110, 221, 16))
        self.label_3.setObjectName("lbCGATSreference")

        # --- fin etiquetas ----
        # --- linea ----
        """
        self.line = QFrame(Dialog)
        self.line.setGeometry(QtCore.QRect(10, 120, 590, 16))
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("lineSeparatorMenuLayout"))
        """
        # --- fin linea ----

        ##--- layout vertical
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 140, self.WIDTH_VIEWER, self.HIGHT_VIEWER))

        self.verticalLayoutWidget.setStyleSheet("background-color:#ccc;")
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        self.verticalLayout.setObjectName("verticalLayout")

        ##--- GraphicsView (visor de imagenes )
        self.graphicsView = pg.GraphicsView(useOpenGL=True, background=pg.mkColor('#ccc'))
        self.graphicsView.setObjectName("graphicsView")
        self.verticalLayout.addWidget(self.graphicsView)

        QtCore.QMetaObject.connectSlotsByName(Dialog)

        self.get_prev_image()
        self.reset_layout()
        self.get_icc_files()

        # ---- fin -------

    def update_preview(self):

        if self.comboBox_2.currentIndex() > 0:

            try:
                self.newICCprofile = os.path.join(self.iccFolder, str(self.comboBox_2.currentText()))
                im = ImgTransformClass(self.imgFileName, self.newICCprofile)

                self.myImage2 = im.image_previsualization()
                self.getImage.setPixmap(self.myImage2)

            except:

                dialog = QtWidgets.QDialog()
                dialog.ui = log_Dialog( traceback.format_exc() )
                dialog.ui.setupUi(dialog)
                dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                dialog.exec_()
        else:
            self.newICCprofile = False

        # print(self.perfil_nuevo)

    def update_chart(self):

        self.remove_item_from_layout()
        self.chartIndex = self.comboBox.currentIndex()
        if self.chartIndex > 0:
            switch = self.chars.get_switch(self.chartIndex)
            self.chartVars = self.chars.get_chart(self.chartIndex)


            chart_name = self.chars.get_chart_name(self.chartIndex)
            if chart_name == "SFR/MTF":
                std = self.camerainfo.check_pitch()
                if std[0]:
                    self.footer_advice(self.credits, "info")
                else:
                    self.footer_advice(std[1], "err")
            else:
                self.footer_advice(self.credits, "info")

            # time.sleep(1)
            if chart_name == "Sampling":
                self.make_ruler()
            else:
                self.rule_distance = None
                if self.chartVars[4] != "" and self.chartVars[5] != "":
                    self.make_roi(self.chartVars[4], self.chartVars[5])
                else:
                    #si se selecciona FULL
                    self.roiCoordinates = [0,0,self.imgWidth/self.ratio,self.imgHeight/self.ratio]
                self.roi_pattern(self.chartVars)
                self.CEGATSpath = self.chartVars[3]
                self.label_3.setText(os.path.basename(self.CEGATSpath))

            # enable / disable buttons
            self.DeltasDialog.setEnabled(switch[0])
            self.openCGATS.setEnabled(switch[1])
            self.openNeutrality.setEnabled(switch[2])
            self.openMTF.setEnabled(switch[3])
            self.openNoise.setEnabled(switch[4])
            self.openOECF.setEnabled(switch[5])
            self.openCameraInfo.setEnabled(switch[6])
            self.openSPD.setEnabled(switch[7])
            self.openDIFFstats.setEnabled(switch[8])
            self.openLensAberr.setEnabled(switch[9])

        else:
            self.reset_layout()

    def reset_layout(self):

        self.label_coordinates.setText("")
        self.comboBox.setCurrentIndex(0)
        self.DeltasDialog.setEnabled(False)
        self.openCGATS.setEnabled(False)
        self.openNeutrality.setEnabled(False)
        self.openMTF.setEnabled(False)
        self.openNoise.setEnabled(False)
        self.openOECF.setEnabled(False)
        self.openCameraInfo.setEnabled(False)
        self.openSPD.setEnabled(False)
        #self.openLensAberr.setEnabled(False)

        #self.openDIFFstats.setEnabled(False)

    def remove_item_from_layout(self):

        objects = list(self.graphicsView.scene().items())
        #print(objects)
        for i in range(objects.__len__()):

            cadena = str(objects[i])
            r = cadena.split(".")
            #print("0:",r[0])
            #print("1:",r[1])
            #print("2:",r[2])


            #if r[2] == 'GraphItem' or r[2] == 'ROI':
            if r[0] == "<pyqtgraph":
                #print('borra')
                try:
                    objects[i].prepareGeometryChange() #parece que soluciona los cuelgues
                    self.graphicsView.removeItem(objects[i])
                    #self.graphicsView.update()  # no soluciona los cuelgues en mojave
                    #QApplication.processEvents() # tampoco soluciona los cuelgues
                    #time.sleep(1) # tampoco soluciona los cuelgues
                except:
                    dialog = QtWidgets.QDialog()
                    dialog.ui = log_Dialog(traceback.format_exc())
                    dialog.ui.setupUi(dialog)
                    dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                    dialog.exec_()

        #objects = list(self.graphicsView.scene().items())
        #print("TRAS ORRAR:",objects)

    def get_prev_image(self):

        fname = DefinePathsClass.create_resource_path("welcome.jpg")

        if self.do_md5(fname) != "a61f9532533f840cb4924eb0da452f7e":
            exit()

        self.imgFileName = fname
        # self.myImage = pg.QtGui.QPixmap(fname)

        try:
            im = ImgTransformClass(self.imgFileName, profile_path=False)
            imgSizing = im.get_ratio_transform()

            self.ratio = imgSizing[7]
            self.imMode = im.mode

            self.imgWidth = im.width
            self.imgHeight = im.height

            self.myImage2 = im.image_previsualization()

            # self.myImage2 = self.myImage.scaled(self.WIDTH_VIEWER, self.HIGHT_VIEWER, QtCore.Qt.KeepAspectRatio)
            self.getImage = QGraphicsPixmapItem(self.myImage2)

            self.graphicsView.addItem(self.getImage)

            # self.layoutGeometry(im)
            self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 140, imgSizing[4], imgSizing[5]))

            self.camerainfo.rese_camera_information()

        except:

            error = traceback.format_exc()
            print(error)
            dialog = QtWidgets.QDialog()
            dialog.ui = log_Dialog(error)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    def do_md5(self, fn):

        import hashlib
        hash_md5 = hashlib.md5()
        with open(fn, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def get_test_image(self):

        #qfd = QtWidgets.QFileDialog()

        if self.params.setting_contains("rootfolder"):
            path = self.params.setting_restore("rootfolder")
            # print(path)
        else:
            path = ""

        qfd = QtWidgets.QFileDialog()
        paths = [str(file_n) for file_n in list(
            QtWidgets.QFileDialog.getOpenFileNames(qfd, "Select files", path,
                                                   filter='Images (*.png *.tif *.tiff  *.jpg *.jpeg)'
                                                   )[0])]

        if len(paths) > 1:
            self.openMultiple.setEnabled(True)
            self.openDIFFstats.setEnabled(True)
            paths.sort()
            self.multipleFiles = paths
            #print(self.multipleFiles)
            # print("is multiple!")
        else:
            self.openMultiple.setEnabled(False)
            self.openDIFFstats.setEnabled(False)
            self.openLensAberr.setEnabled(False)

        # print [str(name) for name in paths]

        if len(paths) > 0:

            try:

                # self.removeItemFromView()

                self.openLensAberr.setEnabled(True)

                self.params.save_setting('rootfolder', os.path.dirname(
                    str(paths[0])))  # guarda donde esta el root del trabajo para proximos archivos

                self.imgFileName = str(paths[0])

                im = ImgTransformClass(str(paths[0]), profile_path=False)

                self.imMode = im.mode

                self.imgWidth = im.width
                self.imgHeight = im.height

                if self.imMode   == "CMYK":
                    return AppWarningsClass.critical_warn("CMYK files are not allowed, only RGB")

                if "16" in self.imMode :
                    return AppWarningsClass.critical_warn("Only 8bits images are allowed, 16 Bit Depth currrently not supported")

                self.camerainfo.set_camera_information(self.imgFileName)
                self.footer_advice(self.credits, "info")

                self.myImage2 = im.image_previsualization()
                img_sizing = im.get_ratio_transform()
                self.ratio = img_sizing[7]

                self.getImage.setPixmap(self.myImage2)
                self.getImage.update()

                if (img_sizing[2] != self.x_orig) and (img_sizing[3] != self.y_orig):
                    # solo se resetea si varia el tamaño de la imagen porque al cambiar el layout falla removeItemView
                    self.x_orig = img_sizing[4]
                    self.y_orig = img_sizing[5]
                    self.remove_item_from_layout()
                    self.reset_layout()
                    self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 140, img_sizing[4], img_sizing[5]))
                    # self.layoutGeometry(im)

                info = GetImgInfo(str(paths[0]))

                self.label.setText(info.get_icc_info()['fileName'] + " (" + info.get_icc_info()['blanco'] + ")")
                self.label_2.setText(info.image_name())
                self.label_2.repaint()  # esto es para que actualice el label sino no aparecen los cambios

            except:

                error = traceback.format_exc()
                print(error)
                dialog = QtWidgets.QDialog()
                dialog.ui = log_Dialog(error)
                dialog.ui.setupUi(dialog)
                dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
                dialog.exec_()

    def layout_geometry(self, im):

        img_sizing = im.get_ratio_transform()
        self.correctionFactor = img_sizing[7]
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 140, img_sizing[4], img_sizing[5]))

    def get_cgats(self):

        qfd = QtWidgets.QFileDialog()
        if self.params.setting_contains("rootfolderCGATS"):
            path = self.params.setting_restore("rootfolderCGATS")
            # print(path)
        else:
            path = ""
        filter = "Images (*.txt *.cie)"
        title = "GET CGATS"
        fname = QtWidgets.QFileDialog.getOpenFileName(qfd, title, path, filter)[0]
        # print( fname)
        if os.path.isfile(fname):
            self.params.save_setting('rootfolderCGATS', os.path.dirname(str(fname)))
            self.CEGATSpath = str(fname)
            self.label_3.setText(os.path.basename(self.CEGATSpath))


    def get_icc_files(self):

        if self.iccFolder is None:
            return AppWarningsClass.informative_warn(
                "ICC Folder not found, set your path at settings dialog and restart")

        arr_icc = [x for x in os.listdir(self.iccFolder) if x.endswith(".icc")]

        arr_scnr = ["---"]
        for p in arr_icc:
            icc_path = os.path.join(self.iccFolder, p)
            if Path(icc_path).stat().st_size > 0:
                try:
                    #puede haber perfiles corruptos!
                    ICC = ImageCms.ImageCmsProfile( icc_path )
                    # hay que usar la versión 3.2.0 de PIL
                    if hasattr(ICC.profile, 'device_class'):
                        if ICC.profile.device_class == "scnr":
                            arr_scnr.append(p)
                except OSError as error:
                    AppWarningsClass.critical_warn(str(error) + str(icc_path))

        self.comboBox_2.addItems(arr_scnr)

    def make_ruler(self):

        #self.plotRoi = pg.LineSegmentROI([[self.X_ROI, self.Y_ROI], [self.X_ROI+50, self.Y_ROI+50]], pen=pg.mkPen(width=4.5, color='b'))

        self.ruleRoi = pg.LineROI([20,20], [200, 20], width=1, pen=pg.mkPen(width=4.5, color='b'))
        self.graphicsView.addItem(self.ruleRoi)

        self.ruleRoi.removeHandle( self.ruleRoi.handles[2]['item'])

        self.ruleRoi.sigRegionChanged.connect(self.rule_state)

    def make_roi(self, WIDTH_ROI, HIGHT_ROI):

        # self.plotRoi = pg.ROI([0,0], [230,150],pen=pg.mkPen(width=4.5, color='r'))
        self.plotRoi = pg.ROI([self.X_ROI, self.Y_ROI], [WIDTH_ROI, HIGHT_ROI], pen=pg.mkPen(width=4.5, color='r'))

        self.graphicsView.addItem(self.plotRoi)

        lock = self.chars.is_lock(self.chartIndex)

        self.plotRoi.addScaleHandle([1, 1], [0, 0], lockAspect=lock)
        self.plotRoi.addScaleHandle([0, 0], [1, 1], lockAspect=lock)
        self.plotRoi.addScaleHandle([1, 0], [0, 1], lockAspect=lock)
        self.plotRoi.addScaleHandle([0, 1], [1, 0], lockAspect=lock)
        self.plotRoi.addRotateHandle([1, 0.5], [0.5, 0.5])

        self.plotRoi.sigRegionChanged.connect(self.get_lastState)

    def rule_state(self):

        size_x, size_y = self.ruleRoi.lastState["size"]
        #print("angle:", self.ruleRoi.lastState["angle"])

        self.rule_distance = int( size_x * self.ratio)

        self.label_coordinates.setText(str(self.rule_distance)+"px")

        #print("SizeRatio:", self.rule_distance )

    def get_lastState(self):

        self.pos_x, self.pos_y = self.plotRoi.lastState["pos"]
        self.angle = self.plotRoi.lastState["angle"]
        self.size_x, self.size_y = self.plotRoi.lastState["size"]
        # print( str(self.pos_x)+","+str(self.pos_y)+" ; "+str(self.size_x)+","+str(self.size_y))

        isRoi = self.chars.is_roi(self.chartIndex)

        if isRoi:
            self.change_roi()
        else:
            self.change_pattern()

    def change_roi(self):

        self.roi_pos_x = self.pos_x  # *self.correctionFactor
        self.roi_pos_y = self.pos_y  # *self.correctionFactor

        self.roi_width = self.size_x  # *self.correctionFactor
        self.roi_height = self.size_y  # *self.correctionFactor

        self.roiCoordinates = [self.roi_pos_x, self.roi_pos_y, self.roi_pos_x + self.roi_width,
                               self.roi_pos_y + self.roi_height]
        #print(self.roiCoordinates)

    def change_pattern(self):
        """
        Para revisar o mejorar:
        t.translate mueve desde la posición relativa, al pasarle las coordendas del ROI que son absolutas
        fuerza al conjunto de parches a desplazarse de forma incoherente al restarle self.X_ROI se corrige con valores negativos
        pero la escala y rotación dejan de funcionar
        """

        t = QtGui.QTransform()
        t.translate(self.pos_x - self.X_ROI, self.pos_y - self.Y_ROI)
        # print( str(self.pos_x - self.X_ROI)+","+str(self.pos_y - self.Y_ROI)  )
        s_factor = self.size_x / self.WIDTH_ROI
        t.scale(s_factor, s_factor)
        t.rotate(self.angle)
        self.simb.setTransform(t)

        # print( "--- Posiciones reales ---" )
        pos = []
        for x, y in self.simb.pos:
            # https://doc.qt.io/qt-5/qtransform.html
            x1 = (t.m11() * x + t.m21() * y + t.m31())  # *self.correctionFactor
            y1 = (t.m22() * y + t.m12() * x + t.m32())  # *self.correctionFactor
            a = [x1, y1]
            pos.append(a)
            # print( str(x1)+","+str(y1) )
        self.coordenadasReales = pos  ##esto es lo que le paso al home.py

    def roi_pattern(self, chartVars):

        self.simb = pg.GraphItem()
        self.simb.setData(pos=chartVars[0], size=chartVars[2], symbol=chartVars[1], pxMode=False)
        self.simb.setOpacity(0.5)
        self.graphicsView.addItem(self.simb)

    def footer_advice(self, msg, type):

        if type == "info":
            color = "color: rgb(155, 155, 155)"
        elif type == "err":
            color = "color: rgb(200, 0, 0)"

        self.label_footer.setStyleSheet(color)
        self.label_footer.setText(_translate("Dialog", msg, None))


"""

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QMainWindow()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())
"""
