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


class FallOffUI(object):

    def __init__(self, imgStats, img):
        self.imgStats = imgStats

        # se rota la imagen porque en la representación se cambian los ejes
        self.np_im = np.rot90(img, 3)

    def setupUi(self, falloff_dialog):

        falloff_dialog.setObjectName("Dialog")
        falloff_dialog.setFixedSize(478, 550)
        falloff_dialog.setWindowTitle(_translate("ImageQA", "ImageQA Light Falloff", None))

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
        self.btExportar.clicked.connect(lambda state, y="neutrallity", x=self.graphicsView: self.export_graph(y, x))

        self.toolButton_2 = QtWidgets.QToolButton(falloff_dialog)
        self.toolButton_2.setGeometry(QtCore.QRect(410, 320, 51, 41))
        self.toolButton_2.setObjectName("report")
        self.toolButton_2.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('report_64px.png')))
        self.toolButton_2.setIconSize(QtCore.QSize(40, 40))
        self.toolButton_2.setEnabled(False)

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

        #promedio = self.imgStats["mean"]
        #min = self.imgStats["min"]
        #max = self.imgStats["max"]

        #desviacion = (max - min) / promedio
        #print(desviacion)

        self.getImage = pg.ImageItem()
        self.getImage.setImage(self.np_im)

        self.graphicsView.addItem(self.getImage)

        '''
        #esto es para representar la imagen con isolineas
        self.my_dict = {}
        i = 0
        for x in range(min, max, 10):
            if (x < promedio):
                color = 'g'
            elif (x > promedio):
                color = 'b'
            self.my_dict[i] = pg.IsocurveItem(level=x, pen=color)
            self.my_dict[i].setParentItem(self.getImage)
            self.my_dict[i].setData(pg.gaussianFilter(self.np_im, (2, 2)))
            i += 1

        c = pg.IsocurveItem(level=promedio, pen='r')
        c.setParentItem(self.getImage)
        c.setData(pg.gaussianFilter(self.np_im, (2, 2)))
        '''
        self.label.setText(self.print_stats_rgb(self.imgStats))
        self.label2.setText(self.print_stats_lab(self.imgStats))

    def print_stats_rgb(self, stats):

        o = "<p style=\"line-height:120%; font-size:16px; color:#666\">"
        o += "<italic style=\"font-size:14px; color:#666\">RGB </italic> <strong>Mean:</strong> " + str(
            round(stats['mean'], 1)) + "<italic style=\"font-size:12px; color:#666\">cv</italic><br>"
        o += "<italic style=\"font-size:14px; color:#666\">RGB </italic> <strong>Desv:</strong> " + str(
            round(stats['desv'], 1)) + "<italic style=\"font-size:12px; color:#666\">cv</italic><br>"
        o += "<italic style=\"font-size:14px; color:#666\">RGB </italic> <strong>Max:</strong> " + str(
            round(stats['max'], 1)) + "<italic style=\"font-size:12px; color:#666\">cv</italic><br>"
        o += "<italic style=\"font-size:14px; color:#666\">RGB </italic> <strong>Min:</strong> " + str(
            round(stats['min'], 1)) + "<italic style=\"font-size:12px; color:#666\">cv</italic><br>"
        o += "<strong>SNR:</strong> " + str(
            round(stats['snr'], 1)) + "<italic style=\"font-size:12px; color:#666\">db</italic><br>"
        o += "<strong>Non</strong> <span style=\"font-size:12px; color:#666\">Uniformity:</span> " + str(
            round(stats['NonUniformity'], 1)) + "<italic style=\"font-size:12px; color:#666\">%</italic><br>"

        o += "</p>"
        return o

    def print_stats_lab(self, stats):

        o = "<p style=\"line-height:120%; font-size:16px; color:#666\">"
        o += "<italic style=\"font-size:14px; color:#666\">L </italic><strong>Mean:</strong> " + str(
            round(stats['l_mean'], 1)) + "<br>"

        o += "<italic style=\"font-size:14px; color:#666\">L </italic><strong>Desv:</strong> " + str(
            round(stats['l_desv'], 1)) + "<br>"

        o += "<italic style=\"font-size:14px; color:#666\">C </italic><strong>Mean:</strong> " + str(
            round(stats['c_mean'], 1)) + "<br>"

        o += "<italic style=\"font-size:14px; color:#666\">C </italic><strong>Desv:</strong> " + str(
            round(stats['c_desv'], 1)) + "<br>"

        o += "<strong>Samples</strong> " + str(
            round(stats['nPxLab'], 1)) + "<italic style=\"font-size:12px; color:#666\">pixels</italic><br>"

        o += "</p>"
        return o

    def export_graph(self, key, plot):
        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save Image')
        # print(fname)
        if fname != "":
            timestr = time.strftime("%Y%m%d-%H%M%S")
            exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
            exporter.parameters()['width'] = 800  # (note this also affects height parameter)
            exporter.export(fname + "/" + key + "_" + str(timestr) + '.png')
