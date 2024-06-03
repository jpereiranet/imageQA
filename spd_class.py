import math
import cv2
import numpy as np
from ImgTransformClass import ImgTransformClass
from warning_class import AppWarningsClass
#from scipy.signal import savgol_filter

class GetSPDClass():

    def __init__(self, filename, roi):

        self.im = ImgTransformClass(filename, None)
        ratio = self.im.get_ratio_transform()
        self.roi = self.scale_coordinates(roi,ratio)

        image_data = cv2.imread(filename,cv2.IMREAD_UNCHANGED)
        self.chns = len(image_data.shape)

        if image_data is None:
            return AppWarningsClass.critical_warn("Unsupported image format")

        self.roi_data = image_data[int(self.roi[1]):int(self.roi[3]), int(self.roi[0]):int(self.roi[2])]


    def scale_coordinates(self, pos,ratio):

        npos = []
        for c in pos:
            npos.append(c * ratio[7])
        return npos

    def reduceRoi(self, image_data, wh, offset):

        if (wh[0] < (offset * 2)) or (wh[1] < (offset * 2)):
            #print(wh)
            maxRoi = max(wh)
            offset = int(maxRoi/2)

    def getPSD(self,idx):

        y = []
        x = []

        if self.chns > 2:
            imgR = self.roi_data[:, :, 2]
            imgG = self.roi_data[:, :, 1]
            imgB = self.roi_data[:, :, 0]

            rn = self.getSpectrum(imgR,idx)
            gn = self.getSpectrum(imgG,idx)
            bn = self.getSpectrum(imgB,idx)
            y.append([rn[0].tolist(), gn[0].tolist(), bn[0].tolist() ])

            x = [round(x, 2) for x in rn[1].tolist()]
        else:
            img = self.roi_data[:, :]
            Y = self.getSpectrum(img,idx)
            y.append( Y[0].tolist() )
            x = [round(x, 2) for x in Y[1].tolist()]

        #y = savgol_filter(y,25, 3, mode='nearest')

        x_str = []
        for val in x:
            x_str.append(str(val))


        return {"curve": y, "stats": "", "x_axis": x_str}


    def getSpectrum(self,img,idx):
        #https://stackoverflow.com/questions/54410356/plot-the-psd-of-an-image-vs-x-y-axis
        if idx == 0:
            shp = 1
        elif idx == 1:
            shp = 0

        n = int(math.ceil(img.shape[idx] / 2.) * 2)

        a = np.fft.rfft(img, n, axis=idx)
        a = a.real * a.real + a.imag * a.imag
        a = a.sum(axis=shp) / a.shape[shp]
        #a = np.log(a)
        max = np.amax(a[1:])
        if max == 0:
            max = 1
        #d = np.full((len(a),), max)
        #a = np.divide(a, d)
        f = np.fft.rfftfreq(n)

        return[a[1:], f[1:]]


    def histogram(self):

        if self.chns > 2:

            colors = ("r", "g", "b")
            channel_ids = (0, 1, 2)

            y = []
            bin_edges = []

            for channel_id, c in zip(channel_ids, colors):
                histogram, bin_edges = np.histogram(
                    self.roi_data[:, :, channel_id], bins=256, range=(0, 256)
                )

                y.append( histogram.tolist() )

            x = bin_edges[0:-1].tolist()
            x = [int(xf) for xf in x]

        else:

            histogram, bin_edges = np.histogram(self.roi_data.ravel(), 256, [0, 256])
            y = [ histogram.tolist()]
            x = bin_edges[0:-1].tolist()
            x = [int(xf) for xf in x]

        x_str = []
        for val in x:
            x_str.append(str(val))



        return {"curve": y, "stats": "", "x_axis": x_str}


