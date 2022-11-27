# -*- coding: utf-8 -*-

import math
import numpy

class GetNoiseClass():

    def __init__(self, imgRGB):

        self.imgRGB = imgRGB
        #self.refRGB = refRGB
        self.x_scale = self.get_x_axis()
        #self.x_scale_d = self.get_x_axis_density()

    '''
    def get_x_axis_density(self):
        y = []
        for x in range(len(self.refRGB)):
            D = float(self.refRGB[x]["D_VIS"])
            y.append(D)
        return y
    '''

    def get_x_axis(self):
        y = []
        for x in range(len(self.imgRGB)):
            EV = self.luma_to_ev(self.imgRGB[x]["RGB_LUMA"])
            y.append(round(EV,1))
        return y

    def new_order_by_list(self, dest,scale):

        destino = numpy.array(dest)
        origen = numpy.array(scale)
        inds = numpy.argsort(-origen)
        sortedList = destino[inds]
        return sortedList.tolist()


    def getRGB(self):
        o = []
        total = len(self.imgRGB)
        for x in range(total):
            r = self.imgRGB[x]["RGB"][0]
            g = self.imgRGB[x]["RGB"][1]
            b = self.imgRGB[x]["RGB"][2]

            rstv = self.imgRGB[x]["RGB_DESV"][0]
            gstv = self.imgRGB[x]["RGB_DESV"][1]
            bstv = self.imgRGB[x]["RGB_DESV"][2]

            rn = self.SNR(r, rstv)
            gn = self.SNR(g, gstv)
            bn = self.SNR(b, bstv)
            o.append([rn, gn, bn])

        s = self.stats(o, "RGB")

        return {"curve": self.new_order_by_list(o,self.x_scale), "stats": s, "x_axis": sorted(self.x_scale,reverse=True)}


    def gain_modulation(self,sI, SI1, rI, rI1):

        o = (sI - SI1) / (rI - rI1)
        return o

    def getCromaNoise(self):

        o = []

        total = len(self.imgRGB)

        for x in range(total):

            rDesv = self.imgRGB[x]["RGB_DESV"][0]
            #gDesv = self.imgRGB[x]["RGB_DESV"][1]
            bDesv = self.imgRGB[x]["RGB_DESV"][2]

            Ydesv = self.imgRGB[x]["RGB_YDESV"]

            desv = math.sqrt( math.pow(Ydesv, 2 ) + (0.64*math.pow(rDesv-Ydesv, 2 )) +  (0.16*math.pow(bDesv-Ydesv, 2 )) )

            o.append(desv)

        s = self.stats(o, "cNoise")

        #print(self.new_order_by_list(o,self.x_scale))

        return {"curve": self.new_order_by_list(o,self.x_scale), "stats": s, "x_axis": sorted(self.x_scale,reverse=True)}


    def getSNR(self):

        o = []
        t = []
        total = len(self.imgRGB)
        for x in range(total):

            mY = self.imgRGB[x]["RGB_LUMA"]

            YSTV = self.mean(self.imgRGB[x]["RGB_DESV"])

            o.append(self.SNR(mY, YSTV))

        s = self.stats(o, "SNR")

        #print(self.x_scale)

        return {"curve": self.new_order_by_list(o,self.x_scale), "stats": s, "x_axis": sorted(self.x_scale,reverse=True)}

    '''
    def getDR(self):

        o = []
        for x in range(len(self.imgRGB)):
            #mSTV = self.mean(self.imgRGB[x]["RGB_DESV"])

            maxR = self.imgRGB[x]["RGB_extrema"][0][1]
            maxG = self.imgRGB[x]["RGB_extrema"][1][1]
            maxB = self.imgRGB[x]["RGB_extrema"][2][1]

            YSTV = self.mean(self.imgRGB[x]["RGB_DESV"])

            #maxY = self.mean( [maxR, maxG, maxB])
            mY = self.imgRGB[x]["RGB_LUMA"]

            DR = math.log2(mY) - math.log2(YSTV)

            o.append( DR )

        s = self.stats(o, "RDEV")

        return {"curve": o, "stats": s}
    '''


    def luma(self, RGB):

        if len(RGB) > 1:
            y = 0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]
        else:
            y = RGB[0]

        return y

    def luma_to_ev(self, luma):
        re =  math.pow( luma/255, 2.2)
        return math.log2(re)

    def SNR(self, mean, desv):
        #print("mean", mean )
        #print("desv", desv )

        if desv > 0:  ### hay que ver que pasa si p es 0 o la desv es 0
            snr = 20 * math.log10(mean / desv)
            #print("snr", snr)
            return snr
        else:
            return 20 * math.log10(mean)


    def stats(self, arr, mode):
        t = []
        # print(arr)

        for x in range(len(arr)):
            # print(len(arr[x]) )
            if type(arr[x]) is list:
                # is OECF
                # if len(arr[x]) == 2:
                #    d = abs(arr[x][0] - arr[x][1])
                #    t.append(d)
                # is RGB
                if len(arr[x]) == 3:
                    # print(self.stddev( arr[x], ddof=0))
                    t.append(self.stddev(arr[x], ddof=0))

            else:
                # is DEV
                t.append(arr[x])

        if mode == "RGB":

            o = {
                 "Desv Avg": [str(round(self.mean(t), 2)), "db"],
                 "Desv Max": [str(round(max(t), 2)), "db"],
                 "Desv Min": [str(round(min(t), 2)), "db"]

                 }

        elif mode == "SNR":

            o = {
                 "Average": [str(round(self.mean(t), 2)), "db"],
                 "Max": [str(round(max(t), 2)), "db"],
                 "Min": [str(round(min(t), 2)), "db"],
                 "Desv": [str(round(self.stddev(t, ddof=0), 2)), "db"],
                 "EV": [str(round(self.mean(t) / 6, 2)), "EV"], #Para pasar de db a EV
                 "Contrast": [ str(int(math.pow(10, math.log10(2)* (self.mean(t)/ 6) )))+":1" ,""]
                 }

        elif mode == "cNoise":

            o = {
                 "Average": [str(round(self.mean(t), 2)), "σ"],
                 "Max": [str(round(max(t), 2)), "σ"],
                 "Min": [str(round(min(t), 2)), "σ"],
                 "Desv": [str(round(self.stddev(t, ddof=0), 2)), "σ"]
                 }
        '''
        elif mode == "DENSITY":
            o = {"units": "D",
                 "Max": str(round(max(t), 2)),
                 "Min": str(round(min(t), 2))

                 }

        elif mode == "RDEV":
            o = {"units": "EV",
                 "Max": str(round(max(t), 2)),
                 "Min": str(round(min(t), 2)),
                 # "Contrast": "1:"+str( int(math.pow( 10, math.log10(2) * max(t) )) ),
                 # "Max Density": str( round( (max(t)/3.322)   ,2) ),
                 # "Min Density": str( round( (min(t)/3.322)   ,2) )
                 }
        '''
        return o

    def mean(self, data):

        if len(data) > 1:

            mean = sum(data) / float(len(data))

        else:

            mean = [data]

        return mean

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
