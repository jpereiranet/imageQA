# -*- coding: utf-8 -*-

import time
from io import BytesIO

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PIL import Image
from PyQt5 import QtCore, QtGui

from app_paths import DefinePathsClass
from plist_set import ProcessSettingsClass
from save_report import saveReportToFileClass
from table_stats_guid import TableStatsUI

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


class caberrationUI(object):

    def __init__(self, valoresDE):
        self.valoresDE = valoresDE

    def setupUi(self, DeltaDialog):

        self.params = ProcessSettingsClass()

        DeltaDialog.setObjectName(_fromUtf8("DeltaDialog"))
        DeltaDialog.setFixedSize(789, 491)
        DeltaDialog.setWindowTitle(_translate("ImageQA", "ImageQA Delta-e", None))

        self.horizontalLayoutWidget = QtGui.QWidget(DeltaDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 440, 291, 32))
        self.horizontalLayoutWidget.setObjectName(_fromUtf8("horizontalLayoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.horizontalLayoutWidget)
        # self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))

        self.btCerrar = QtGui.QToolButton(self.horizontalLayoutWidget)
        self.btCerrar.setGeometry(QtCore.QRect(0, 0, 30, 30))
        self.btCerrar.setObjectName(_fromUtf8("btCerrar"))
        self.btCerrar.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('close_64px.png')))
        self.btCerrar.setIconSize(QtCore.QSize(30, 30))
        self.btCerrar.setToolTip("Close")

        self.tabWidget = QtGui.QTabWidget(DeltaDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 761, 391))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))

        i = 0

        for key, value in self.valoresDE:

            self.my_dict = {}
            x = "tab_" + str(i)
            y = "horizontalLayoutWidget_" + str(i)
            z = "horizontalLayout_" + str(i)
            v = "verticalLayoutWidget_" + str(i)
            l = "verticalLayout_" + str(i)
            bt1 = "toolButton1_" + str(i)
            bt2 = "toolButton2_" + str(i)
            bt3 = "toolButton3_" + str(i)
            # g = "graphicsView_"+str(i)
            a = "label_" + str(i)

            nameTab = key
            objName = "LensDialog_" + key

            self.my_dict[x] = QtGui.QWidget()
            self.my_dict[x].setObjectName(_fromUtf8("tab_2"))
            self.my_dict[y] = QtGui.QWidget(self.my_dict[x])
            self.my_dict[y].setGeometry(QtCore.QRect(0, 300, 731, 60))
            self.my_dict[y].setObjectName(_fromUtf8("horizontalLayoutWidget_3"))
            self.my_dict[z] = QtGui.QHBoxLayout(self.my_dict[y])
            # self.my_dict[z].setMargin(0)
            self.my_dict[z].setObjectName(_fromUtf8("horizontalLayout_3"))
            self.my_dict[a] = QtGui.QLabel(self.my_dict[y])
            self.my_dict[a].setObjectName(_fromUtf8("label_5"))
            self.my_dict[a].setWordWrap(True);
            self.my_dict[z].addWidget(self.my_dict[a])
            self.my_dict[v] = QtGui.QWidget(self.my_dict[x])
            self.my_dict[v].setGeometry(QtCore.QRect(0, 0, 741, 291))
            self.my_dict[v].setObjectName(_fromUtf8("verticalLayoutWidget_2"))
            self.my_dict[l] = QtGui.QVBoxLayout(self.my_dict[v])
            # self.my_dict[l].setMargin(0)
            self.my_dict[l].setObjectName(_fromUtf8("verticalLayout_2"))

            self.my_dict[bt1] = QtGui.QToolButton(self.my_dict[x])
            self.my_dict[bt1].setGeometry(QtCore.QRect(710, 310, 41, 41))
            self.my_dict[bt1].setObjectName(_fromUtf8("toolButton"))
            self.my_dict[bt1].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('report_64px.png')))
            self.my_dict[bt1].setIconSize(QtCore.QSize(40, 40))

            self.my_dict[bt2] = QtGui.QToolButton(self.my_dict[x])
            self.my_dict[bt2].setGeometry(QtCore.QRect(660, 310, 41, 41))
            self.my_dict[bt2].setObjectName(_fromUtf8("toolButton_2"))
            self.my_dict[bt2].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('pictures_64px.png')))
            self.my_dict[bt2].setIconSize(QtCore.QSize(40, 40))

            self.my_dict[bt3] = QtGui.QToolButton(self.my_dict[x])
            self.my_dict[bt3].setGeometry(QtCore.QRect(610, 310, 41, 41))
            self.my_dict[bt3].setObjectName(_fromUtf8("toolButton_3"))
            self.my_dict[bt3].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('table_64px.png')))
            self.my_dict[bt3].setIconSize(QtCore.QSize(30, 30))

            self.my_dict[bt1].setEnabled(False)
            self.my_dict[bt3].setEnabled(False)

            if key == "VISUAL-CABG" or key == "VISUAL-CARG" or key == "VISUAL-DIST":
                plot = self.print_image(i, value, key)

            if key == "CARG":
                plot = self.print_ca_plot(i, value, "caBRG")
                self.my_dict[a].setText(self.print_stats(value["stats"], key))

            if key == "CABGr":
                plot = self.print_ca_plot(i, value, "caBRGr")
                self.my_dict[a].setText(self.print_stats_r(value["stats"], key))

            if key == "DISTORTION":
                plot = self.print_distortion_plot(i, value, key)
                self.my_dict[a].setText(self.print_stats_dist(value["stats"], key))

                # print(key)
                # print(value[0])

            self.my_dict[l].addWidget(plot)
            # self.my_dict[bt2].clicked.connect(lambda: self.exportGraph(plot,key))

            self.my_dict[bt2].clicked.connect(lambda state, y=key, x=plot: self.export_graph(y, x))
            self.my_dict[bt1].clicked.connect(lambda state, y=value, x=key: self.export_list(y, x))
            self.my_dict[bt3].clicked.connect(lambda state, y=value, x=key: self.open_data_table_ui(y, x))

            # exportList(self, list, key)

            # self.my_dict[bt1].clicked.connect(lambda: self.exportGraph(plotBars,key))

            tabId = "tab_" + str(i)
            self.tabWidget.addTab(self.my_dict[x], _fromUtf8(tabId))
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_dict[x]), _translate(objName, nameTab, None))

            i += 1

        self.tabWidget.setCurrentIndex(0)

        # QtCore.QObject.connect(self.btCerrar, QtCore.SIGNAL(_fromUtf8("clicked()")), DeltaDialog.close)
        self.btCerrar.clicked.connect(DeltaDialog.close)
        QtCore.QMetaObject.connectSlotsByName(DeltaDialog)

    def open_data_table_ui(self, value, key):

        dialog = QtGui.QDialog()
        dialog.ui = TableStatsUI(value, key, None)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def export_list(self, value, key):

        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")
            #print(path)

        fname = QtGui.QFileDialog.getExistingDirectory(None, 'Choose a directory for save list', path,
                                                       QtGui.QFileDialog.ShowDirsOnly)
        if fname != "":
            saveReportToFileClass(value, fname, key)
            self.params.save_setting('rootfolderSAVE', str(fname))

    def export_graph(self, key, plot):
        """
        al llamar a pyqtgraph/exporters/ImageExporter.py en la linea 70 hay que forzar a INT las variables width y height
        int(self.params['width']), int(self.params['height'])
        """
        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")


        fname = QtGui.QFileDialog.getExistingDirectory(None, 'Choose a directory for save Image', path,
                                                       QtGui.QFileDialog.ShowDirsOnly)

        if fname != "":

            timestr = time.strftime("%Y%m%d-%H%M%S")
            exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
            exporter.parameters()['width'] = 800  # (note this also affects height parameter)
            exporter.export(fname + "/" + key + "_" + timestr + '.png')
            self.params.save_setting('rootfolderSAVE', str(fname))

    def print_stats_dist(self, value, mode):

        o = ""
        o = o + "<strong>Distortion</strong>: " + str(value["KIND"])+"<br>"
        o = o + "<strong>Max</strong>: " + str(value["MAX"])

        return "<p style=\"line-height:90%; font-size:16px; color:#666\">" + o + "</p>"

    def print_stats(self, value, mode):

        o = ""
        o = o + "<strong>BG Max</strong>: " + str(value["BG_Max"])+"<br>"
        o = o + "<strong>RG Max</strong>: " + str(value["RG_Max"])

        return "<p style=\"line-height:90%; font-size:16px; color:#666\">" + o + "</p>"

    def print_stats_r(self, value, mode):

        o = ""
        o = o + "<strong>Radial BG Max</strong>: " + str(value["BGr_Max"])+"<br>"
        o = o + "<strong>Radial RG Max</strong>: " + str(value["RGr_Max"])

        return "<p style=\"line-height:90%; font-size:16px; color:#666\">" + o + "</p>"


    def print_distortion_plot(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].setObjectName(_fromUtf8("plot"))

        newxdic = {0: "0%", 1: "20%", 2: "40%", 3: "60%", 4: "80%", 5: "100%"}
        stringaxis = self.my_plot[x].getAxis('bottom')
        stringaxis.setTicks([newxdic.items()])

        self.my_plot[x].setLabel('left', 'Delta', units='')
        self.my_plot[x].setLabel('bottom', 'Image Diagonal', units='')


        self.my_plot[x].plot(values["curve"], pen='w', symbol='o', symbolPen='w', symbolBrush=0.5, name='Red')

        return self.my_plot[x]

    def print_ca_plot(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].setObjectName(_fromUtf8("plot"))

        newxdic = {0: "0%", 1: "10%", 2: "20%", 3: "30%", 4: "40%", 5: "50%", 6: "60%", 7: "70%", 8: "80%", 9: "90%", 10: "100%"}
        stringaxis = self.my_plot[x].getAxis('bottom')
        stringaxis.setTicks([newxdic.items()])

        self.my_plot[x].setLabel('left', 'Delta', units='')
        self.my_plot[x].setLabel('bottom', 'Image Diagonal', units='')

        #self.my_plot[x].setAspectLocked(True)

        if mode == "caBRG":

            self.my_plot[x].plot(values["caBG"], pen='b', symbol='o', symbolPen='b', symbolBrush=0.5, name='Red')
            self.my_plot[x].plot(values["caRG"], pen='r', symbol='s', symbolPen='r', symbolBrush=0.5, name='Green')

        if mode == "caBRGr":
            self.my_plot[x].plot(values["caBGr"], pen='b', symbol='o', symbolPen='b', symbolBrush=0.5, name='Red')
            self.my_plot[x].plot(values["caRGr"], pen='r', symbol='s', symbolPen='r', symbolBrush=0.5, name='Green')

        return self.my_plot[x]
        # self.verticalLayout.addWidget(self.graphicsView)

    def print_image(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setAspectLocked(True)
        self.my_plot[x].setLabel('left', 'Pixels', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')

        self.getImage = pg.ImageItem()
        self.getImage.setImage(values)

        self.getImage = pg.ImageItem()

        self.getImage.setImage(np.rot90(values, 3))

        self.my_plot[x].addItem(self.getImage)

        return self.my_plot[x]

