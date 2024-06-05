# -*- coding: utf-8 -*-

import time

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


class spdUI(object):

    def __init__(self, valoresDE):

        self.valoresDE = valoresDE

    def setupUi(self, deltaNoise):

        self.params = ProcessSettingsClass()

        deltaNoise.setObjectName("deltaNoise")
        deltaNoise.setFixedSize(789, 491)
        deltaNoise.setWindowTitle(_translate("ImageQA", "ImageQA NOISE POWER SPECTRUM + HISTOGRAM", None))

        self.horizontalLayoutWidget = QtWidgets.QWidget(deltaNoise)
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

        self.tabWidget = QtWidgets.QTabWidget(deltaNoise)
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
            objName = "deltaNoise_" + key

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

            if key == "NPS_RGB_X" or key == "NPS_RGB_Y" :

                if len(value["curve"][0]) == 3:
                    plot = self.print_multiple_line_plot(i, value, key)
                elif len(value["curve"]) == 1:
                    plot = self.print_line_plot(i, value, key)

            elif  key == "HISTO" :

                if len(value["curve"]) == 3:
                    plot = self.print_multiple_line_plot(i, value, key)
                elif len(value["curve"]) == 1:
                    plot = self.print_line_plot(i, value, key)

            self.my_dict[l].addWidget(plot)
            # self.my_dict[bt2].clicked.connect(lambda: self.exportGraph(plot,key))

            self.my_dict[bt2].clicked.connect(lambda state, y=key, x=plot: self.export_plot(y, x))
            self.my_dict[bt1].clicked.connect(lambda state, y=value, x=key: self.export_list(y, x))
            self.my_dict[bt3].clicked.connect(lambda state, y=value, x=key: self.open_date_table(y, x))

            tabId = "tab_" + str(i)
            self.tabWidget.addTab(self.my_dict[x], tabId)
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_dict[x]), _translate(objName, nameTab, None))

            i += 1

        self.tabWidget.setCurrentIndex(0)

        self.btCerrar.clicked.connect(deltaNoise.close)

        QtCore.QMetaObject.connectSlotsByName(deltaNoise)

    def open_date_table(self, value, key):

        dialog = QtWidgets.QDialog()
        dialog.ui = TableStatsUI(value, key, None)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()

    def export_plot(self, key, plot):

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

    def export_list(self, value, key):

        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")

        fname = QtWidgets.QFileDialog.getExistingDirectory(None, 'Choose a directory for save list', path,
                                                           QtWidgets.QFileDialog.ShowDirsOnly)

        if fname != "":
            saveReportToFileClass(value, fname, key)
            self.params.save_setting('rootfolderSAVE', str(fname))

    def reduce_scale(self, values):

        total = len(values)

        if total > 16:
            i = 0
            tmpdic = values
            values = []
            for x in range(total):
                #print("contador",i)
                if i < (total/16):
                    values.append( "" )
                    #print("menor",tmpdic[x] )
                else:
                    values.append( tmpdic[x] )
                    #print("mayor", tmpdic[x])
                    i = 0

                i = i+1


        return values

    def print_multiple_line_plot(self, index, values, mode):

        #print(values)
        xdict = dict(enumerate(self.reduce_scale(values["x_axis"])))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")



        #self.my_plot[x].addLegend()

        #r = []
        #g = []
        #b = []

        if mode == "HISTO":

            self.my_plot[x].setLabel('left', 'Counts', units='')
            self.my_plot[x].setLabel('bottom', 'Bins', units='')

            r = values["curve"][0]
            g = values["curve"][1]
            b = values["curve"][2]

        elif mode == "NPS_RGB_X" or mode == "NPS_RGB_Y":

            self.my_plot[x].setLabel('left', 'Power Density', units='pixel^2')
            self.my_plot[x].setLabel('bottom', 'Cycles/pixel', units='')

            for y in values["curve"]:
                r = y[0]
                g = y[1]
                b = y[2]

        self.my_plot[x].plot(r, pen='r')
        self.my_plot[x].plot(g, pen='g')
        self.my_plot[x].plot(b, pen='b')

        return self.my_plot[x]


    def print_line_plot(self, index, values, mode):

        xdict = dict(enumerate(self.reduce_scale(values["x_axis"])))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        if mode == "HISTO":

            self.my_plot[x].setLabel('left', 'Counts', units='')
            self.my_plot[x].setLabel('bottom', 'Bins', units='')

        elif mode == "NPS_RGB_X" or mode == "NPS_RGB_Y":

            self.my_plot[x].setLabel('left', 'Power Density', units='pixel^2')
            self.my_plot[x].setLabel('bottom', 'Cycles/pixel', units='cp')

        #self.my_plot[x].addLegend()

        self.my_plot[x].plot(values["curve"][0], pen='w')

        return self.my_plot[x]
