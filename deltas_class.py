# -*- coding: utf-8 -*-
from colormath.color_conversions import convert_color
from colormath.color_diff import delta_e_cie1976, delta_e_cie1994, \
    delta_e_cie2000, delta_e_cmc
from colormath.color_objects import LabColor, LCHabColor
from app_paths import DefinePathsClass
import configparser
from os import path


class GetDeltasClass:
    '''
    imgLab son los valores Lab de la imagen
    targRef son los valores lab del archivo de referencia
    '''

    def __init__(self, imgLab, targRef):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        if path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.observer = self.config['SAMPLING']['DEFAULT_OBSERVER']
        else:
            self.observer = 2

        self.imgLab = imgLab
        self.targRef = targRef
        self.patches = self.get_patch_name(targRef)
        self.rgbcolor_patches = self.get_patch_rgbcolor(targRef)

    def get_patch_name(self, reference):
        patchName = []
        for patch in reference:
            patchName.append(patch["SAMPLE_ID"])
        return patchName

    def get_patch_rgbcolor(self, reference):
        patchcolor = []
        for patch in reference:
            patchcolor.append([patch["RGB_R"],patch["RGB_G"],patch["RGB_B"]])
        return patchcolor

    def get_cie76(self):


        deltaCIE76 = []
        colorOriginal = []
        colorObtenido = []

        o = {}

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            deltaCIE76.append(round(delta_e_cie1976(color1, color2),2))
            colorObtenido.append( (self.imgLab[i]['LAB'][0],self.imgLab[i]['LAB'][1],self.imgLab[i]['LAB'][2])  )
            colorOriginal.append( (self.targRef[i]['LAB_L'],self.targRef[i]['LAB_A'],self.targRef[i]['LAB_B'] ) )

        #o.append([deltaCIE76, self.do_stats(deltaCIE76, "∆e")])


        o = {
            "curve":deltaCIE76,
            "stats":self.do_stats(deltaCIE76, "∆e"),
            "x_axis":self.patches,
            "colorOrig":colorOriginal,
            "colorDest":colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def string_to_float(self, string):

        try:
            return float(string)
        except:
            return float( string.replace(',','.') )

    def get_cie00(self):

        deltaCIE00 = []
        o = {}
        colorOriginal = []
        colorObtenido = []

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            deltaCIE00.append(round(delta_e_cie2000(color1, color2),2))
            colorObtenido.append( (self.imgLab[i]['LAB'][0],self.imgLab[i]['LAB'][1],self.imgLab[i]['LAB'][2])  )
            colorOriginal.append( (self.targRef[i]['LAB_L'],self.targRef[i]['LAB_A'],self.targRef[i]['LAB_B'] ) )


        #o.append([deltaCIE00, self.do_stats(deltaCIE00, "∆e")])
        o = {
            "curve":deltaCIE00,
            "stats":self.do_stats(deltaCIE00, "∆e"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def get_cie94(self):

        deltaCIE94 = []
        o = {}
        colorOriginal = []
        colorObtenido = []

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            deltaCIE94.append(round(delta_e_cie1994(color1, color2),2))
            colorObtenido.append( (self.imgLab[i]['LAB'][0],self.imgLab[i]['LAB'][1],self.imgLab[i]['LAB'][2])  )
            colorOriginal.append( (self.targRef[i]['LAB_L'],self.targRef[i]['LAB_A'],self.targRef[i]['LAB_B'] ) )


        #o.append([deltaCIE94, self.do_stats(deltaCIE94, "∆e")])
        o = {
            "curve":deltaCIE94,
            "stats":self.do_stats(deltaCIE94, "∆e"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }
        return o

    def get_cmc(self):

        colorOriginal = []
        colorObtenido = []
        deltaCMCconformidad = []
        o = {}

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            deltaCMCconformidad.append(round(delta_e_cmc(color1, color2, pl=2, pc=1),2))  # conformidad
            colorObtenido.append((self.imgLab[i]['LAB'][0], self.imgLab[i]['LAB'][1], self.imgLab[i]['LAB'][2]))
            colorOriginal.append((self.targRef[i]['LAB_L'], self.targRef[i]['LAB_A'], self.targRef[i]['LAB_B']))

        #o.append([deltaCMCconformidad, self.do_stats(deltaCMCconformidad, "∆e")])
        o = {
            "curve":deltaCMCconformidad,
            "stats":self.do_stats(deltaCMCconformidad, "∆e"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def get_d_chroma(self):

        colorOriginal = []
        colorObtenido = []
        deltaChroma = []
        o = {}

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            lch1 = convert_color(color1, LCHabColor)
            lch2 = convert_color(color2, LCHabColor)

            DeC = lch1.lch_c - lch2.lch_c
            deltaChroma.append(round(abs(DeC),2))

            colorOriginal.append( round(lch1.lch_c,2) )
            colorObtenido.append( round(lch2.lch_c,2) )


        #o.append([deltaChroma, self.do_stats(deltaChroma, "∆C")])
        o = {
            "curve":deltaChroma,
            "stats":self.do_stats(deltaChroma, "∆C"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def get_d_lightness(self):

        colorOriginal = []
        colorObtenido = []
        deltaLigtness = []
        o = {}

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            lch1 = convert_color(color1, LCHabColor)
            lch2 = convert_color(color2, LCHabColor)

            DeL = lch1.lch_l - lch2.lch_l

            deltaLigtness.append(round(abs(DeL),2))
            colorOriginal.append( round(lch1.lch_l,2) )
            colorObtenido.append( round(lch2.lch_l,2) )


        #o.append([deltaLigtness, self.do_stats(deltaLigtness, "∆L")])
        o = {
            "curve":deltaLigtness,
            "stats":self.do_stats(deltaLigtness, "∆L"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def get_d_hue(self):

        colorOriginal = []
        colorObtenido = []
        deltaHue = []
        o = {}

        for i in range(len(self.imgLab)):
            color1 = LabColor(lab_l=self.imgLab[i]['LAB'][0], lab_a=self.imgLab[i]['LAB'][1],
                              lab_b=self.imgLab[i]['LAB'][2], observer=self.observer.strip('"'), illuminant=self.imgLab[i]['LAB'][3])
            color2 = LabColor(lab_l=self.targRef[i]['LAB_L'], lab_a=self.targRef[i]['LAB_A'], lab_b=self.targRef[i]['LAB_B'])

            lch1 = convert_color(color1, LCHabColor)
            lch2 = convert_color(color2, LCHabColor)

            DeH = lch1.lch_h - lch2.lch_h

            deltaHue.append(round(abs(DeH),2))
            colorOriginal.append( round(lch1.lch_h,2) )
            colorObtenido.append( round(lch2.lch_h,2) )


        #o.append([deltaHue, self.do_stats(deltaHue, "∆H")])
        o = {
            "curve":deltaHue,
            "stats":self.do_stats(deltaHue, "∆H"),
            "x_axis":self.patches,
            "colorOrig": colorOriginal,
            "colorDest": colorObtenido,
            "RGB_COLOR_PATCHES":self.rgbcolor_patches
                }

        return o

    def find_grey_patches(self):

        o = []
        for x in range(len(self.targRef)):

            lab = LabColor(lab_l=self.targRef[x]['LAB_L'], lab_a=self.targRef[x]['LAB_A'], lab_b=self.targRef[x]['LAB_B'], observer=self.observer.strip('"'),
                           illuminant='D50')
            lch = convert_color(lab, LCHabColor)
            c = lch.lch_c
            # si es menor de 2 es que es un gris
            if c < 2:
                o.append(x)

        return o

    def get_chromatic_patches(self, arr):

        gray = self.find_grey_patches()

        o = []
        for x in range(len(arr)):

            if x not in gray:
                o.append(arr[x])

        return o

    def get_achromatic_patches(self, arr):

        gray = self.find_grey_patches()

        o = []
        for x in range(len(arr)):

            if x in gray:
                o.append(arr[x])

        return o

    def do_stats(self, arr, unit):

        max_value = round(max(arr), 2)
        min_value = round(min(arr), 2)
        avg_value = round(self.do_mean(arr), 2)
        desv_value = round(self.stddev(arr), 2)

        meanColorPatch = round(self.do_mean(self.get_chromatic_patches(arr)), 2)
        meanGrayPatch = round(self.do_mean(self.get_achromatic_patches(arr)), 2)

        o = {"units": unit,
             "Average": str(avg_value),
             "Max": str(max_value),
             "Min": str(min_value),
             "Desv": desv_value,
             "Average Chromatic": str(meanColorPatch),
             "Average Achromatic": str(meanGrayPatch)
             }
        return o
        # return [avg_value, max_value, min_value, desv_value]

    def do_mean(self, data):
        """Return the sample arithmetic mean of data."""
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        # print(data)
        return sum(data) / float(n)  # in Python 2 use sum(data)/float(n)

    def _ss(self, data):
        """Return sum of square deviations of sequence data."""
        c = self.do_mean(data)
        ss = sum((x - c) ** 2 for x in data)
        return ss

    def stddev(self, data, ddof=0):
        """Calculates the population standard deviation
        by default; specify ddof=1 to compute the sample
        standard deviation."""
        n = len(data)
        if n < 2:
            raise ValueError('variance requires at least two data points')
        ss = self._ss(data)
        pvar = ss / (n - ddof)
        return pvar ** 0.5
