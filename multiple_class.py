# -*- coding: utf-8 -*-

import os

from PyQt5 import QtCore, QtGui, QtWidgets

from charts import ChartPatternsClass
from deltas_class import GetDeltasClass
from getImageColors import getImageColors
from metadata_class import GetMetadataClass
#from mtf_class import GetMTFClass
from mtf_rgb import GetMTFClassRGB
from multiple_stats_guid import multipleStatsUI
from noise_class import GetNoiseClass
from oecf_class import GetOECFClass
from readCGATS import GetCGATSClass

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class MultipleTestClass(object):

    def __init__(self, coordenadasReales, multipleFiles, CEGATSpath, perfil_nuevo, chartIndex):

        # super(UI_Multiple, self).__init__(multipleFiles, coordenadasReales, CEGATSpath, perfil_nuevo, chartIndex)
        # self.a = QtGui.QApplication(sys.argv)
        self.multipleFiles = multipleFiles
        self.coords = coordenadasReales
        self.cgats = CEGATSpath
        self.icc = perfil_nuevo
        self.chartIndex = chartIndex
        self.charts = ChartPatternsClass()

    def setupUi(self, MultipleDialog):

        MultipleDialog.setObjectName("MultipleDialog")
        MultipleDialog.setFixedSize(299, 239)
        MultipleDialog.setWindowTitle(_translate("MultipleDialog", "ImageQA Batch Analysis", None))

        self.listView = QtGui.QListView(MultipleDialog)
        self.listView.setGeometry(QtCore.QRect(20, 20, 261, 141))
        self.listView.setObjectName("listView")

        model = QtGui.QStandardItemModel()
        self.listView.setModel(model)

        arr = []
        for i in self.multipleFiles:
            # print( os.path.basename( str(i) ) )
            item = QtGui.QStandardItem(os.path.basename(str(i)))
            model.appendRow(item)
            arr.append(str(i))

        self.comboBox = QtGui.QComboBox(MultipleDialog)
        self.comboBox.setGeometry(QtCore.QRect(20, 180, 191, 26))
        self.comboBox.setObjectName("comboBox")
        items = ["--- Select----", "Delta-e", "OECF", "MTF", "NOISE", "Sensitometry"]
        self.comboBox.addItems(items)

        switch = self.charts.get_switch(self.chartIndex)

        self.comboBox.model().item(1).setEnabled(switch[0])
        self.comboBox.model().item(2).setEnabled(switch[5])
        self.comboBox.model().item(3).setEnabled(switch[3])
        self.comboBox.model().item(4).setEnabled(switch[4])
        self.comboBox.model().item(5).setEnabled(switch[4])

        self.comboBox.currentIndexChanged.connect(self.enable_go_button)

        self.goButton = QtGui.QToolButton(MultipleDialog)
        self.goButton.setGeometry(QtCore.QRect(230, 170, 51, 41))
        self.goButton.setObjectName("toolButton")
        self.goButton.setText(_translate("MultipleDialog", "GO", None))
        self.goButton.setEnabled(False)
        self.goButton.clicked.connect(self.open_stats)

        QtCore.QMetaObject.connectSlotsByName(MultipleDialog)

    def check_item(self, itemName):

        items_list = self.listView.model().findItems(itemName, QtCore.Qt.MatchExactly)
        item = items_list[0].row()
        self.listView.model().item(item).setBackground(QtGui.QColor("#7fc97f"))
        QtGui.QApplication.processEvents()

    def reset_check_item(self):

        for item in range(self.listView.model().rowCount()):
            self.listView.model().item(item).setBackground(QtGui.QColor("#ffffff"))

    def enable_go_button(self):

        self.reset_check_item()

        if self.comboBox.currentIndex() > 0:
            self.goButton.setEnabled(True)
        else:
            self.goButton.setEnabled(False)

    def open_stats(self):

        index = self.comboBox.currentIndex()

        if index == 1:

            stats = [("CIE76", self.get_means_color("CIE76")),
                     ("CIE00", self.get_means_color("CIE00"))
                     ]

        elif index == 2:

            stats = [
                ("OECF", self.get_m_oecf())
            ]

        elif index == 3:

            stats = [
                ("MTF", self.get_m_mtf())
            ]

        elif index == 4:

            stats = [
                ("SNR", self.get_m_noise())
            ]

        elif index == 5:

            stats = [
                ("SENSITOMETRY", self.get_m_sentitometry())
            ]

        if stats[0][1] is not None:
            dialog = QtGui.QDialog()
            dialog.ui = multipleStatsUI(stats)
            dialog.ui.setupUi(dialog)
            dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            dialog.exec_()

    # empiezan las funcioens de analisis

    def get_m_mtf(self):

        o = {}
        i = 0
        for filename in self.multipleFiles:
            #get_mtf = GetMTFClass(str(filename), self.coords)
            #esf = get_mtf.compute_esf()
            #lsf = get_mtf.compute_lsf(esf["xesf"], esf["esf"], esf["esf_smooth"])
            #mtf = get_mtf.compute_mtf(lsf["lsf"], lsf["lsf_smooth"])

            get_mtf_rgb = GetMTFClassRGB(str(filename), self.coords)
            values = get_mtf_rgb.get_mtf_multiple()

            #channel_mtf = values["channel_mtf"]
            #channel_lsf = values["channel_lsf"]
            #channel_esf = values["channel_esf"]

            self.check_item(os.path.basename(str(filename)))

            meta = GetMetadataClass(str(filename))
            exposure = meta.get_exposure()

            o[i] = {}
            o[i]["FILENAME"] = os.path.basename(str(filename))
            o[i]["SHUTTER"] = exposure[0]
            o[i]["APERTURE"] = exposure[1]
            o[i]["ISO"] = exposure[2]
            o[i]["MTF"] = values["channel_mtf"]

            i = i + 1

        r = None
        metrics = ["MTF50", "MTF30", "MTF10"]
        if o[0]["MTF"] is not None:
            r = []

            for x in o:
                rep = {
                 "filename": o[x]["FILENAME"],
                 "shutter": o[x]["SHUTTER"],
                 "aperture": o[x]["APERTURE"],
                 "iso": o[x]["ISO"],
                 "x_mtf_final": o[x]["MTF"]["GRAY"]["x_mtf_final"],
                 "mtf_final": o[x]["MTF"]["GRAY"]["mtf_final"],

                 }
                for metric in metrics:
                    rep[metric] =  o[x]["MTF"]["GRAY"][metric]["MTF"]
                    rep[metric + "MTFpercent"] = o[x]["MTF"]["GRAY"][metric]["MTFpercent"]
                    rep[metric+"LPmm"] =  o[x]["MTF"]["GRAY"][metric]["LPmm"]
                    rep[metric+"LW_PH"] =  o[x]["MTF"]["GRAY"][metric]["LW_PH"]
                    rep[metric+"LPH"] =  o[x]["MTF"]["GRAY"][metric]["LPH"]

                    rep[metric + "lpNyquist"] = o[x]["MTF"]["GRAY"][metric]["lpNyquist"]
                    rep[metric + "imgLPmm"] = o[x]["MTF"]["GRAY"][metric]["imgLPmm"]
                    rep[metric + "lpPercent"] = o[x]["MTF"]["GRAY"][metric]["lpPercent"]



                r.append(rep)

        return r

    def get_m_noise(self):


        o = {}
        i = 0
        for filename in self.multipleFiles:
            meta = GetMetadataClass(str(filename))
            exposure = meta.get_exposure()

            valoresLAB = getImageColors(self.coords, str(filename), self.icc)
            noise = GetNoiseClass(valoresLAB.get_rgb_values())

            self.check_item(os.path.basename(str(filename)))

            o[i] = {}
            o[i]["FILENAME"] = os.path.basename(str(filename))
            o[i]["ISO"] = exposure[2]
            o[i]["SNRRGB"] = noise.getRGB()
            o[i]["SNR"] = noise.getSNR()

            i = i + 1

        r = []
        for x in o:
            # filename = o[x]["FILENAME"]
            iso = o[x]["ISO"]
            fn = o[x]["FILENAME"]
            items = o[x]["SNR"]
            #r.append(((iso, fn), items))
            r.append({ "File": fn,
                       "ISO":iso,
                       "curve": items["curve"],
                       "stats": items["stats"],
                       "x_axis": items["x_axis"]
                       })

        return r

    def get_m_deltas(self):

        o = {}
        i = 0
        for filename in self.multipleFiles:
            valoresLAB = getImageColors(self.coords, str(filename), self.icc)
            valoresReferencia = GetCGATSClass(self.cgats)

            deltas = GetDeltasClass(valoresLAB.get_lab_values(), valoresReferencia.labCGATS)

            self.check_item(os.path.basename(str(filename)))

            o[i] = {}
            o[i]["FILENAME"] = os.path.basename(str(filename))
            o[i]["CIE76"] = deltas.get_cie76()
            o[i]["CIE00"] = deltas.get_cie00()
            # o[i]["CIE94"] = deltas.getCIE94()
            # o[i]["CMC"] =   deltas.getCMC()

            i = i + 1

        return o

    def get_means_color(self, field):

        arr = self.get_m_deltas()

        o = []
        for x in arr:
            filename = arr[x]["FILENAME"]
            means = arr[x][field]["stats"]

            o.append((filename, float(means['Average'])))

        return o
        # print(o)

    def get_m_dev(self):

        arr = self.get_m_deltas()

        patches = self.charts.get_gray_scale(self.chartIndex)
        o = []
        for x in arr:
            filename = arr[x]["FILENAME"]
            items = arr[x]["DEV"]
            scale = [items[i] for i in patches]
            o.append((filename, scale))

        return o
        # print(o)

    def get_patch_name(self, reference):
        patchName = []
        for patch in reference:
            patchName.append(patch["SAMPLE_ID"])
        return patchName

    def get_density_name(self, reference):
        patchName = []
        for patch in reference:
            patchName.append(patch["D_VIS"])
        return patchName

    def get_m_oecf(self):

        o = {}
        i = 0
        for filename in self.multipleFiles:
            meta = GetMetadataClass(str(filename))
            filen = os.path.basename(str(filename))
            exposure = meta.get_exposure() + (filen,)

            valoresLAB = getImageColors(self.coords, str(filename), self.icc)
            valoresReferencia = GetCGATSClass(self.cgats)

            #OECF = GetOECFClass(valoresLAB.get_rgb_values(), valoresReferencia.RGB, valoresLAB.get_lab_values(),
            #                           valoresReferencia.labCGATS)

            OECF = GetOECFClass(valoresLAB.get_rgb_values(), valoresLAB.get_lab_values(), valoresReferencia.labCGATS)


            self.check_item(os.path.basename(str(filename)))

            o[i] = {}
            o[i]["FILENAME"] = os.path.basename(str(filename))
            o[i]["OECF"] = OECF.get_oecf_values("OECF")
            o[i]["shutter"] = exposure[0]
            o[i]["aperture"] = exposure[1]
            o[i]["ISO"] = exposure[2]

            i = i + 1

        s = []
        for x in o:
            filename = o[x]["FILENAME"]
            items = o[x]["OECF"]
            shutter = o[x]["shutter"]
            aperture = o[x]["aperture"]
            ISO = o[x]["ISO"]
            # scale = [items[i] for i in patches]
            #arrD = []
            #for y in items[0]:
            #    arrD.append(y)

            s.append({ "File": filename,
                       "shutter": shutter,
                       "aperture":aperture,
                       "iso": ISO,
                       "curve": items["curve"],
                       "stats": items["stats"],
                       "x_axis": items["x_axis"]
                       })
            #s.append((exposure, arrD))

        return s

    def get_m_sentitometry(self):

        patches = self.charts.get_gray_scale(self.chartIndex)

        o = []

        for filename in self.multipleFiles:

            meta = GetMetadataClass(str(filename))
            filen = os.path.basename(str(filename))
            exposure = meta.get_exposure() + (filen,)

            self.check_item(os.path.basename(str(filename)))
            # print(exposure)
            valoresLAB = getImageColors(self.coords, str(filename), self.icc)

            LAB = valoresLAB.get_lab_values()
            scale = []

            for x in patches:
                scale.append(LAB[x - 1]['LAB'][0])

            o.append((exposure, scale))

        return o
