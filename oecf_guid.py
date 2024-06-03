# -*- coding: utf-8 -*-
import time
from io import BytesIO

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

from app_paths import DefinePathsClass
from plist_set import ProcessSettingsClass
from save_report import saveReportToFileClass
from table_stats_guid import TableStatsUI

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class GetOECFUI(object):

    def __init__(self, de_values):
        #self.patchName = self.get_patch_name(ref_values)
        #.densityName = self.get_density_name(ref_values)
        #self.RGBvalues = rgb_values
        self.valoresDE = de_values
        #self.ref_values = ref_values
    '''
    def get_patch_name(self, reference):
        patchName = []
        for patch in reference:
            patchName.append(patch["SAMPLE_ID"])
        return patchName

    def get_density_name(self, reference):
        patchName = []
        for patch in reference:
            patchName.append(patch["D_VIS"])

        patchName.sort()
        return patchName
    '''


    def setupUi(self, OECFDialog):

        self.params = ProcessSettingsClass()

        OECFDialog.setObjectName("OECFDialog")
        OECFDialog.setFixedSize(789, 491)
        OECFDialog.setWindowTitle(_translate("ImageQA", "ImageQA OECF", None))

        self.horizontalLayoutWidget = QtWidgets.QWidget(OECFDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 440, 291, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)

        self.horizontalLayout.setObjectName("horizontalLayout")

        self.btCerrar = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.btCerrar.setGeometry(QtCore.QRect(0, 0, 30, 30))
        self.btCerrar.setObjectName("btCerrar")
        self.btCerrar.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('close_64px.png')))
        self.btCerrar.setIconSize(QtCore.QSize(30, 30))
        self.btCerrar.setToolTip("Close")

        self.tabWidget = QtWidgets.QTabWidget(OECFDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 761, 391))
        self.tabWidget.setObjectName("tabWidget")

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
            objName = "OECFDialog_" + key

            self.my_dict[x] = QtWidgets.QWidget()
            self.my_dict[x].setObjectName("tab_2")
            self.my_dict[y] = QtWidgets.QWidget(self.my_dict[x])
            self.my_dict[y].setGeometry(QtCore.QRect(0, 300, 731, 60))
            self.my_dict[y].setObjectName("horizontalLayoutWidget_3")
            self.my_dict[z] = QtWidgets.QHBoxLayout(self.my_dict[y])

            self.my_dict[z].setObjectName("horizontalLayout_3")
            self.my_dict[a] = QtWidgets.QLabel(self.my_dict[y])
            self.my_dict[a].setObjectName("label_5")
            self.my_dict[a].setWordWrap(True);
            # self.my_dict[a].setText( self.printStats( value[0][1], key ) )
            self.my_dict[z].addWidget(self.my_dict[a])
            self.my_dict[v] = QtWidgets.QWidget(self.my_dict[x])
            self.my_dict[v].setGeometry(QtCore.QRect(0, 0, 741, 291))
            self.my_dict[v].setObjectName("verticalLayoutWidget_2")
            self.my_dict[l] = QtWidgets.QVBoxLayout(self.my_dict[v])

            self.my_dict[l].setObjectName("verticalLayout_2")

            self.my_dict[bt1] = QtWidgets.QToolButton(self.my_dict[x])
            self.my_dict[bt1].setGeometry(QtCore.QRect(710, 310, 41, 41))
            self.my_dict[bt1].setObjectName("toolButton")
            self.my_dict[bt1].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('report_64px.png')))
            self.my_dict[bt1].setIconSize(QtCore.QSize(40, 40))

            self.my_dict[bt2] = QtWidgets.QToolButton(self.my_dict[x])
            self.my_dict[bt2].setGeometry(QtCore.QRect(660, 310, 41, 41))
            self.my_dict[bt2].setObjectName("toolButton_2")
            self.my_dict[bt2].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('pictures_64px.png')))
            self.my_dict[bt2].setIconSize(QtCore.QSize(40, 40))

            self.my_dict[bt3] = QtWidgets.QToolButton(self.my_dict[x])
            self.my_dict[bt3].setGeometry(QtCore.QRect(610, 310, 41, 41))
            self.my_dict[bt3].setObjectName("toolButton_3")
            self.my_dict[bt3].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('table_64px.png')))
            self.my_dict[bt3].setIconSize(QtCore.QSize(30, 30))

            if key == "OECF" or key == "RED" or key == "GREEN" or key == "BLUE" or key == "L-OECF":
                # [[[[92.0, 96.0], [72.0, 79.0], [56.0, 64.0], [39.0, 47.0], [26.0, 33.0], [13.0, 19.0]], {'Err Min': '4.0', 'Err Average': '6.67', 'Err Max': '8.0', 'Err Desv': 1.0}]]
                plot = self.printDoubleLineChart(i, value, key)
                self.my_dict[a].setText(self.printStats(value["stats"], key))

            elif key == "DEV" or key == "WB" or key == "LGAIN":
                # [[[-0.06076036545392528, -0.12553088208385946, -0.18632134097921205, -0.2848811081320429, -0.33839640574312607, -0.5133144596125951], {'Err Min': '-0.51', 'Err Average': '-0.25', 'Err Max': '-0.06', 'Err Desv': 0.0}]]
                plot = self.printSimpleLineChart(i, value, key)

                self.my_dict[a].setText(self.printStats(value["stats"], key))
                # print(key)
                # print(value)

            elif key == "RGB":
                # [[[[236.1, 245.0], [186.8, 200.0], [143.51, 161.0], [100.23, 121.0], [66.06, 82.0], [34.95, 49.0]], {'Err Min': '8.9', 'Err Average': '15.06', 'Err Max': '20.77', 'Err Desv': 4.0}]]
                plot = self.printTripleLineChart(i, value, key)

                self.my_dict[a].setText(self.printStats(value["stats"], key))
                # print(key)
                # print(value)

            elif key == "ROI" or key == "VISUAL":

                plot = self.printImage(i, value, key)
                self.my_dict[bt1].setEnabled(False)
                self.my_dict[bt3].setEnabled(False)

            self.my_dict[l].addWidget(plot)
            # self.my_dict[bt2].clicked.connect(lambda: self.exportGraph(plot,key))

            self.my_dict[bt2].clicked.connect(lambda state, y=key, x=plot: self.exportGraph(y, x))
            self.my_dict[bt1].clicked.connect(lambda state, y=value, x=key: self.exportList(y, x))
            self.my_dict[bt3].clicked.connect(lambda state, y=value, x=key: self.openTableData(y, x))

            # exportList(self, list, key)

            # self.my_dict[bt1].clicked.connect(lambda: self.exportGraph(plotBars,key))

            tabId = "tab_" + str(i)
            self.tabWidget.addTab(self.my_dict[x], tabId)
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_dict[x]), _translate(objName, nameTab, None))

            i += 1

        self.tabWidget.setCurrentIndex(0)

        self.btCerrar.clicked.connect(OECFDialog.close)

        QtCore.QMetaObject.connectSlotsByName(OECFDialog)

    def openTableData(self, value, key):

        dialog = QtWidgets.QDialog()
        dialog.ui = TableStatsUI(value, key, None)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def exportGraph(self, key, plot):

        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")

        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save Image', path,
                                                           QtWidgets.QFileDialog.ShowDirsOnly)

        # fname = QtGui.QFileDialog.getExistingDirectory(None,'Choose a directory for save Image')
        # print(fname)
        if fname != "":

            timestr = time.strftime("%Y%m%d-%H%M%S")
            exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
            #exporter.parameters()['width'] = 800  # (note this also affects height parameter)
            exporter.params['width'] = 717
            exporter.export(fname + "/" + key + "_" + timestr + '.png')
            self.params.save_setting('rootfolderSAVE', str(fname))

    def exportList(self, value, key):

        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")

        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save list', path,
                                                           QtWidgets.QFileDialog.ShowDirsOnly)

        if fname != "":
            saveReportToFileClass(value, fname, key)
            self.params.save_setting('rootfolderSAVE', str(fname))

    def printStats(self, stats, mode):

        o = ""
        i = 0
        unit = stats["units"]
        for key, value in sorted(stats.items()):
            if key != "units":
                if i > 2:
                    o = o + "<br>"
                    i = 0
                o = o + "<strong>" + key + "</strong>: " + str(
                    value) + "<italic style=\"font-size:12px; color:#666\">" + unit + "</italic>&nbsp;&nbsp;&nbsp;&nbsp;"
                i = i + 1

        return "<p style=\"line-height:100%; font-size:16px; color:#666\">" + o + "</p>"

    def printDoubleLineChart(self, index, values, mode):

        xdict = dict(enumerate(values["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        if mode == "OECF":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)

            colorA = QtGui.QPen(QtGui.QColor(120, 120, 120), 0, QtCore.Qt.SolidLine)
            colorB = QtGui.QPen(QtGui.QColor(220, 220, 220), 0, QtCore.Qt.SolidLine)

        elif mode == "L-OECF":
            self.my_plot[x].setLabel('left', 'Lightness', units='L*')
            self.my_plot[x].setYRange(0, 100)

            colorA = QtGui.QPen(QtGui.QColor(255, 0, 0), 0, QtCore.Qt.SolidLine)
            colorB = QtGui.QPen(QtGui.QColor(255, 200, 200), 0, QtCore.Qt.SolidLine)

        elif mode == "RED":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)

            colorA = QtGui.QPen(QtGui.QColor(255, 0, 0), 0, QtCore.Qt.SolidLine)
            colorB = QtGui.QPen(QtGui.QColor(255, 200, 200), 0, QtCore.Qt.SolidLine)

        elif mode == "GREEN":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)

            colorA = QtGui.QPen(QtGui.QColor(0, 255, 0), 0, QtCore.Qt.SolidLine)
            colorB = QtGui.QPen(QtGui.QColor(200, 255, 200), 0, QtCore.Qt.SolidLine)

        elif mode == "BLUE":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)

            colorA = QtGui.QPen(QtGui.QColor(0, 0, 255), 0, QtCore.Qt.SolidLine)
            colorB = QtGui.QPen(QtGui.QColor(200, 200, 255), 0, QtCore.Qt.SolidLine)

        self.my_plot[x].setLabel('bottom', 'Optical Density', units='D')

        self.my_plot[x].addLegend()

        # l = pg.LegendItem((100,60), offset=(70,30))  # args are (size, offset)
        # l.setParentItem(plt.graphicsItem())   # Note we do NOT call plt.addItem in this case

        o = []
        i = []

        for y in values["curve"]:
            o.append(y[0])
            i.append(y[1])

        self.my_plot[x].plot(o, pen=colorA, symbol='o', symbolPen=colorA, symbolBrush=0.5, name='Image')
        self.my_plot[x].plot(i, pen=colorB, symbol='o', symbolPen=colorB, symbolBrush=0.5, name='Reference')

        return self.my_plot[x]

    def printTripleLineChart(self, index, values, mode):

        xdict = dict(enumerate(values["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        if mode == "RGB":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)

        self.my_plot[x].setLabel('bottom', 'Optical Density', units='D')

        self.my_plot[x].addLegend()

        # l = pg.LegendItem((100,60), offset=(70,30))  # args are (size, offset)
        # l.setParentItem(plt.graphicsItem())   # Note we do NOT call plt.addItem in this case

        r = []
        g = []
        b = []

        for y in values["curve"]:
            r.append(y[0])
            g.append(y[1])
            b.append(y[2])

        self.my_plot[x].plot(r, pen='r', symbol='o', symbolPen='r', symbolBrush=0.5, name='Red')
        self.my_plot[x].plot(g, pen='g', symbol='s', symbolPen='g', symbolBrush=0.5, name='Green')
        self.my_plot[x].plot(b, pen='b', symbol='t', symbolPen='b', symbolBrush=0.5, name='Blue')

        return self.my_plot[x]

    def printSimpleLineChart(self, index, values, mode):

        xdict = dict(enumerate(values["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        if mode == "LGAIN":
            self.my_plot[x].setLabel('left', 'L* Gain Modulation', units='')
            self.my_plot[x].setLabel('bottom', 'Optical Density', units='OD')
            self.my_plot[x].setAspectLocked(True)
            legend = "Gain"
            self.my_plot[x].addLegend()

        if mode == "DEV":
            self.my_plot[x].setLabel('left', '∆ EV', units='')
            self.my_plot[x].setLabel('bottom', 'Optical Density', units='OD')
            self.my_plot[x].setAspectLocked(True)
            self.my_plot[x].addLegend()
            legend = "∆EV"

        if mode == "WB":
            self.my_plot[x].setLabel('left', '∆ C', units='')
            #self.my_plot[x].setLabel('bottom', 'Patch', units='')
            self.my_plot[x].setAspectLocked(True)
            self.my_plot[x].setLabel('bottom', 'Optical Density', units='OD')
            legend = "∆Croma"

            self.my_plot[x].addLegend()

        color = QtGui.QPen(QtGui.QColor(220, 220, 220), 0, QtCore.Qt.SolidLine)
        c1 = self.my_plot[x].plot(values["curve"], pen=color, symbol='o', symbolPen=color, symbolBrush=0.5, name=legend)

        return self.my_plot[x]

    def printImage(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setAspectLocked(True)
        self.my_plot[x].setLabel('left', 'Pixels', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')

        self.getImage = pg.ImageItem()

        img = Image.open(BytesIO(values))
        self.getImage.setImage(np.rot90(img, 3))

        self.my_plot[x].addItem(self.getImage)

        return self.my_plot[x]
