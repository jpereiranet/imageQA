# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import pyqtgraph as pg
import pyqtgraph.exporters
import numpy as np
import time, sys, os
from save_report import saveReportToFileClass
import random
from plist_set import ProcessSettingsClass
from table_stats_guid import TableStatsUI
from app_paths import DefinePathsClass

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)

class multipleStatsUI(object):
    
    def __init__(self, de_values):
        #self.patchName = patchName
        #self.RGBvalues = RGBvalues
        self.de_values = de_values


            
    def setupUi(self, multipleDialog):
          
        self.params = ProcessSettingsClass()
         
        multipleDialog.setObjectName("multipleDialog")
        multipleDialog.setFixedSize(789, 491)
        multipleDialog.setWindowTitle(_translate("ImageQA", "ImageQA Batch", None))
        
        self.horizontalLayoutWidget = QtWidgets.QWidget(multipleDialog)
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
        
        
        self.tabWidget = QtWidgets.QTabWidget(multipleDialog)
        self.tabWidget.setGeometry(QtCore.QRect(10, 40, 761, 391))
        self.tabWidget.setObjectName("tabWidget")

        i = 0

        for key,value in self.de_values:
            
            self.my_dict = {}
            x = "tab_"+str(i)
            y = "horizontalLayoutWidget_"+str(i)
            z = "horizontalLayout_"+str(i)
            v = "verticalLayoutWidget_"+str(i)
            l = "verticalLayout_"+str(i)
            bt1 = "toolButton1_"+str(i)
            bt2 = "toolButton2_"+str(i)
            bt3 = "toolButton3_"+str(i)
            #g = "graphicsView_"+str(i)
            a = "label_"+str(i)
            
            nameTab = key
            objName = "multipleDialog_"+key
        
            
        
            self.my_dict[x] = QtWidgets.QWidget()
            self.my_dict[x].setObjectName("tab_2")
            self.my_dict[y] = QtWidgets.QWidget(self.my_dict[x])
            self.my_dict[y].setGeometry(QtCore.QRect(0, 300, 731, 41))
            self.my_dict[y].setObjectName("horizontalLayoutWidget_3")
            self.my_dict[z] = QtWidgets.QHBoxLayout(self.my_dict[y])
            self.my_dict[z].setObjectName("horizontalLayout_3")
            self.my_dict[a] = QtWidgets.QLabel(self.my_dict[y])
            self.my_dict[a].setObjectName("label_5")
            self.my_dict[a].setWordWrap(True)
            #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
            self.my_dict[z].addWidget(self.my_dict[a])
            self.my_dict[v] = QtWidgets.QWidget(self.my_dict[x])
            self.my_dict[v].setGeometry(QtCore.QRect(0, 0, 741, 291))
            self.my_dict[v].setObjectName("verticalLayoutWidget_2")
            self.my_dict[l] = QtWidgets.QVBoxLayout( self.my_dict[v] )

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
            
            
            if key == "SNRRGB" or key == "RGB" :
                
                plot = self.print_line_plot(i, value, key)
                #print(key)
                #print(value)
                #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
                
            if key == "SNR":
                #print(value)
                #print(key)
                #print(value)
                plot = self.print_one_line_plot(i, value, key)
                

            elif key == "DEV":
                #print(key)
                #print(value)                
                plot = self.print_simple_line_plot(i, value, key)
                #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
               
            elif key == "OECF" or key == "RED_" or key == "GREEN_" or key == "BLUE_":
                #print(key)
                #print(value)
                                
                plot = self.printOECFLineChart( i, value, key )
                #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
            
            elif key == "SENSITOMETRY":
                #print(key)
                #print(value)                
                plot = self.print_simple_line_plot(i, value, key)
                #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
                
            elif  key == "MTF":
                #print(key)
                #print(value)                
                plot = self.print_mtf_plot(i, value, key)

            elif key == "CIE76" or key == "CIE00":
                #print(key)
                #print(value)                
                plot = self.print_bars_plot(i, value)
                #self.my_dict[a].setText( self.printStats( value[0][1], key ) )
                
            self.my_dict[l].addWidget(plot)   
            
            #self.my_dict[bt2].clicked.connect(lambda: self.exportGraph(plot,key))
            
            self.my_dict[bt2].clicked.connect(lambda state, y=key, x=plot: self.export_grapth(y, x))
            self.my_dict[bt1].clicked.connect(lambda state, y=value, x=key+"_MULTI": self.export_list(y, x))
            self.my_dict[bt3].clicked.connect(lambda state, y=value, x=key+"_MULTI": self.open_data_table(y, x))

            #self.my_dict[bt1].clicked.connect(lambda: self.exportGraph(plotBars,key))
                
            tabId = "tab_"+str(i)
            self.tabWidget.addTab(self.my_dict[x], tabId)
            self.tabWidget.setTabText(self.tabWidget.indexOf(self.my_dict[x]), _translate(objName, nameTab, None))
            
            i += 1
            
        self.tabWidget.setCurrentIndex(0)

        self.btCerrar.clicked.connect(multipleDialog.close)

        QtCore.QMetaObject.connectSlotsByName(multipleDialog)

    
    def open_data_table(self, value, key):
        
        dialog = QtWidgets.QDialog()
        dialog.ui = TableStatsUI(value, key, None)
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        dialog.exec_()
    
    def export_list(self, list, key):
        
        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")
            
        fname = QtWidgets.QFileDialog.getExistingDirectory( None, 'Choose a directory for save list', path, QtWidgets.QFileDialog.ShowDirsOnly )
        
        #fname = QtGui.QFileDialog.getExistingDirectory(None,'Choose a directory for save list') 
        saveReportToFileClass(list, fname, key)
        self.params.save_setting('rootfolderSAVE', str(fname))
        
    def export_grapth(self, key, plot):
        
        path = ""
        if self.params.setting_contains("rootfolderSAVE"):
            path = self.params.setting_restore("rootfolderSAVE")
            
        fname = QtWidgets.QFileDialog.getExistingDirectory( None, 'Choose a directory for save Image', path, QtWidgets.QFileDialog.ShowDirsOnly )
        
        #fname = QtGui.QFileDialog.getExistingDirectory(None,'Choose a directory for save Image') 
        #print(fname)
        timestr = time.strftime("%Y%m%d-%H%M%S")
        exporter = pyqtgraph.exporters.ImageExporter(plot.plotItem)
        #exporter.parameters()['width'] = 800   # (note this also affects height parameter)
        exporter.params['width'] = 717
        exporter.export( fname+"/"+key+"_"+timestr+'.png')
        
        self.params.save_setting('rootfolderSAVE', str(fname))


    def print_line_plot(self, index, values, mode):
        #print(values)


        
        im = []
        j = 1
        for img in values:
            im.append( str(j)+"-"+img[0][0:3])
            j = j +1
        
        xdict = dict(enumerate( im ))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        
        self.my_plot = {}
        x = "graphicsView_"+str(index)
        
        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")
        if mode == "RGB":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setYRange(0, 255)
        elif mode == "RGBSNR":
            self.my_plot[x].setLabel('left', 'Signal To Noise Ratio', units='db')
        elif mode == "SENSITOMETRY":
            self.my_plot[x].setLabel('left', 'Lightness', units='L*')
            
        self.my_plot[x].setLabel('bottom', 'Images', units='')
        
        self.my_plot[x].addLegend()

  
        Wr = []
        Wg = []
        Wb = []
        
        Gr = []
        Gg = []
        Gb = []
        
        Br = []
        Bg = []
        Bb = []
        
        i = 0
        for value in values:
       
            Wr.append(value[1][0][0])
            Wg.append(value[1][0][1])
            Wb.append(value[1][0][2])
            
            Gr.append(value[1][1][0])
            Gg.append(value[1][1][1])
            Gb.append(value[1][1][2])

            Br.append(value[1][2][0])
            Bg.append(value[1][2][1])
            Bb.append(value[1][2][2])
            
        
        self.my_plot[x].plot(Wr, pen='r', symbol='o', symbolPen='r', symbolBrush=0.5, name='White red ')
        self.my_plot[x].plot(Wg, pen='g', symbol='o', symbolPen='g', symbolBrush=0.5, name='White green ')
        self.my_plot[x].plot(Wb, pen='b', symbol='o', symbolPen='b', symbolBrush=0.5, name='White blue ') 
        
        self.my_plot[x].plot(Gr, pen='r', symbol='s', symbolPen='r', symbolBrush=0.5, name='Grey red ')
        self.my_plot[x].plot(Gg, pen='g', symbol='s', symbolPen='g', symbolBrush=0.5, name='Grey green ')
        self.my_plot[x].plot(Gb, pen='b', symbol='s', symbolPen='b', symbolBrush=0.5, name='Grey blue ')
        
        self.my_plot[x].plot(Br, pen='r', symbol='t', symbolPen='r', symbolBrush=0.5, name='Black red ')
        self.my_plot[x].plot(Bg, pen='g', symbol='t', symbolPen='g', symbolBrush=0.5, name='Black green ')
        self.my_plot[x].plot(Bb, pen='b', symbol='t', symbolPen='b', symbolBrush=0.5, name='Black blue ')  
        
        return self.my_plot[x]
    
    def print_one_line_plot(self, index, values, mode):

        #print(values)
        xdict = dict(enumerate(values[0]["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        
        self.my_plot = {}
        x = "graphicsView_"+str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")
        
        if mode == "SNR":
            self.my_plot[x].setLabel('left', 'SNR', units='db')

        self.my_plot[x].setLabel('bottom', 'Aproximate Exposure Values', units='EV')
        
        self.my_plot[x].addLegend()
    
        n = len(values)
        range = int(255 / n)

        for value in values:

            Rr = random.randrange(100, 255, 10)
            Gr = random.randrange(100, 255, 10)
            Br = random.randrange(100, 255, 10)

            color = QtGui.QPen(QtGui.QColor(Rr, Gr, Br), 0, QtCore.Qt.SolidLine)

            self.my_plot[x].plot(value["curve"], pen=color, name="ISO"+str(value['ISO'])+" ("+value['File']+")")
            range = range+range

        
        return self.my_plot[x]    
    
    
    def print_mtf_plot(self, index, values, mode):

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].setObjectName("plot")

        newxdic = {0: 0.0, 1: "", 2: "", 3: "", 4: "", 5: "", 6: "", 7: "", 8: "", 9: "", 10: "", 11: "",
                   12: "",13: 0.1, 14: "", 15: "", 16: "", 17: "", 18: "", 19: "", 20: "", 21: "", 22: "", 23: "",
                   24: "", 25: 0.2, 26: "", 27: "", 28: "", 29: "", 30: "", 31: "", 32: "", 33: "", 34: "", 35: "",
                   36: "", 37: "", 38: 0.3, 39: "", 40: "", 41: "", 42: "", 43: "", 44: "", 45: "", 46: "", 47: "", 48: "", 49: "", 50: "",
                   51: 0.4, 52: "", 53: "", 54: "", 55: "", 56: "", 57: "", 58: "", 59: "", 60: "", 61: "", 62: "",
                   63: 0.5, 64: "", 65: "", 66: "", 67: "", 68: "", 69: "", 70: "", 71: "", 72: "", 73: "", 74: "", 75: "",
                   76: 0.6, 77: "", 78: "", 79: "", 80: "", 81: "", 82: "", 83: "", 84: "", 85: "", 86: "", 87: "", 88: "",
                   89: 0.7, 90: "", 91: "", 92: "", 93: "", 94: "", 95: "", 96: "", 97: "", 98: "", 99: "", 100: "",
                   101: 0.8, 102: "", 103: "", 104: "", 105: "", 106: "", 107: "", 108: "", 109: "", 110: "", 111: "", 112: "", 113: "",
                   114: 0.9, 115: "", 116: "", 117: "", 118: "", 119: "", 120: "", 121: "", 12: "", 123: "", 124: "", 125: "", 126: 0.9}
        
        stringaxis = self.my_plot[x].getAxis('bottom')
        #newxdic = {0: 0.0,   63: 0.5 ,126: 1}
        stringaxis.setTicks([newxdic.items()])

        self.my_plot[x].setLabel('left', 'Modulation factor', units='')
        self.my_plot[x].setLabel('bottom', 'Cycles/Pixel', units='')
        
        self.my_plot[x].addLegend()

        o = []
        i = []

        for value in values:
        
            Rr = random.randrange(100, 255, 10)
            Gr = random.randrange(100, 255, 10)
            Br = random.randrange(100, 255, 10)
            
            smoot = np.ndarray.tolist(value["mtf_final"])
            #print(value[1][1])
            color = QtGui.QPen(QtGui.QColor(Rr, Gr, Br), 0, QtCore.Qt.SolidLine)

            self.my_plot[x].plot(smoot, pen=color, name=value["filename"])


        return self.my_plot[x]
    
    
    def printOECFLineChart(self,index, values, mode):
            
        xdict = dict(enumerate(values[0]["x_axis"]))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])

        self.my_plot = {}
        x = "graphicsView_" + str(index)

        self.my_plot[x] = pg.PlotWidget(name=mode)
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        self.my_plot[x].setObjectName("plot")
        #self.my_plot = {}
        #x = "graphicsView_"+str(index)
        
        #self.my_plot[x] = pg.PlotWidget(name='Plot1')
        #self.my_plot[x].setMenuEnabled(False)
        #self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        
        
        #self.my_plot[x].setObjectName("plot")
            
        if  mode == "OECF":
            self.my_plot[x].setLabel('left', 'Count Values', units='CV')
            self.my_plot[x].setLabel('bottom', 'Optical Density', units='OD')
        
            
        #self.my_plot[x].setLabel('bottom', 'Patch', units='')
        
        self.my_plot[x].addLegend()

        n = len(values)
        range = int(255 / n)

        for value in values:
            #print(value)
            z = []
            ref = []
            for v in value["curve"]:
                #print(v)
                z.append(float(v[0])) #carga curva imagen
                ref.append(float(v[1])) #carga cuvar referencia
                
            Rr = random.randrange(100, 255, 10)
            Gr = random.randrange(100, 255, 10)
            Br = random.randrange(100, 255, 10)

            color = QtGui.QPen(QtGui.QColor(Rr, Gr, Br), 0, QtCore.Qt.SolidLine)

            self.my_plot[x].plot(z, pen=color,symbol='o', symbolPen=color, symbolBrush=pg.mkBrush([Rr, Gr, Br, 191]), name=value["File"])
            range = range+range

        color = QtGui.QPen(QtGui.QColor(255, 0, 0), 0, QtCore.Qt.SolidLine )
        self.my_plot[x].plot(ref, pen=color, symbol='s', symbolPen=color, symbolBrush=0.5, name="Reference")
        
        return self.my_plot[x]
    
    def print_simple_line_plot(self, index, values, mode):
        
        #print(values)
        
        im = []
        shutter = []
        aperture = []
        
        j = 1
        for img in values:
            
            if type(img[0]) == tuple:
                shutter.append( img[0][0])
                aperture.append( img[0][1])
            else:
                im.append( str(j)+"-"+img[0][0:3])
            
            j = j +1
        
        
        if mode == "SENSITOMETRY":
            #comprueba si usar el array con apertura o velocidad por repetición de los valores, si no se repiten es la otra escala

            repeatShutter = len(set(shutter)) <= 1
            repeatAperture = len(set(aperture)) <= 1
            if repeatShutter:
                im = aperture
            elif repeatAperture:
                im = shutter
                  
        
        xdict = dict(enumerate( im ))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        
        self.my_plot = {}
        x = "graphicsView_"+str(index)
        
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        
        
        self.my_plot[x].setObjectName("plot")

        if mode == "DEV":
            self.my_plot[x].setLabel('left', '∆ EV', units='')
            self.my_plot[x].setLabel('bottom', 'Image', units='')
            
        elif  mode == "OECF":
            self.my_plot[x].setLabel('left', '∆ CV', units='')
            self.my_plot[x].setLabel('bottom', 'Image', units='')
            
        elif  mode == "SENSITOMETRY":
            self.my_plot[x].setLabel('left', 'Lightness', units='L*') 
            self.my_plot[x].setLabel('bottom', 'exposure', units='')
            
        #self.my_plot[x].setLabel('bottom', 'Image', units='')
        
        self.my_plot[x].addLegend()

        Wv = []
        Gv = []
        Bv = []
        
        i = 0
        for value in values: 
             
            Wv.append(value[1][0])
            Gv.append(value[1][1])
            Bv.append(value[1][2])

        colorA = QtGui.QPen(QtGui.QColor(250, 250, 250), 0, QtCore.Qt.SolidLine)
        colorB = QtGui.QPen(QtGui.QColor(200, 200, 200), 0, QtCore.Qt.SolidLine)
        colorC = QtGui.QPen(QtGui.QColor(100, 100, 100), 0, QtCore.Qt.SolidLine)

        self.my_plot[x].plot(Wv, pen=colorA, symbol='o', symbolPen=colorA, symbolBrush=0.5, name='White')
        self.my_plot[x].plot(Gv, pen=colorB, symbol='s', symbolPen=colorB, symbolBrush=0.5, name='Grey')
        self.my_plot[x].plot(Bv, pen=colorC, symbol='t', symbolPen=colorC, symbolBrush=0.5, name='Black')
     
        
        return self.my_plot[x]
    
    def print_bars_plot(self, index, values):
        
        #x = ['A01', 'A02', 'A03', 'A04', 'A05', 'A06', 'B01', 'B02', 'B03', 'B04', 'B05', 'B06', 'C01', 'C02', 'C03', 'C04', 'C05', 'C06', 'D01', 'D02', 'D03', 'D04', 'D05', 'D06']
        #RGB = [[120.0, 84.0, 70.0], [200.0, 147.0, 131.0], [90.0, 123.0, 157.0], [94.0, 109.0, 66.0], [131.0, 130.0, 176.0], [93.0, 191.0, 173.0], [226.0, 125.0, 46.0], [70.0, 92.0, 174.0], [202.0, 82.0, 96.0], [95.0, 59.0, 105.0], [162.0, 191.0, 64.0], [233.0, 162.0, 38.0], [41.0, 66.0, 153.0], [70.0, 153.0, 74.0], [181.0, 56.0, 59.0], [243.0, 203.0, 16.0], [196.0, 87.0, 152.0], [0.0, 137.0, 169.0], [249.0, 249.0, 245.0], [204.0, 205.0, 204.0], [163.0, 165.0, 164.0], [122.0, 122.0, 122.0], [83.0, 86.0, 86.0], [49.0, 49.0, 50.0]]
        #valores = [4.087079540389303+index, 26.350893085388346, 31.326033832741064, 26.147504712580115, 32.069746409192426, 47.54279596821581, 27.349475394841647, 34.74605147078201, 20.93713967367054, 26.899617884278662, 43.55986723896667, 36.542839523283085, 36.33991338030653, 39.676784282403666, 16.435616745850744, 45.00340648534447, 28.763248121974915, 40.854622104322004, 46.7631167919002, 39.212963503781346, 30.799714084152203, 19.787182039097967, 17.541255936049154, 21.467976117460505]
        
        #print(values)
        #print(index)
        
        im = []
        j = 1
        for img in values:
            im.append( str(j)+"-"+img[0][0:3])
            j = j +1
        
        xdict = dict(enumerate( im ))
        stringaxis = pg.AxisItem(orientation='bottom')
        stringaxis.setTicks([xdict.items()])
        
        self.my_plot = {}
        x = "graphicsView_"+str(index)
        
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setMenuEnabled(False)
        self.my_plot[x].getAxis('bottom').setTicks([xdict.items()])
        
        self.my_plot[x].setObjectName("plot")
        self.my_plot[x].setLabel('left', 'Delta-e', units='∆e')
        self.my_plot[x].setLabel('bottom', 'Images', units='')
        
        i = 0
        for value in values:
            color = self.rgb_levels(value[1])
            bg = pg.BarGraphItem(x= np.arange( 1 )+i , height= value[1] , width=1, brush= pg.QtGui.QColor(color[0],color[1],color[2]))
            self.my_plot[x].addItem( bg   )
            i += 1            
        
        return self.my_plot[x]
    
    
    
    def rgb_levels(self, de):
        
        if de < 2:
            r = 0
            g = 116
            b = 0
        if de > 2 and de < 4:
            r = 255
            g = 170
            b = 0   
        if de > 4:
            r = 250
            g = 0
            b = 0   
        
        return r,g,b                             

        
    def print_image(self, index, values, mode):
                
        self.my_plot = {}
        x = "graphicsView_"+str(index)
        self.my_plot[x] = pg.PlotWidget(name='Plot1')
        self.my_plot[x].setAspectLocked(True)
        self.my_plot[x].setLabel('left', 'Pixels', units='')
        self.my_plot[x].setLabel('bottom', 'Pixels', units='')
        
        self.getImage = pg.ImageItem()
        self.getImage.setImage(np.rot90(values,3) )
        
        self.my_plot[x].addItem(self.getImage)
        
        return self.my_plot[x]


