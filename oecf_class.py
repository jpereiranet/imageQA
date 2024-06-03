# -*- coding: utf-8 -*-
import math
from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, LCHabColor
#from scipy.signal import savgol_filter

import numpy as np



class GetOECFClass:

    def __init__(self, img_rgb, img_lab, ref_lab):


        self.imgRGB = img_rgb
        #self.refRGB = ref_rgb
        self.refLab = ref_lab
        self.imgLab = img_lab
        self.density = self.get_density_name(ref_lab)


    def get_density_name(self, reference):

        patchName = []
        for patch in reference:
            patchName.append(patch["D_VIS"])
        return patchName


    def new_order_by_list(self, dest):

        destino = np.array(dest)
        origen = np.array(self.density)
        inds = origen.argsort()
        sortedList = destino[inds]
        return sortedList.tolist()

    def getGain(self):

        total = len(self.imgLab)
        orig = []
        ref = []
        for x in range(total):

            lOrig = self.imgLab[x]["LAB"][0]
            lRef = self.refLab[x]["LAB_L"]

            orig.append(lOrig)
            ref.append(lRef)

        npOrig = np.array(orig)
        npRef = np.array(ref)

        firstDerivative = np.diff(npOrig) / np.diff(npRef)

        o = firstDerivative.tolist()
        #o = savgol_filter(o, total, 3)

        s = self.get_oecf_stats(o, "LGAIN")

        sorted(self.density)
        str_density = []
        for d in self.density:
            str_density.append(str(d))

        return {"curve": o, "stats":s, "x_axis": str_density }




    def get_oecf_values(self, mode):

        o = []
        #t = []
        #to =[]
        #meter aqui una validación de numero de parches!!!!
        #count_rgb_img = len(self.imgRGB)
        #count_rgb_ref = len(self.imgRGB)

        total = len(self.imgRGB)

        for x in range(total):

            Ri = self.imgRGB[x]["RGB"][0]
            Gi = self.imgRGB[x]["RGB"][1]
            Bi = self.imgRGB[x]["RGB"][2]
            luma_img = self.imgRGB[x]["RGB_LUMA"]


            Rr = self.refLab[x]["RGB_R"]
            Gr = self.refLab[x]["RGB_G"]
            Br = self.refLab[x]["RGB_R"]

            luma_ref = self.refLab[x]["LUMA"]

            #print(self.imgLab[x])

            if mode == "WB":

                color1 = LabColor(lab_l=self.refLab[x]["LAB_L"], lab_a=self.refLab[x]["LAB_A"], lab_b=self.refLab[x]["LAB_B"] )
                #print(self.refLab[x]["LAB_L"])
                color2 = LabColor(lab_l=self.imgLab[x]["LAB"][0], lab_a=self.imgLab[x]["LAB"][1], lab_b=self.imgLab[x]["LAB"][2])

                lch1 = convert_color(color1, LCHabColor)
                lch2 = convert_color(color2, LCHabColor)

                DeC = abs(lch1.lch_c - lch2.lch_c)

                o.append(DeC)

            if mode == "L-OECF":

                L_REF = self.refLab[x]["LAB_L"]
                L_IMG = self.imgLab[x]["LAB"][0]

                o.append([round(L_IMG, 0), round(L_REF, 0)])


            if mode == "OECF":

                #Co = self.value_to_percent(self.imgRGB[x]["RGB"])
                #Ci = self.value_to_percent(self.refRGB[x])

                Yo = luma_img
                Yi = luma_ref

                o.append([round(Yo, 0), round(Yi, 0)])

            elif mode == "RGB":

                o.append([Ri, Gi, Bi])


            elif mode == "RED":

                o.append([Ri, Rr])


            elif mode == "GREEN":

                o.append([Gi, Gr])


            elif mode == "BLUE":

                o.append([Bi, Br])


            elif mode == "DEV":

                Yo = luma_img
                Yi = luma_ref
                dev = self.get_delta_ev(round(Yo, 1), round(Yi, 1))
                o.append(dev)

        #s = self.get_oecf_stats(o, mode)

        o = self.new_order_by_list(o)

        s = self.get_oecf_stats(o, mode)


        #if mode == "OECF":
        #    slope2 = self.best_fit_slope(o)
        #    print("slope2", slope2)

        sorted(self.density)
        str_density = []
        for d in self.density:
            str_density.append(str(d))

        return {"curve": o, "stats":s, "x_axis": str_density }

    '''
    def best_fit_slope(self, o):

        from statistics import mean

        curva = self.get_curves(o)
        ys = np.array(curva, dtype=np.float64)
        ys.sort()
        print("Y", ys)
        xs = np.array(self.desity_trans(self.density), dtype=np.float64)
        xs.sort()
        print("X",xs)
        slope, intercept = np.polyfit(np.log(xs), np.log(ys), 1)
        print("slope", slope)
        #https://pythonprogramming.net/how-to-program-best-fit-line-slope-machine-learning-tutorial/
        m = (((mean(xs) * mean(ys)) - mean(xs * ys)) /
             ((mean(xs) ** 2) - mean(xs ** 2)))
        return m
        '''
    def desity_trans(self,d):
        o = []
        for x in d:
            o.append(math.pow(10, -1 * float(x)))
        print("transmison", o)
        return o

    def get_curves(self,c):
        o = []
        for x in c:
            o.append(x[0]/255)

        print("curvaY", o)
        return o

    def get_oecf_stats(self, arr, mode):
        t = []
        # print(arr)

        for x in range(len(arr)):
            # print(len(arr[x]) )
            if type(arr[x]) is list:
                # is OECF
                if len(arr[x]) == 2:
                    d = abs(arr[x][0] - arr[x][1])
                    t.append(d)
                # is RGB
                if len(arr[x]) == 3:
                    # print(self.stddev( arr[x], ddof=0))
                    t.append(self.stddev(arr[x], ddof=0))

            else:
                # is DEV or WB
                t.append(arr[x])

        if mode == "WB":
            o = {"units": "∆C",
                 "Err Avg": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2)),
                 "Err Desv": str(round(self.stddev(t, ddof=0), 2))
                 }

        if mode == "LGAIN":
            o = {"units": "",
                 "Err Avg": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2))
                 }
        if mode == "L-OECF":

            o = {"units": "L*",
                 "Err Avg": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2)),
                 "Err Desv": str(round(self.stddev(t, ddof=0), 2))
                 }

        if mode == "OECF":

            o = {"units": "cv",
                 "Err Avg": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2)),
                 "Err Desv": str(round(self.stddev(t, ddof=0), 2))
                 }

        elif mode == "RED" or mode == "GREEN" or mode == "BLUE":

            o = {"units": "cv",
                 "Err Avg": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2)),
                 "Err Desv": str(round(self.stddev(t, ddof=0), 2))
                 }
        elif mode == "RGB":

            o = {"units": "cv",
                 "Desv Avg": str(round(self.mean(t), 2)),
                 "Desv Max": str(round(max(t), 2)),
                 "Desv Min": str(round(min(t), 2))

                 }

        elif mode == "DEV":

            o = {"units": "∆EV",
                 "Err Average": str(round(self.mean(t), 2)),
                 "Err Max": str(round(max(t), 2)),
                 "Err Min": str(round(min(t), 2)),
                 "Err Desv": str(round(self.stddev(t, ddof=0), 2))
                 }

        return o



    def gain_modulation(self,sI, SI1, rI, rI1):

        o = (sI - SI1) / (rI - rI1)

        return o

    def value_to_percent(self, color):

        o = []
        for x in color:
            c = (x / 255) * 100
            o.append(c)
        return o

    def get_luma(self, RGB):

        if len(RGB) > 1:
            y = 0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]
        else:
            y = RGB[0]

        return y

    def get_delta_ev(self, Yo, Yi):

        return (math.log(Yo) - math.log(Yi)) / math.log(2)

    def mean(self, data):
        """Return the sample arithmetic mean of data."""
        n = len(data)
        if n < 1:
            raise ValueError('mean requires at least one data point')
        # print(data)
        return sum(data) / float(n)  # in Python 2 use sum(data)/float(n)

    def _ss(self, data):
        """Return sum of square deviations of sequence data."""
        c = self.mean(data)
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
