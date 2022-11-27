from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor

from warning_class import AppWarningsClass

import math


class GetCGATSClass:

    def __init__(self, cgatsFile):
        self.cgatsFile = cgatsFile
        self.f = open(self.cgatsFile, "r")

        idxData = self.get_lab_from_cgats()
        self.read_cgats_file(idxData)
        #self.get_patch_name()
        #self.lab_to_rgb()

    def get_lab_from_cgats(self):

        start = 0
        end = 0
        for idx, item in enumerate(self.f):
            v = item.strip()

            if v == "BEGIN_DATA_FORMAT":
                start = idx
            if v == "END_DATA_FORMAT":
                end = idx

        self.f.seek(0)

        fields = []
        for idx, item in enumerate(self.f):

            if idx > start and idx < end:
                fields.append(item.split())

        if "SAMPLE_ID" not in fields[0]:
            return AppWarningsClass.critical_warn("CGATS file does not contain any SAMPLE_ID tag")
        if "LAB_L" not in fields[0]:
            return AppWarningsClass.critical_warn("CGATS file does not contain any LAB_L tag")
        if "LAB_A" not in fields[0]:
            return AppWarningsClass.critical_warn("CGATS file does not contain any LAB_A tag")
        if "LAB_B" not in fields[0]:
            return AppWarningsClass.critical_warn("CGATS file does not contain any LAB_B tag")

        if "D_VIS" in fields[0]:

            idxData = [i for i, e in enumerate(fields[0]) if
                       e == "SAMPLE_ID" or e == "LAB_L" or e == "LAB_A" or e == "LAB_B" or e == "D_VIS"]
        else:

            idxData = [i for i, e in enumerate(fields[0]) if
                       e == "SAMPLE_ID" or e == "LAB_L" or e == "LAB_A" or e == "LAB_B" ]

        return idxData


    def read_cgats_file(self, idxData):

        start = 0
        end = 0
        self.f.seek(0)
        for idx, item in enumerate(self.f):
            v = item.strip()

            if v == "BEGIN_DATA":
                start = idx
            if v == "END_DATA":
                end = idx

        self.f.seek(0)

        self.labCGATS = []

        for idx, item in enumerate(self.f):

            if item.strip() is not "" and not item.strip().startswith("#"):
                if idx > start and idx < end:
                    item = item.split()
                    values = []
                    for i in idxData:
                        values.append(item[i])


                    rgbr =  self.lab_to_rgb_2(values[1], values[2], values[3])[0]
                    rgbg = self.lab_to_rgb_2(values[1], values[2], values[3])[1]
                    rgbb = self.lab_to_rgb_2(values[1], values[2], values[3])[2]
                    LUMA = self.rgb_to_luma(rgbr, rgbg, rgbb)

                    if len(values) > 4:
                        dvis = values[4]
                    else:
                        dvis = self.RGB_to_density(LUMA )

                    refDic = {
                        "SAMPLE_ID":values[0],
                        "LAB_L":round(self.string_to_float(values[1]),2),
                        "LAB_A":round(self.string_to_float(values[2]),2),
                        "LAB_B":round(self.string_to_float(values[3]),2),
                        "RGB_R": rgbr,
                        "RGB_G": rgbg,
                        "RGB_B": rgbb,
                        "D_VIS": round(self.string_to_float(dvis),2),
                        "LUMA": LUMA
                    }
                    self.labCGATS.append(refDic)
                    #self.labCGATS.append([values[0],self.string_to_float(values[1]),self.string_to_float(values[2]),self.string_to_float(values[3])])

        #print(self.labCGATS)
        return self.labCGATS

    def rgb_to_luma(self, rgbr, rgbg, rgbb):

        y = 0.2126 * rgbr + 0.7152 * rgbg + 0.0722 * rgbb
        return round(y,0)

    def RGB_to_density(self, luma):

        density = round( math.log10(math.pow((255 / luma), 2.2)), 2)
        return density


    def lab_to_rgb_2(self, CIEL,CIEa,CIEb):
        '''
        Convierte a RGB para colorear las barras de los graficos para una comprension viusal
        '''
        lab = LabColor(CIEL,CIEa,CIEb)
        rgb = convert_color(lab, sRGBColor)
        a = vars(rgb)
        g = self.check_rgb_range(round(a["rgb_g"] * 255))
        r = self.check_rgb_range(round(a["rgb_r"] * 255))
        b = self.check_rgb_range(round(a["rgb_b"] * 255))
        return r, g, b

    def string_to_float(self, string):

        try:
            return float(string)
        except:
            return float(string.replace(',', '.'))
    '''
    def get_patch_name(self):

        self.patchName = []
        for patch in self.labCGATS:
            self.patchName.append(patch[0])

        # print(self.patchName)
    '''
    def lab_to_rgb(self):
        '''
        Convierte a RGB para colorear las barras de los graficos para una comprension viusal
        '''
        self.RGB = []
        for patch in self.labCGATS:
            # aRGB = []
            lab = LabColor(patch[1], patch[2], patch[3])
            rgb = convert_color(lab, sRGBColor)
            a = vars(rgb)
            g = self.check_rgb_range(round(a["rgb_g"] * 255))
            r = self.check_rgb_range(round(a["rgb_r"] * 255))
            b = self.check_rgb_range(round(a["rgb_b"] * 255))
            self.RGB.append([r, g, b])



    def check_rgb_range(self, value):

        if value > 255:
            return 255
        else:
            return value
