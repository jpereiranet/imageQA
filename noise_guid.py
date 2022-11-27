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


class deltaNoiseUI(object):

    def __init__(self, valoresDE):

        self.valoresDE = valoresDE

    def setupUi(self, deltaNoise):

        self.params = ProcessSettingsClass()

        deltaNoise.setObjectName("deltaNoise")
        deltaNoise.setFixedSize(789, 491)
        deltaNoise.setWindowTitle(_translate("ImageQA", "ImageQA NOISE", None))

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

            if key == "SNR-RGB":

                # [[[[106.46639166956584, 106.99846539849773, 106.83838255928363], [108.55241303710899, 111.17530155640496, 110.83221007754842], [105.68789124821613, 107.03107130384356, 105.12326881227327], [97.02059997090801, 104.41927286879121, 99.33624605416284], [87.47592111941451, 85.97706230169257, 90.4159556414332], [70.67619673661682, 76.04977192704804, 72.06472771239795]], {'Desv Max': '3.09db', 'Desv Min': '0.22db', 'Desv Avg': '1.57db'}]]

                plot = self.print_multiple_line_plot(i, value, key)
                self.my_dict[a].setText(self.print_stats(value["stats"], key))

                # self.my_dict[a].setText( self.printStats( value[0][1], key ) )

            elif key == "SNR" or key == "C_NOISE":

                # [[[105.89903777448205, 109.31752174785206, 105.7638850825043, 99.6386900492993, 87.01634009129585, 76.26421863860946], {'Err Min': '76.26db', 'Err Average': '97.32db', 'Err Max': '109.32db', 'Err Desv': '11.86db'}]]

                plot = self.print_line_plot(i, value, key)
                self.my_dict[a].setText(self.print_stats(value["stats"], key))

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

        if fname is not "":

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

        if fname is not "":
            saveReportToFileClass(value, fname, key)
            self.params.save_setting('rootfolderSAVE', str(fname))

    def print_stats(self, stats, mode):

        o = ""
        i = 0
        #unit = stats["units"]
        for key, value in sorted(stats.items()):
            if i > 2:
                o = o + "<br>"
                i = 0
            o = o + "<strong>" + key + "</strong>: " + str(
                value[0]) + "<italic style=\"font-size:12px; color:#666\">" + value[1] + "</italic>&nbsp;&nbsp;&nbsp;&nbsp;"
            i = i + 1

        return "<p style=\"line-height:100%; font-size:16px; color:#666\">" + o + "</p>"

    def print_multiple_line_plot(self, index, values, mode):

        xdict = dict(enumerate(values["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        self.my_plot[x].setLabel('left', 'Signal To Noise Ratio', units='db')
        self.my_plot[x].setLabel('bottom', 'Aproximate Exposure Values', units='EV')

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

        self.my_plot[x].plot(r, pen='r', symbol='o', symbolPen='r', symbolBrush=0.5, name='red plot')
        self.my_plot[x].plot(g, pen='g', symbol='o', symbolPen='g', symbolBrush=0.5, name='green plot')
        self.my_plot[x].plot(b, pen='b', symbol='o', symbolPen='b', symbolBrush=0.5, name='blue plot')

        return self.my_plot[x]

    def print_line_plot(self, index, values, mode):

        xdict = dict(enumerate(values["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")

        if mode == "SNR":
            self.my_plot[x].setLabel('left', 'Signal To Noise Ratio', units='db')
            self.my_plot[x].setLabel('bottom', 'Aproximate Exposure Values', units='EV')
            label = "SNR"
        elif mode == "C_NOISE":
            self.my_plot[x].setLabel('left', 'Desv', units='σ')
            self.my_plot[x].setLabel('bottom', 'Aproximate Exposure Values', units='EV')
            label = "Desv"


        self.my_plot[x].addLegend()

        # l = pg.LegendItem((100,60), offset=(70,30))  # args are (size, offset)
        # l.setParentItem(plt.graphicsItem())   # Note we do NOT call plt.addItem in this case

        r = []

        for y in values["curve"]:
            r.append(y)

        self.my_plot[x].plot(r, pen='w', symbol='o', symbolPen='w', symbolBrush=0.5, name=label)

        return self.my_plot[x]
