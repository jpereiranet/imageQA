
import cv2
import numpy as np
from numpy import trapz
from mtf_class import GetMTFClass
from warning_class import AppWarningsClass
from ImgTransformClass import ImgTransformClass
from PIL import Image
from plist_set import ProcessSettingsClass

from scipy.integrate import simps

class GetMTFClassRGB:

    def __init__(self, filename, roi):

        self.im = ImgTransformClass(filename, None)
        ratio = self.im.get_ratio_transform()

        self.filename = filename

        self.roi = self.scale_coordinates(roi,ratio)

        image_data = cv2.imread(filename)

        if image_data is None:
            return AppWarningsClass.critical_warn("Unsupported image format")

        roi_data = image_data[int(self.roi[1]):int(self.roi[3]), int(self.roi[0]):int(self.roi[2])]

        w_roi = self.roi[2] - self.roi[0]
        h_roi = self.roi[3] - self.roi[1]

        self.roi_data = self.reduceRoi(roi_data, [w_roi,h_roi], offset=25)


    def rotateImage(self, th, image_data, wh):

        ancho = int(wh[0])
        alto = int(wh[1])

        a = th[0][0 ]
        b = th[0][ancho-1]
        c = th[ alto-1][ ancho-1 ]
        d = th[alto - 1][0]

        #print("esquinas",[a,b,c,d])

        if (a == 255 and b  == 255) :
            #th = np.transpose(th)
            th= np.rot90(th,3)
            image_data = np.rot90(image_data,3)

        if (c == 255 and d == 255):
            th= np.rot90(th)
            image_data = np.rot90(image_data)

        if (a == 255 and d == 255):
            th = np.rot90(th,2)
            image_data = np.rot90(image_data,2)

        #cv2.imwrite("rotacion.png", th)

        #self.data = np.rot90(self.data, 2)

        return th,image_data


    def reduceRoi(self, image_data, wh, offset):


        if (wh[0] < (offset * 2)) or (wh[1] < (offset * 2)):
            #print(wh)
            maxRoi = max(wh)
            offset = int(maxRoi/2)


        gray = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)

        _, th = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        th = cv2.erode(th, kernel, iterations=1)

        th,image_data = self.rotateImage(th,image_data, wh)

        #cv2.imwrite("tres.png", th)

        minI = np.amin(th)
        maxI = np.amax(th)

        edges = cv2.Canny(th, minI, maxI - 5, 3, L2gradient=True)

        #cv2.imwrite("edge.png", edges)

        coor = np.column_stack(np.where(edges == 255))

        arr_coor = np.ndarray.tolist(coor)

        minc = arr_coor[0]
        maxc = arr_coor[-1]

        yCentro = maxc[0] / 2

        xCentro = None
        for x in arr_coor:
            if x[0] == int(yCentro):
                xCentro = x[1]

        if xCentro == None:
            return AppWarningsClass.critical_warn("ROI Wrong, please select another area")

        #print("ycentro", yCentro)
        #print("xcentro", xCentro)

        if offset > xCentro:
            offset = xCentro
        if offset > yCentro:
            offset = yCentro

        #print(offset)

        xt = int(xCentro - offset)
        yt = int(yCentro - offset)

        xb = int(xCentro + offset)
        yb = int(yCentro + offset)

        #print([xt, yt])
        #print([xb, yb])

        roi_data = image_data[yt:yb, xt:xb]

        #cv2.imwrite("roidata.png", roi_data)

        return roi_data


    def get_mtf_multiple(self):

        #roi_data = self.image_data[int(self.roi[1]):int(self.roi[3]), int(self.roi[0]):int(self.roi[2])]

        #roi_data = self.reduceRoi(self.roi_data)

        return self.getGRAYMTF(self.roi_data)



    def get_mtf_esf_lsf(self):

        if self.isgray(self.roi_data):

            return self.getGRAYMTF(self.roi_data)

        else:

            b = self.roi_data[:, :, 0]
            g = self.roi_data[:, :, 1]
            r = self.roi_data[:, :, 2]
            gray = cv2.cvtColor(self.roi_data, cv2.COLOR_BGR2GRAY)
            #channels = [r,g,b,gray]
            channels = {"RED":r, "GREEN": g, "BLUE":b, "GRAY":gray}

            return  self.getRGBMTF(channels)

    def rise(self,ch):

        x = ch["xesf"].tolist()
        y = ch["esf"].tolist()

        ymin = min(y)
        yofset = [i-ymin for i in y]

        yofsetmax = max(yofset)

        y10 = (yofsetmax * 10) / 100
        y90 = (yofsetmax * 90) / 100

        for i in range(len(yofset)):
            if y10 > yofset[i]:
                i10 = i
            elif y90 > yofset[i]:
                i90 = i

        xlow = x[i10]
        xtop = x[i90]

        risevalue = xtop - xlow

        return risevalue





    def missregistration(self,r,g,b):

        ch_red = r["esf"]
        ch_green = g["esf"]
        ch_blue = b["esf"]

        #print("rojo", np.prod(ch_red.shape) )
        #print("verde", np.prod(ch_green.shape) )
        #print("azul",  np.prod(ch_blue.shape) )

        ch_red, ch_green, ch_blue, xindex = self.normaliceDimensions( ch_red, ch_green, ch_blue)

        channels = [ch_red,ch_green,ch_blue]
        xindexes = [r["xesf"],g["xesf"],b["xesf"]]
        x = xindexes[xindex]

        curve_levels = [np.sum(ch_red), np.sum(ch_green), np.sum(ch_blue) ]

        curvemax = curve_levels.index(min(curve_levels))
        curvemin = curve_levels.index(max(curve_levels))

        #print("curva maxima",curvemax )
        #print("curva curvemin", curvemin)
        #print("puntos",len(ch_red))

        difcurve = np.subtract(channels[curvemax], channels[curvemin])

        # calcula la area de la curva
        area = trapz(difcurve, x)
        ca = round(abs(area/len(x)), 1)
        #print("CA =", ca )

        return ca

    def normaliceDimensions(self, ch_red,ch_green,ch_blue):

        numpies = [ ch_red,ch_green,ch_blue]
        dimensions = [ np.prod(ch_red.shape), np.prod(ch_green.shape), np.prod(ch_blue.shape) ]

        maxdimension = max(dimensions)
        mindimension = min(dimensions)
        maxdIndex = dimensions.index(max(dimensions))
        minvalue = min(numpies[maxdIndex])
        maxvalue = max(numpies[maxdIndex])
        #print("max dim",maxdimension)
        #print("min dim", mindimension)

        if maxdimension is not mindimension:

            rd = np.prod(ch_red.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(maxvalue)
                ch_red = np.append(ch_red,npvalues  )

            rd = np.prod(ch_green.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(maxvalue)
                ch_green = np.append(ch_green,npvalues )

            rd = np.prod(ch_blue.shape)
            total = maxdimension - rd
            if total > 0:
                npvalues = np.zeros(total)
                npvalues.fill(maxvalue)
                ch_blue = np.append(ch_blue,npvalues  )

        return [ch_red, ch_green, ch_blue, maxdIndex ]


    def isgray(self, img):

        if type(img) is np.ndarray:
            if len(img.shape) < 3: return True
            if img.shape[2]  == 1: return True
            b,g,r = img[:,:,0], img[:,:,1], img[:,:,2]
            if (b==g).all() and (b==r).all(): return True
            return False
        else:
            return AppWarningsClass.critical_warn("Img Err")

    def getRGBMTF(self,channels):
        print("-----")

        mtf_per_channel = {}
        lsf_per_channel = {}
        esf_per_channel = {}

        for key, value in channels.items():
            #print("......")
            #print("channel",key)

            get_mtf = GetMTFClass(value)
            esf = get_mtf.compute_esf()
            if type(esf) is dict:
                lsf = get_mtf.compute_lsf(esf["xesf"], esf["esf"], esf["esf_smooth"])
                mtf = get_mtf.compute_mtf( lsf["lsf"], lsf["lsf_smooth"])
            else:
                return AppWarningsClass.critical_warn("Cannot compute MTF, please choose another area")


            mtf_per_channel[key] = mtf


            metrics = { "MTF50":0.5, "MTF30":0.3, "MTF10":0.1 }


            for metric,value in metrics.items():
                mtf_per_channel[key][metric] = {}
                MTF = self.MTFatLimit(mtf["mtf_final"], mtf["x_mtf_final"], value)
                derived_metrics = self.otherMetrics(MTF)


                if MTF < 0.5:
                    #print("GETLimits", MTF)
                    #print("metrica",value)
                    mtf_per_channel[key][metric]["MTF"] = MTF
                    mtf_per_channel[key][metric]["MTFpercent"] =  derived_metrics["MTFpercent"]
                    mtf_per_channel[key][metric]["LPmm"] = derived_metrics["LPmm"]
                    mtf_per_channel[key][metric]["LW_PH"] = derived_metrics["LW_PH"]
                    mtf_per_channel[key][metric]["LPH"] = derived_metrics["LPH"]
                    mtf_per_channel[key][metric]["lpPercent"] = derived_metrics["lpPercent"]
                    mtf_per_channel[key][metric]["imgLPmm"] = derived_metrics["imgLPmm"]
                    mtf_per_channel[key][metric]["lpNyquist"] = derived_metrics["lpNyquist"]

                else:
                    mtf_per_channel[key][metric]["MTF"] = None
                    mtf_per_channel[key][metric]["MTFpercent"] =  None
                    mtf_per_channel[key][metric]["LPmm"] = None
                    mtf_per_channel[key][metric]["LW_PH"] = None
                    mtf_per_channel[key][metric]["LPH"] = None
                    mtf_per_channel[key][metric]["lpPercent"] = None
                    mtf_per_channel[key][metric]["imgLPmm"] = None
                    mtf_per_channel[key][metric]["lpNyquist"] = None

            lsf_per_channel[key] = lsf
            esf_per_channel[key] = esf

        ca = self.missregistration(esf_per_channel["RED"], esf_per_channel["GREEN"], esf_per_channel["BLUE"] )

        raise_red = round(self.rise( esf_per_channel["RED"] ),1)
        raise_green = round(self.rise(esf_per_channel["GREEN"]),1)
        raise_blue = round(self.rise(esf_per_channel["BLUE"]),1)

        esf_per_channel["INFO"] = {"CA": ca, "RAISE_RED": raise_red, "RAISE_GREEN": raise_green, "RAISE_BLUE": raise_blue,"RAISE_GRAY": None}
        #mtf_per_channel["GRAY"]["mtf_final"] = self.meanCurves(mtf_per_channel, "mtf_final")
        #mtf_per_channel["GRAY"]["esf"] = self.meanCurves(esf_per_channel, "esf")


        o = {
                "mode": "RGB",
                "channel_mtf": mtf_per_channel,
                "channel_lsf": lsf_per_channel,
                "channel_esf": esf_per_channel
            }


        return o



    def MTFatLimit(self, mtf, xmtf, limit):

        redondear = lambda x: round(x, 1)
        y_rounded = list(map(redondear, mtf))
        pos01 = [i for i, x in enumerate(y_rounded) if x == limit]
        mtfs10 = [np.ndarray.tolist(xmtf)[i] for i in pos01]
        if (len(mtfs10) > 0):
            mtf10 = sum(mtfs10) / len(mtfs10)
        else:
            mtf10 = 0  # revisar esto!!!
        return round(mtf10, 2)


    def otherMetrics(self,MTF):

        MTFpercent = None
        params = ProcessSettingsClass()
        heightSensor = params.setting_restore("camera/heightSensor")
        widthSensor = params.setting_restore("camera/imgWidth")
        imgHeight = params.setting_restore("camera/imgHeight")
        pitch = params.setting_restore("camera/pitch")
        resolution = params.setting_restore("camera/resolution")

        MTFpercent = round((MTF * 100) / 0.5, 1)

        if resolution:

            lpNyquist = round( ( float(resolution) / 2) / 24.4, 2)  #esto define e limite de Nyquist en Lp/mm
            linesMM = lpNyquist * 2  #eso da la relacion de Lineas/mm en la imagen
            imgLPmm = round(linesMM * MTF, 2)  #esto da las Lp/mm a un %MTF dado, convierte de c/p a la Lp/mm para el tamaño de imagen
            lpPercent = round((imgLPmm * 100) / lpNyquist, 1) # % respecto a Nyquist

        else:
            lpNyquist = None
            linesMM = None
            imgLPmm = None
            lpPercent = None

        if pitch and imgLPmm:

            LPmm = round((MTF / float(pitch)) * 1000, 2)
            LPmax = round ( 1000 / (2 * float(pitch) ), 2  )
            LW_PH = round(MTF * 2 * float(imgHeight), 0)
            LPH = round(imgLPmm * float(heightSensor), 0)
            #print("pitch", float(pitch))
            #print("MTF", MTF)
            #print("lp/mm",imgLPmm)
            #print("heightSensor", heightSensor)
            #print("imgHeight", imgHeight)
            #LPmmPercent = round( (LPmm * 100) / LPmax ,1 )
        else:
            LPmm = None
            LPmax = None
            LW_PH = None
            LPH = None

        o = {"LPmm": LPmm,
             "LW_PH": LW_PH,
             "LPH": LPH,
             "LPmax": LPmax,
             "MTFpercent":MTFpercent,
             "lpNyquist":lpNyquist,
             "imgLPmm": imgLPmm,
              "lpPercent": lpPercent
             }
        return o



    def meanCurves(self, values, c):

        ch_red = values["RED"][c]
        ch_green = values["GREEN"][c]
        ch_blue =  values["BLUE"][c]
        ch_red,ch_green,ch_blue,_ =  self.normaliceDimensions( ch_red,ch_green,ch_blue)

        o = []
        for x in range(len(ch_red)):
            o.append( 0.25 * ch_red[x] + 0.5 * ch_green[x] + 0.25 * ch_blue[x] )

        return o


    def scale_coordinates(self, pos,ratio):

        npos = []
        for c in pos:
            npos.append(c * ratio[7])
        return npos


    def getGRAYMTF(self, image_data):

        image_data = cv2.cvtColor(image_data, cv2.COLOR_BGR2GRAY)
        get_mtf = GetMTFClass(image_data)
        esf = get_mtf.compute_esf()
        if type(esf) is dict:
            lsf = get_mtf.compute_lsf(esf["xesf"], esf["esf"], esf["esf_smooth"])
            mtf = get_mtf.compute_mtf(lsf["lsf"], lsf["lsf_smooth"])
        else:
            return AppWarningsClass.critical_warn("Cannot compute MTF, please choose another area")

        mtf_channel = {}

        mtf_channel["GRAY"] = mtf

        metrics = {"MTF50": 0.5, "MTF30": 0.3, "MTF10": 0.1}

        for metric, value in metrics.items():
            mtf_channel["GRAY"][metric] = {}
            MTF = self.MTFatLimit(mtf["mtf_final"], mtf["x_mtf_final"], value)
            derived_metrics = self.otherMetrics(MTF)

            if MTF < 0.5:
                mtf_channel["GRAY"][metric]["MTF"] = MTF
                mtf_channel["GRAY"][metric]["MTFpercent"] = derived_metrics["MTFpercent"]
                mtf_channel["GRAY"][metric]["LPmm"] = derived_metrics["LPmm"]
                mtf_channel["GRAY"][metric]["LW_PH"] = derived_metrics["LW_PH"]
                mtf_channel["GRAY"][metric]["LPH"] = derived_metrics["LPH"]
                mtf_channel["GRAY"][metric]["lpPercent"] = derived_metrics["lpPercent"]
                mtf_channel["GRAY"][metric]["imgLPmm"] = derived_metrics["imgLPmm"]
                mtf_channel["GRAY"][metric]["lpNyquist"] = derived_metrics["lpNyquist"]
            else:
                mtf_channel["GRAY"][metric]["MTF"] = None
                mtf_channel["GRAY"][metric]["MTFpercent"] = None
                mtf_channel["GRAY"][metric]["LPmm"] = None
                mtf_channel["GRAY"][metric]["LW_PH"] = None
                mtf_channel["GRAY"][metric]["LPH"] = None
                mtf_channel["GRAY"][metric]["lpPercent"] = None
                mtf_channel["GRAY"][metric]["imgLPmm"] = None
                mtf_channel["GRAY"][metric]["lpNyquist"] = None

        raise_gray = round( self.rise( esf ) ,1)


        #esf["INFO"] = {"RAISE_GRAY": raise_gray}


        return {
            "mode": "GRAY",
            "channel_mtf": mtf_channel,
            "channel_lsf": {"GRAY":lsf},
            "channel_esf": {"GRAY":esf,"INFO": {"RAISE_GRAY": raise_gray,"CA": None, "RAISE_RED": None, "RAISE_GREEN": None, "RAISE_BLUE": None} }

        }

    def compute_roi(self):

        # crea una imagen con el ROI definido para dejar constancia donde se hace la seleccion

        in_image = Image.open(self.filename)
        rgbimg = Image.new("RGBA", in_image.size)
        rgbimg.paste(in_image)

        ancho = int(self.roi[2] - self.roi[0])
        alto = int(self.roi[3] - self.roi[1])
        x = int(self.roi[0])
        y = int(self.roi[1])

        image = Image.new('RGBA', (ancho, alto), (0, 255, 0))
        rgbimg.paste(image, (x, y))

        return rgbimg


#GetMTFClassRGB(filename="/Volumes/Macintosh_HD_DATA/imageIQ/mtf_luz_continua_apertura/DSC_4107.TIF", roi=None)