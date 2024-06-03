import math
import cv2
import numpy
from PIL import Image, ImageStat,ImageFilter
from ImgTransformClass import ImgTransformClass
from getImageColors import getImageColors
from warning_class import AppWarningsClass


class GetFallOffClass():

    def __init__(self, pos, rgb_image):

        self.im = ImgTransformClass(rgb_image, None)
        self.ratio = self.im.get_ratio_transform()

        self.rgb_image = Image.open(rgb_image).convert('L')

        self.coor = self.scale_coordinates(pos)

        lab = getImageColors(pos, rgb_image, None )
        self.lab_values = lab.get_all_lab_values_dowscale()

    def slice_image(self):

        left = self.coor[0]
        top = self.coor[1]
        right = self.coor[2]
        bottom = self.coor[3]
        im1 = self.rgb_image.crop((left, top, right, bottom))
        #size = 10
        #im1= im1.filter(ImageFilter.RankFilter(size = 11, rank = (11 * 11)//2) )

        #self.np_im = numpy.array(im1)

        self.np_im = self.apllyLUT(numpy.array(im1))

        '''
        width = int(self.np_im.shape[1])
        height = int(self.np_im.shape[0])

        if width > 600 or height > 600:

            diagonal = math.sqrt(  height*height + height*height  )
            factor = diagonal / 600
            dim = (int(width/factor), int(height/factor))
            self.np_im = cv2.resize(self.np_im, dim, interpolation=cv2.INTER_AREA)

        #self.np_im  = cv2.applyColorMap(self.np_im , cv2.COLORMAP_JET)

            # im1.save('ROI.tiff', format='TIFF')
        '''

        return im1


    def apllyLUT(self,im):

        im = cv2.normalize(im, im, 0, 255, cv2.NORM_MINMAX)

        n = 20  # Number of levels of quantization
        indices = numpy.arange(0, 256)
        divider = numpy.linspace(0, 255, n + 1)[1]
        quantiz = numpy.int0(numpy.linspace(0, 255, n))
        color_levels = numpy.clip(numpy.int0(indices / divider), 0, n - 1)
        palette = quantiz[color_levels]
        im2 = palette[im]
        im2 = cv2.convertScaleAbs(im2)

        return cv2.applyColorMap(im2, cv2.COLORMAP_JET)

    def scale_coordinates(self, pos):

        npos = []
        for c in pos:
            value = int(c * self.ratio[7])
            npos.append(value)
        return npos

    def get_lab_stats(self):

        l = []
        c = []

        for lab in self.lab_values:
            l.append(lab[0])
            c.append( math.sqrt( (lab[1]*lab[1]) + (lab[2]*lab[2])) )

        o = {
            "l_mean": self.do_mean(l),
            "l_desv": self.stddev(l),
            "c_mean": self.do_mean(c),
            "c_desv": self.stddev(c),
            "nPixels": len(self.lab_values)
            }

        #print(o)
        return o

    def image_stats(self):

        im = self.slice_image()
        st = ImageStat.Stat(im)
        mean_v = st.mean
        desv = st.stddev  # Crea desviacion estandar
        pixeles = st.count  # apunta los pixeles promedidados
        if desv[0] == 0:
            desv[0] = 1
        snr = 20 * math.log10(mean_v[0] / desv[0])
        ex = st.extrema
        NonUniformity = ((ex[0][1] - ex[0][0]) / mean_v[0]) * 100

        lab = self.get_lab_stats()
        # guadar en un array valores lab, Des y Pixeles, Esto puede variar!
        return {"mean": mean_v[0],
                "desv": desv[0],
                "snr": snr,
                "max": ex[0][1],
                "min": ex[0][0],
                "NonUniformity": NonUniformity,
                "npixels": pixeles,
                "l_mean": lab["l_mean"],
                "l_desv": lab["l_desv"],
                "c_mean": lab["c_mean"],
                "c_desv": lab["c_desv"],
                "nPxLab": lab["nPixels"]
                }


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
