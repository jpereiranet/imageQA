# -*- coding: utf-8 -*-

import time, math

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
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


class MtfUI(object):

    def __init__(self, valoresMTF):

        self.valoresMTF = valoresMTF

    def setupUi(self, MTFDialog):

        self.params = ProcessSettingsClass()

        MTFDialog.setObjectName("MTFDialog")
        MTFDialog.setFixedSize(789, 541)
        MTFDialog.setWindowTitle(_translate("ImageQA", "ImageQA MTF LSF ESF", None))

        self.horizontalLayoutWidget = QtWidgets.QWidget(MTFDialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 485, 291, 32))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")

        self.btCerrar = QtWidgets.QToolButton(self.horizontalLayoutWidget)
        self.btCerrar.setGeometry(QtCore.QRect(0, 0, 30, 30))
        self.btCerrar.setObjectName("btCerrar")
        self.btCerrar.setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('close_64px.png')))
        self.btCerrar.setIconSize(QtCore.QSize(30, 30))
        self.btCerrar.setToolTip("Close")

        self.tabWidget = QtWidgets.QTabWidget(MTFDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 761, 430))
        self.tabWidget.setObjectName("tabWidget")

        i = 0

        for key, value in self.valoresMTF:

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
            objName = "MTFDialog_" + key

            self.my_dict[x] = QtWidgets.QWidget()
            self.my_dict[x].setObjectName("tab_2")
            self.my_dict[y] = QtWidgets.QWidget(self.my_dict[x])
            self.my_dict[y].setGeometry(QtCore.QRect(0, 275, 731, 141))
            self.my_dict[y].setObjectName("horizontalLayoutWidget_3")
            self.my_dict[z] = QtWidgets.QHBoxLayout(self.my_dict[y])

            self.my_dict[z].setObjectName("horizontalLayout_3")
            self.my_dict[a] = QtWidgets.QLabel(self.my_dict[y])
            self.my_dict[a].setObjectName("label_5")
            self.my_dict[a].setWordWrap(True)

            if key == "MTF":
                self.my_dict[a].setText(self.printStats(value))
                self.my_dict[a].setStyleSheet("padding:0")
            if key == "ESF":
                self.my_dict[a].setText(self.printStatsESF(value))

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
            self.my_dict[bt1].setIconSize(QtCore.QSize(30, 30))

            self.my_dict[bt2] = QtWidgets.QToolButton(self.my_dict[x])
            self.my_dict[bt2].setGeometry(QtCore.QRect(660, 310, 41, 41))
            self.my_dict[bt2].setObjectName("toolButton_2")
            self.my_dict[bt2].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('pictures_64px.png')))
            self.my_dict[bt2].setIconSize(QtCore.QSize(30, 30))

            self.my_dict[bt3] = QtWidgets.QToolButton(self.my_dict[x])
            self.my_dict[bt3].setGeometry(QtCore.QRect(610, 310, 41, 41))
            self.my_dict[bt3].setObjectName("toolButton_3")
            self.my_dict[bt3].setIcon(QtGui.QIcon(DefinePathsClass.create_resource_path('table_64px.png')))
            self.my_dict[bt3].setIconSize(QtCore.QSize(30, 30))

            if key == "BORDER" or key == "ROI":
                plot = self.printImage(i, value, key)
                self.my_dict[bt1].setEnabled(False)
                self.my_dict[bt3].setEnabled(False)

            if key == "MTF":
                plot = self.printLineMTF(i, value, key)
            if key == "LSF":
                plot = self.printLineLSF(i, value, key)
            if key == "ESF":

                plot = self.printLineESF(i, value, key)

            self.my_dict[l].addWidget(plot)

            self.my_dict[bt2].clicked.connect(lambda state, y=key, x=plot: self.exportGraph(y, x))
            self.my_dict[bt1].clicked.connect(lambda state, y=value, x=key: self.exportList(y, x))
            self.my_dict[bt3].clicked.connect(lambda state, y=value, x=key: self.openTableData(y, x))

            tabId = "tab_" + str(i)
            self.tabWidget.addTab(self.my_dict[x], tabId)
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_dict[x]), _translate(objName, nameTab, None))

            i += 1

        self.tabWidget.setCurrentIndex(0)

        self.btCerrar.clicked.connect(MTFDialog.close)
        QtCore.QMetaObject.connectSlotsByName(MTFDialog)

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
            #print(path)

        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save list', path,
                                                       QtWidgets.QFileDialog.ShowDirsOnly)

        if fname != "":
            saveReportToFileClass(value, fname, key)
            self.params.save_setting('rootfolderSAVE', str(fname))

    '''
    def closeEvent(self):
        self.close()      
    '''

    def createCenteScale(self,values):

        total = len(values)
        centro = (int(total / 2))-1

        valormaximo = max(values)
        #print("vmax",valormaximo)
        mitadvalormaximo = round((valormaximo / 2), 2)

        pasos = mitadvalormaximo / centro

        #print("total "+str(total))
        #print("pasos "+str(pasos))
        #print("centro "+str(centro))

        newxdic = {}
        i = float(mitadvalormaximo)
        t = 0
        v = ""
        for x in range(0, centro):
            #print(x)
            if t > 10:
                v = math.ceil(i)
                t = 0
            #else:
            #    v = None

                newxdic[x] = str(v)
            i = i - pasos
            t = t + 1

        #print("left "+str(x))
        #print("centro " + str(centro))
        newxdic[centro] = "0"

        j = pasos
        t = 0
        v = ""
        for y in range(centro+1, total):
            #print(y)
            if t > 10:
                v = math.floor(j)
                t = 0
            #else:
            #    v = ""

                newxdic[y] = str(v)
            j = j + pasos
            t = t + 1

        #print("right " + str(y))

        #print(newxdic)

        return (newxdic, centro)
    '''
    def normaliceDimensions(self,ch_gray, ch_red,ch_green,ch_blue):

        numpies = [ch_gray, ch_red,ch_green,ch_blue]
        dimensions = [np.prod(ch_gray.shape), np.prod(ch_red.shape), np.prod(ch_green.shape), np.prod(ch_blue.shape) ]

        maxdimension = max(dimensions)
        mindimension = min(dimensions)
        maxdIndex = dimensions.index(max(dimensions))
        minvalue = min(numpies[maxdIndex])
        maxvalue = max(numpies[maxdIndex])
        #print("max dim",maxdimension)
        #print("min dim", mindimension)

        if maxdimension is not mindimension:
            rd = np.prod(ch_gray.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(maxvalue)
                ch_gray = np.append( ch_gray,npvalues )

            rd = np.prod(ch_red.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(minvalue)

                ch_red = np.append(npvalues, ch_red)

            rd = np.prod(ch_green.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(minvalue)
                ch_green = np.append(npvalues,ch_green )

            rd = np.prod(ch_blue.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(minvalue)
                ch_blue = np.append(npvalues,ch_blue  )

        return [ch_gray, ch_red, ch_green, ch_blue,maxdIndex ]
    '''

    #MTF
    def printLineMTF(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)

        newxdic = {0: "0.0", 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "",
                   12: "",13: "0.1", 14: "", 15: "", 16: "", 17: "", 18: "", 19: "", 20: "", 21: "", 22: "", 23: "",
                   24: "", 25: "0.2", 26: "", 27: "", 28: "", 29: "", 30: "", 31: "", 32: "", 33: "", 34: "", 35: "",
                   36: "", 37: "", 38: "0.3", 39: "", 40: "", 41: "", 42: "", 43: "", 44: "", 45: "", 46: "", 47: "", 48: "", 49: "", 50: "",
                   51: "0.4", 52: "", 53: "", 54: "", 55: "", 56: "", 57: "", 58: "", 59: "", 60: "", 61: "", 62: "",
                   63: "0.5", 64: "", 65: "", 66: "", 67: "", 68: "", 69: "", 70: "", 71: "", 72: "", 73: "", 74: "", 75: "",
                   76: "0.6", 77: "", 78: "", 79: "", 80: "", 81: "", 82: "", 83: "", 84: "", 85: "", 86: "", 87: "", 88: "",
                   89: "0.7", 90: "", 91: "", 92: "", 93: "", 94: "", 95: "", 96: "", 97: "", 98: "", 99: "", 100: "",
                   101: "0.8", 102: "", 103: "", 104: "", 105: "", 106: "", 107: "", 108: "", 109: "", 110: "", 111: "", 112: "", 113: "",
                   114: "0.9", 115: "", 116: "", 117: "", 118: "", 119: "", 120: "", 121: "", 122: "", 123: "", 124: "", 125: "", 126: "1"}
        stringaxis = self.my_plot[x].getAxis('bottom')
        #newxdic = {0: "0.0",   63: "0.5" ,126: "1"}
        stringaxis.setTicks([newxdic.items()])
        #stringaxis.setTickSpacing(5, 1)

        self.my_plot[x].setObjectName("plot")

        self.my_plot[x].setLabel('left', 'Modulation factor', units='')
        self.my_plot[x].setLabel('bottom', 'Cycles/Pixel', units='')

        label_opts = {'position': 0.9, 'color': (200, 200, 100),
                      'fill': (200, 200, 200, 50), 'movable': True}
        t_line = pg.InfiniteLine(pos=63, movable=False, angle=90, label='Nyquist', labelOpts=label_opts)
        self.my_plot[x].addItem(t_line)

        self.my_plot[x].addLegend()

        if len(values) == 1:
            self.my_plot[x].plot(values["GRAY"]["mtf_final"], pen='w', name='Grey')
        else:
            self.my_plot[x].plot(values["RED"]["mtf_final"], pen='r', name='Red')
            self.my_plot[x].plot(values["GREEN"]["mtf_final"], pen='g', name='Green')
            self.my_plot[x].plot(values["BLUE"]["mtf_final"], pen='b', name='Blue')
            self.my_plot[x].plot(values["GRAY"]["mtf_final"], pen='w', name='Grey')

        return self.my_plot[x]

    #ESF
    def printLineESF(self, index, values, mode):

        #xindexes = [ values["GRAY"]["xesf"], values["RED"]["xesf"], values["GREEN"]["xesf"], values["BLUE"]["xesf"] ]

        newxdic, centro = self.createCenteScale( values["GRAY"]["xesf"] )

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')

        self.my_plot[x].setMenuEnabled(False)
        #newxdic = {0: 8, 11: 7, 22: 6, 33: 5, 44: 4, 56: 3, 67: 2, 78: 1, 89: 0,
        #           100: 1, 111: 2, 122: 3, 133: 4, 144: 5, 156: 6, 167: 7, 177: 8}
        stringaxis = self.my_plot[x].getAxis('bottom')
        stringaxis.setTicks([newxdic.items()])

        self.my_plot[x].setObjectName("plot")

        self.my_plot[x].setLabel('left', 'Grey Value', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')
        # point = QtCore.QPointF(65, 0)
        label_opts = {'position': 0.1, 'color': (200, 200, 100),
                      'fill': (200, 200, 200, 50), 'movable': True}
        t_line = pg.InfiniteLine(pos=centro, movable=False, angle=90, label='edge', labelOpts=label_opts)
        self.my_plot[x].addItem(t_line)

        self.my_plot[x].addLegend()

        #raw = np.ndarray.tolist(values["esf"])
        #c1 = self.my_plot[x].plot(raw, pen='r', name='raw')

        #smoot = np.ndarray.tolist(values["esf_smooth"])
        #c2 = self.my_plot[x].plot(smoot, pen='g', name='smoot')


        if len(values) == 2:
            self.my_plot[x].plot(values["GRAY"]["esf"], pen='w', name='Grey')
        else:
            self.my_plot[x].plot(values["RED"]["esf"], pen='r', name='Red')
            self.my_plot[x].plot(values["GREEN"]["esf"], pen='g', name='Green')
            self.my_plot[x].plot(values["BLUE"]["esf"], pen='b', name='Blue')
            self.my_plot[x].plot(values["GRAY"]["esf"], pen='w', name='Grey')

        return self.my_plot[x]

        # LSF

    def printLineLSF(self, index, values, mode):

        GRAY_CH = values["GRAY"]["lsf_smooth"]

        #redondear = lambda x: round(x, 1)
        #x_axis = list(map(redondear, np.ndarray.tolist(values["xesf"])))
        #xdict = dict(enumerate(x_axis))
        #print(xdict)

        newxdic, centro = self.createCenteScale( values["GRAY"]["xesf"] )

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')

        self.my_plot[x].setMenuEnabled(False)

        #newxdic = {0:8, 11: 7, 22:6, 33:5, 44:4, 56:3, 67: 2, 78: 1, 89: 0,
        #            100: 1, 111: 2, 122: 3, 133: 4, 144: 5, 156: 6, 167:7, 177: 8}
        stringaxis = self.my_plot[x].getAxis('bottom')
        stringaxis.setTicks([newxdic.items()])

        self.my_plot[x].setObjectName("plot")

        self.my_plot[x].setLabel('left', 'Grey Value', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')
        # point = QtCore.QPointF(65, 0)
        label_opts = {'position': 0.1, 'color': (200, 200, 100),
                      'fill': (200, 200, 200, 50), 'movable': True}
        t_line = pg.InfiniteLine(pos=centro, movable=False, angle=90, label='edge', labelOpts=label_opts)
        self.my_plot[x].addItem(t_line)

        self.my_plot[x].addLegend()


        self.my_plot[x].plot(GRAY_CH, pen='w', name='Grey')


        return self.my_plot[x]

    def printImage(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setAspectLocked(lock=True, ratio=1)
        self.my_plot[x].setLabel('left', 'Pixels', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')

        self.getImage = pg.ImageItem()
        self.getImage.setImage(np.rot90(values, 3))

        self.my_plot[x].addItem(self.getImage)

        return self.my_plot[x]

    def printStats(self, stats):
        metrics = ["MTF50", "MTF30", "MTF10"]
        o = ""
        for metric in metrics:

            if stats["GRAY"][metric]["MTF"]:
                o += "<p style=\"line-height:90%; font-size:16px; color:#666\">"
                o += "<strong>"+metric+":</strong> <span style=\"font-size:13px; color:#666\">(" + str(int(stats["GRAY"][metric]["MTFpercent"]))+"%)</span>&nbsp;"+ str(
                    stats["GRAY"][metric]["MTF"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">Cycles/pixel</italic>&nbsp;&nbsp;"

                if stats["GRAY"][metric]["imgLPmm"] and stats["GRAY"][metric]["lpNyquist"]:
                    o +=  str(stats["GRAY"][metric]["imgLPmm"])+"/"+str(stats["GRAY"][metric]["lpNyquist"])+"<span style=\"font-size:13px; color:#666\">("+str(int(stats["GRAY"][metric]["lpPercent"]))+"%)</span>&nbsp;<italic style=\"font-size:12px; color:#666\">Lp/mm</italic>&nbsp;&nbsp;"
                    o += "" + str(stats["GRAY"][metric]["LW_PH"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">LW/PH</italic>&nbsp;&nbsp;"
                    o += "" + str(stats["GRAY"][metric]["LPH"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">LP/PH</italic>"
                o += "</p>"
            else:
                o += "<p style=\"line-height:90%; font-size:12px; color:#666\">"
                o += "<span>"+metric+" Not available due aliasing</span>"
                o += "</p>"


        return o

    def printStatsESF(self, stats):

        o = ""
        if "INFO" in stats and stats["INFO"]["CA"] != None:
            o = "<p style=\"line-height:100%; font-size:16px; color:#666\">"
            o += "<strong>Misregistration (CA):</strong> " + str(
                stats["INFO"]["CA"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">pixels</italic>&nbsp;&nbsp;"
            o += "</p>"

            o += "<p style=\"line-height:100%; font-size:16px; color:#666\">"
            o += "<strong>10-90% Rise (RGB):</strong> " + str(
                stats["INFO"]["RAISE_RED"])+"/"+ str(
                stats["INFO"]["RAISE_GREEN"])+"/"+ str(
                stats["INFO"]["RAISE_BLUE"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">pixels</italic>&nbsp;&nbsp;"
            o += "</p>"

        if "INFO" in stats and stats["INFO"]["RAISE_GRAY"] != None:
            o = "<p style=\"line-height:100%; font-size:16px; color:#666\">"
            o += "<strong>10-90% Rise (RGB):</strong> " + str(
                stats["INFO"]["RAISE_GRAY"]) + "&nbsp;<italic style=\"font-size:12px; color:#666\">pixels</italic>&nbsp;&nbsp;"
            o += "</p>"

        return o