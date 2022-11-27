# -*- coding: utf-8 -*-
# from curses.ascii import NUL
from app_paths import DefinePathsClass
import configparser
from os import path



class ChartPatternsClass:

    def __init__(self):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        self.conf_default = False
        if path.exists(path_conf_file):
            self.config.read(path_conf_file)
        else:
            self.conf_default = True

        self.Y_ROI = 0
        self.X_ROI = 0

        # tuple order: function, (isRoi,lock), (btDeltas, btCgats, btNeutral, btMTF, btNoise,btOCF, btConfingCamera,openSPD,openDiffStats, openLensAberr), (white, middlegray, black)
        self.chartsType = {"---": (None, None, None, None),
                           "Colorchecker Classic": (
                           self.colorchecker_classic_pattern, (False, True), (True, True, False, False, False, False, False, False, False, False),
                           (18, 21, 23)),
                           "Colorchecker SG": (
                           self.colorchecker_SG_pattern, (False, True), (True, True, False, False, False, False, False, False, False, False),
                           (75, 78, 80)),
                           "ROI": (self.roi_pattern, (True, False), (False, False, True, False, False, False, True, True, False, False)),
                           "SFR/MTF": (self.mtf_pattern, (True, True), (False, False, False, True, False, False, True, False, False, False)),
                           "Sampling": (self.set_scale, (False, False), (False, False, False, False, False, False, True, False, False, False)),

                           "GS Colorchecker Classic": (
                           self.colorchecker_classic_gray_scale, (False, True), (False, True, False, False, True, True, False, False, False, False),
                           (1, 4, 6)),
                           "GS Colorchecker SG": (
                           self.colorchecker_sg_gray_scale, (False, True),(False, True, False, False, True, True, False, False, False, False),
                           (1, 4, 7)),
                           "Kodak Q13 step-wedge": (
                           self.kodak_q13, (False, True), (False, True, False, False, True, True, False, False, False, False), (1, 8, 17)),
                           "IT8": (self.it8_color, (False, True), (True, True, False, False, False, False, False, False, False, False), (18, 21, 23)),
                           "Custom": ( self.custom_pattern, (False, True), (True, True, False, False, True, True, False, False, False, False),(18, 21, 23)),
                           "Full": (self.full_pattern, (True, False),
                                   (False, False, True, False, False, False, True, True, False, False)),

                           }

    def get_chart(self, index):

        arrKey = sorted(self.chartsType.keys())
        return self.chartsType[arrKey[index]][0]()

    def get_chart_name(self, index):
        arr_key = sorted(self.chartsType.keys())
        return arr_key[index]

    def is_roi(self, index):
        arr_key = sorted(self.chartsType.keys())
        return self.chartsType[arr_key[index]][1][0]

    def is_lock(self, index):
        arr_key = sorted(self.chartsType.keys())
        return self.chartsType[arr_key[index]][1][1]

    def get_gray_scale(self, index):

        arrKey = sorted(self.chartsType.keys())
        return self.chartsType[arrKey[index]][3]

    def get_switch(self, index):

        arrKey = sorted(self.chartsType.keys())
        return self.chartsType[arrKey[index]][2]

    def colorchecker_classic_pattern(self):

        if self.conf_default:
            margen = 20
            filas = 4
            columnas = 6
            espaciado = 38
            sizeBox = 20
            wroi = 230
            hroi = 150
            reference = "ColorChecker_Built_In.txt"

        else:
            margen = int(self.config['COLORCHECKER_CLASSIC']['MARGIN'])
            filas = int(self.config['COLORCHECKER_CLASSIC']['ROWS'])
            columnas = int(self.config['COLORCHECKER_CLASSIC']['COLUMNS'])
            espaciado = float(self.config['COLORCHECKER_CLASSIC']['SPACING'])
            sizeBox = int(self.config['COLORCHECKER_CLASSIC']['SIZEBOX'])
            wroi = int(self.config['COLORCHECKER_CLASSIC']['WROI'])
            hroi = int(self.config['COLORCHECKER_CLASSIC']['HROI'])
            reference = self.config['COLORCHECKER_CLASSIC']['REFERENCE']

        ## Patron para la Colorchecker
        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        # reference = "reference/ColorChecker_Built_In.txt"
        reference = DefinePathsClass.create_reference_paths(reference.strip('"'))

        return [pos, symbols, sizeBox, reference, wroi, hroi]

    def custom_pattern(self):

        if self.conf_default:
            margen = 20
            filas = 4
            columnas = 6
            espaciado = 38
            sizeBox = 20
            wroi = 230
            hroi = 150
            reference = ""

        else:
            margen = int(self.config['CUSTOM_CHART']['MARGIN'])
            filas = int(self.config['CUSTOM_CHART']['ROWS'])
            columnas = int(self.config['CUSTOM_CHART']['COLUMNS'])
            espaciado = float(self.config['CUSTOM_CHART']['SPACING'])
            sizeBox = int(self.config['CUSTOM_CHART']['SIZEBOX'])
            wroi = int(self.config['CUSTOM_CHART']['WROI'])
            hroi = int(self.config['CUSTOM_CHART']['HROI'])
            reference = self.config['CUSTOM_CHART']['REFERENCE']

        ## Patron para la Colorchecker
        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        # reference = "reference/ColorChecker_Built_In.txt"
        reference = DefinePathsClass.create_reference_paths(reference.strip('"'))

        return [pos, symbols, sizeBox, reference, wroi, hroi]


    def colorchecker_SG_pattern(self):

        if self.conf_default:
            margen = 10
            filas = 10
            columnas = 14
            espaciado = 16
            sizeBox = 5
            wroi = 230
            hroi = 170
            reference = "ColorChecker_Built_In.txt"

        else:
            margen = int(self.config['COLORCHECKER_SG']['MARGIN'])
            filas = int(self.config['COLORCHECKER_SG']['ROWS'])
            columnas = int(self.config['COLORCHECKER_SG']['COLUMNS'])
            espaciado = float(self.config['COLORCHECKER_SG']['SPACING'])
            sizeBox = int(self.config['COLORCHECKER_SG']['SIZEBOX'])
            wroi = int(self.config['COLORCHECKER_SG']['WROI'])
            hroi = int(self.config['COLORCHECKER_SG']['HROI'])
            reference = self.config['COLORCHECKER_SG']['REFERENCE']

        ## Patron para la Colorchecker
        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        ## archivo de referencia
        reference = DefinePathsClass.create_reference_paths( reference.strip('"') )

        return [pos, symbols, sizeBox, reference, wroi, hroi]

    def colorchecker_classic_gray_scale(self):


        if self.conf_default:
            margen = 20
            filas = 1
            columnas = 6
            espaciado = 38
            sizeBox = 20
            wroi = 230
            hroi = 40
            reference = "ColorChecker_Built_In_GS.txt"

        else:
            margen = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['MARGIN'])
            filas = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['ROWS'])
            columnas = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['COLUMNS'])
            espaciado = float(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['SPACING'])
            sizeBox = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['SIZEBOX'])
            wroi = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['WROI'])
            hroi = int(self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['HROI'])
            reference = self.config['COLORCHECKER_CLASSIC_GRAYSCALE']['REFERENCE']

        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        reference = DefinePathsClass.create_reference_paths( reference.strip('"') )

        return [pos, symbols, sizeBox, reference, wroi, hroi]

    def kodak_q13(self):

        if self.conf_default:
            margen = 6
            filas = 1
            columnas = 20
            espaciado = 11.5
            sizeBox = 5
            wroi = 230
            hroi = 15
            reference = ""

        else:
            margen = float(self.config['KODAK_Q13']['MARGIN'])
            filas = int(self.config['KODAK_Q13']['ROWS'])
            columnas = int(self.config['KODAK_Q13']['COLUMNS'])
            espaciado = float(self.config['KODAK_Q13']['SPACING'])
            sizeBox = int(self.config['KODAK_Q13']['SIZEBOX'])
            wroi = int(self.config['KODAK_Q13']['WROI'])
            hroi = int(self.config['KODAK_Q13']['HROI'])
            reference = self.config['KODAK_Q13']['REFERENCE']

        ## Patron para la Colorchecker
        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        if reference is not "":
            reference = DefinePathsClass.create_reference_paths(reference.strip('"'))
        else:
            reference = ""

        return [pos, symbols, sizeBox, reference, wroi, hroi]

    def roi_pattern(self):

        if self.conf_default:
            wroi = 230
            hroi = 150
        else:
            wroi = int(self.config['ROI']['WROI'])
            hroi = int(self.config['ROI']['HROI'])

        return ["", "", "", "", wroi, hroi]

    def full_pattern(self):

        return ["", "", "", "", "", ""]

    def mtf_pattern(self):

        if self.conf_default:
            wroi = 50
            hroi = 50
        else:
            wroi = int(self.config['SFR']['WROI'])
            hroi = int(self.config['SFR']['HROI'])

        return ["", "", "", "", wroi, hroi]

    def set_scale(self):

        if self.conf_default:
            wroi = 100
            hroi = 50
        else:
            wroi = int(self.config['SAMPLING_RULE']['WROI'])
            hroi = int(self.config['SAMPLING_RULE']['HROI'])
        return ["", "", "", "", wroi, hroi]

    def it8_color(self):

        if self.conf_default:
            margen = 12
            filas = 12
            columnas = 22
            espaciado = 9
            sizeBox = 5
            wroi = 230
            hroi = 145
            reference = ""

        else:
            margen = int(self.config['IT8']['MARGIN'])
            filas = int(self.config['IT8']['ROWS'])
            columnas = int(self.config['IT8']['COLUMNS'])
            espaciado = float(self.config['IT8']['SPACING'])
            sizeBox = int(self.config['IT8']['SIZEBOX'])
            wroi = int(self.config['IT8']['WROI'])
            hroi = int(self.config['IT8']['HROI'])
            reference = self.config['IT8']['REFERENCE']

        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = espaciado + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        sY = Y + espaciado + (espaciado / 2)

        X = 3
        for z in range(0, 24):
            X = X + espaciado
            a = []
            a.append(X)
            a.append(sY)
            pos.append(a)
            symbols.append('s')

        #reference = DefinePathsClass.create_reference_paths("")
        if reference is not "":
            reference = DefinePathsClass.create_reference_paths(reference.strip('"'))
        else:
            reference = ""

        return [pos, symbols, sizeBox, reference, wroi, hroi]


    def colorchecker_sg_gray_scale(self):

        if self.conf_default:
            margen = 15
            filas = 2
            columnas = 6
            espaciado = 38
            sizeBox = 15
            wroi = 220
            hroi = 70
            reference = ""

        else:
            margen = int(self.config['COLORCHECKER_SG_GRAYSCALE']['MARGIN'])
            filas = int(self.config['COLORCHECKER_SG_GRAYSCALE']['ROWS'])
            columnas = int(self.config['COLORCHECKER_SG_GRAYSCALE']['COLUMNS'])
            espaciado = float(self.config['COLORCHECKER_SG_GRAYSCALE']['SPACING'])
            sizeBox = int(self.config['COLORCHECKER_SG_GRAYSCALE']['SIZEBOX'])
            wroi = int(self.config['COLORCHECKER_SG_GRAYSCALE']['WROI'])
            hroi = int(self.config['COLORCHECKER_SG_GRAYSCALE']['HROI'])
            reference = self.config['COLORCHECKER_SG_GRAYSCALE']['REFERENCE']

        ## Patron para la Colorchecker
        symbols = []
        pos = []
        Y = self.Y_ROI + margen
        for y in range(filas):
            X = self.X_ROI + margen
            for x in range(columnas):
                a = []
                a.append(X)
                a.append(Y)
                pos.append(a)
                symbols.append('s')
                if x < columnas:
                    X = X + espaciado
                else:
                    x = 0
            if y < filas:
                Y = Y + espaciado
            else:
                y = 0

        # reference = "reference/ColorChecker_Built_In.txt"
        reference = DefinePathsClass.create_reference_paths(reference.strip('"'))
        ## archivo de referencia
        return [pos, symbols, sizeBox, reference, wroi, hroi]
