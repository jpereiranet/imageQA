# -*- coding: utf-8 -*-

import time

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PyQt5 import QtCore, QtGui, QtWidgets

from app_paths import DefinePathsClass

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class ImgDiffGui(object):

    def __init__(self, imgStats, img):
        self.imgStats = imgStats

        # se rota la imagen porque en la representación se cambian los ejes
        self.np_im = np.rot90(img, 3)

    def setupUi(self, falloff_dialog):

        falloff_dialog.setObjectName("Dialog")
        falloff_dialog.setFixedSize(478, 550)
        falloff_dialog.setWindowTitle(_translate("ImageQA", "ImageQA image diff", None))

        self.btCerrar = QtWidgets.QToolButton(falloff_dialog)
        self.btCerrar.setGeometry(QtCore.QRect(20, 480, 30, 30))
        self.btCerrar.setObjectName("btCerrar")
        self.btCerrar.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('close_64px.png')))
        self.btCerrar.setIconSize(QtCore.QSize(30, 30))
        self.btCerrar.setToolTip("Close")

        self.verticalLayoutWidget = QtWidgets.QWidget(falloff_dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 441, 291))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)

        self.verticalLayout.setObjectName("verticalLayout")

        ##--- GraphicsView (visor de imagenes )
        # self.graphicsView = pg.GraphicsView( useOpenGL=False, background='k')
        # self.graphicsView.setObjectName("graphicsView")
        # self.verticalLayout.addWidget(self.graphicsView)

        self.graphicsView = pg.PlotWidget(name='Plot1')
        self.graphicsView.setLabel('left', 'Pixels', units='')
        self.graphicsView.setLabel('bottom', 'Pixels', units='')

        self.verticalLayout.addWidget(self.graphicsView)

        self.verticalLayoutWidget_2 = QtWidgets.QWidget(falloff_dialog)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(20, 320, 321, 161))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")

        self.verticalLayout_2 = QtWidgets.QHBoxLayout(self.verticalLayoutWidget_2)

        self.verticalLayout_2.setObjectName("verticalLayout_2")

        self.btExportar = QtWidgets.QToolButton(falloff_dialog)
        self.btExportar.setGeometry(QtCore.QRect(350, 320, 51, 41))
        self.btExportar.setObjectName("Export")
        self.btExportar.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('pictures_64px.png')))
        self.btExportar.setIconSize(QtCore.QSize(40, 40))
        self.btExportar.clicked.connect(lambda state, y="SSIM-MAP", x=self.graphicsView: self.export_graph(y, x))
        '''
        self.toolButton_2 = QtWidgets.QToolButton(falloff_dialog)
        self.toolButton_2.setGeometry(QtCore.QRect(410, 320, 51, 41))
        self.toolButton_2.setObjectName("report")
        self.toolButton_2.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('report_64px.png')))
        self.toolButton_2.setIconSize(QtCore.QSize(40, 40))
        self.toolButton_2.setEnabled(False)
        '''

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)

        self.label2 = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.label2.setObjectName("label2")
        self.verticalLayout_2.addWidget(self.label2)

        QtCore.QMetaObject.connectSlotsByName(falloff_dialog)

        self.btCerrar.clicked.connect(falloff_dialog.close)
        self.get_previsualization_image()

    def get_previsualization_image(self):

        self.getImage = pg.ImageItem()
        self.getImage.setImage(self.np_im)

        self.graphicsView.addItem(self.getImage)

        self.graphicsView.setAspectLocked(True)

        self.label.setText(self.print_stats_rgb(self.imgStats))
        self.label2.setText(self.print_stats_lab(self.imgStats))

    def print_stats_rgb(self, stats):

        o = "<p style=\"line-height:120%; font-size:16px; color:#666\">"
        o += "<strong>SSIM:</strong> " + str(
            round(stats['ssim'], 1)) + "<italic style=\"font-size:12px; color:#666\"></italic><br>"
        o += "<strong>MSE:</strong> " + str(
            round(stats['mse'], 1)) + "<italic style=\"font-size:12px; color:#666\"></italic><br>"
        o += "<strong>PSNR:</strong> " + str(
            round(stats['psnr'], 1)) + "<italic style=\"font-size:12px; color:#666\">db</italic><br>"
        o += "<strong>RMSE:</strong> " + str(
            round(stats['rmse'], 1)) + "<italic style=\"font-size:12px; color:#666\"></italic><br>"
        #o += "<strong>Sample:</strong>  <span style=\"font-size:12px; color:#666\">"+stats['sizeSample'][3]+"</span> "  + str(
        #    stats['sizeSample'][0])+"x"+str(stats['sizeSample'][1]) +" "+ str(stats['sizeSample'][2])+ "Kb<br>"
        #o += "<strong>Reference</strong> <span style=\"font-size:12px; color:#666\">"+stats['sizeReference'][3]+"</span> " + str(
        #    stats['sizeReference'][0])+"x"+str(stats['sizeReference'][1]) +" "+ str(stats['sizeReference'][2])+ "Kb<br>"

        o += "</p>"
        return o

    def print_stats_lab(self, stats):

        o = "<p style=\"line-height:120%; font-size:16px; color:#666\">"
        o += "<strong>Sample:</strong><br>" \
            "<span style=\"font-size:12px; color:#666\">" + stats['sizeSample'][3] + "</span><br>" \
             "<span style=\"font-size:12px; color:#666\">"+ str(stats['sizeSample'][0]) + "x" + str(stats['sizeSample'][1])+"p</span> " \
             "<span style=\"font-size:12px; color:#666\">" + str(stats['sizeSample'][2]) + "Kb</span><br>" \

        o += "<strong>Reference</strong><br>" + \
            "<span style=\"font-size:12px; color:#666\">"+ stats['sizeReference'][3] + "</span><br>" \
            "<span style=\"font-size:12px; color:#666\">"+ str(stats['sizeReference'][0]) + "x" + str(stats['sizeReference'][1]) + "p</span> " \
            "<span style=\"font-size:12px; color:#666\">"+ str(stats['sizeReference'][2]) + "Kb</span><br>" \

        o += "</p>"
        return o

    def export_graph(self, key, plot):
        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save Image')
        # print(fname)
        if fname is not "":
            timestr = time.strftime("%Y%m%d-%H%M%S")
            exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
            exporter.parameters()['width'] = 800  # (note this also affects height parameter)
            exporter.export(fname + "/" + key + "_" + str(timestr) + '.png')