import cv2
import math
import numpy as np
from app_paths import DefinePathsClass
import configparser
from os import path

class GetAbCromatic:

    def __init__(self, pathToimage):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")

        if path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.w = int(self.config['ABERRATION_CHARTS']['COLUMN_DOTS'])
            self.h = int(self.config['ABERRATION_CHARTS']['ROW_DOTS'])
            self.radio = float(self.config['ABERRATION_CHARTS']['RADIO'])
            self.text =  float(self.config['ABERRATION_CHARTS']['TEXT_SIZE'])
            self.despTxt_x = float(self.config['ABERRATION_CHARTS']['DESP_TXT_X'])
            self.despTxt_y = float(self.config['ABERRATION_CHARTS']['DESP_TXT_Y'])
        else:
            self.w = 20  # columnas carta
            self.h = 15  # filas carta
            self.radio = 0.0123
            self.text = 0.0004
            self.despTxt_x = 0.02
            self.despTxt_y = 0.009

        self.image = cv2.imread(pathToimage)
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]


    def getAberration(self):



        self.radio = int(self.radio * float(self.width))
        self.text = self.text * float(self.width)
        self.despTxt_x = math.ceil(self.despTxt_x * float(self.width))
        self.despTxt_y = math.ceil(self.despTxt_y * float(self.width))

        blue, green, red = cv2.split(self.image)

        blueCorners, retB  = self.find_corners(blue)
        greenCorners, retG = self.find_corners(green)
        redCorners, retR = self.find_corners(red)

        if retB and retG and retR :
            deBG = self.deltasDots(blueCorners, greenCorners)
            deRG = self.deltasDots(redCorners, greenCorners)

            imgBG = self.drawCircles(deBG, [(0,0,255), (0,255,0) ])
            imgRG = self.drawCircles(deRG, [(255,0,0), (0,255,0) ])

            #self.imageBG = self.image_to_byte_array(imgBG)
            #self.imageRG = self.image_to_byte_array(imgRG)
            self.imageBG = imgBG
            self.imageRG = imgRG

            diagBG = self.getDiagonal(deBG,1)
            diagRG = self.getDiagonal(deRG,1)

            diagBGr = self.getDiagonal(deBG,2)
            diagRGr = self.getDiagonal(deRG,2)


            #cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/aberrationBG.png", imgBG)
            #cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/aberrationRG.png", imgRG)

            return {"caBG":diagBG,
                    "caRG":diagRG,
                    "caBGr":diagBGr,
                    "caRGr":diagRGr,
                    "stats":{"BG_Max": str(max(diagBG)), "RG_Max": str(max(diagRG)), "BGr_Max": str(max(diagBGr)), "RGr_Max": str(max(diagRGr)),    }
                    }
        else:

            return None

    def getDiagonal(self, deltas, poss):

        d1 = round(deltas[150][poss],2)
        d2 = round(deltas[169][poss],2)
        d3 = round((deltas[168][poss] + deltas[188][poss]) / 2,2)
        d4 = round(deltas[187][poss],2)
        d5 = round(deltas[206][poss],2)
        d6 = round((deltas[225][poss] + deltas[205][poss]) / 2,2)
        d7 = round(deltas[224][poss],2)
        d8 = round(deltas[243][poss],2)
        d9 = round(deltas[262][poss],2)
        d10 = round((deltas[261][poss] + deltas[281][poss]) / 2,2)
        d11 = round(deltas[280][poss],2)

        diagonal = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11]

        return diagonal


    def drawCircles(self, channels, color):

        imgblank = self.create_blank(self.width, self.height, rgb_color=(255, 255, 255))

        i = 0
        for x in channels:
            cv2.circle(imgblank, (int(x[3]), int(x[4])), self.radio, color[0], cv2.FILLED, 8, 0)
            cv2.circle(imgblank, (int(x[5]), int(x[6])), self.radio, color[1], cv2.FILLED, 8, 0)
            cv2.putText(imgblank, str(round(x[1],1)), (int(x[3] - self.despTxt_x), int(x[4] - self.despTxt_y)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.text, (30, 30, 30), 2)
            i = i + 1

        return imgblank


    def deltasDots(self, cha, chb):

        arr_cha = self.numpy2tuple(cha)
        arr_chb = self.numpy2tuple(chb)

        arr = []
        for i in range(len(cha)):

            diff = (arr_cha[i][0] - arr_chb[i][0])**2 + (arr_cha[i][1] - arr_chb[i][1])**2

            d = math.sqrt( diff )
            dr = math.sqrt( diff / ( self.width**2 + self.height**2  ) )

            arr.append( (i, d, dr, arr_cha[i][0], arr_cha[i][1], arr_chb[i][0], arr_chb[i][1] ) )

        return arr

    '''
    def drawCircles(self, channels, imgblank):

        color = [ (255,0,0), (0,255,0), (0,0,255) ]
        i = 0
        for x in channels:

            for y in x:
                cv2.circle(imgblank, (int(y[0]), int(y[1])), self.radio, color[i], cv2.FILLED, 8, 0)
            i = i + 1

        return imgblank
    '''


    def find_corners(self, img):

        sim = cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING
        # asim = cv2.CALIB_CB_ASYMMETRIC_GRID
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        params = cv2.SimpleBlobDetector_Params()
        params.maxArea = 10e4
        params.minArea = 10
        params.minDistBetweenBlobs = 5
        blobDetector = cv2.SimpleBlobDetector_create(params)
        ret, corners = cv2.findCirclesGrid(img, (self.w, self.h), sim, blobDetector, None)
        if ret:
            return corners, ret
        return (None,ret)

    def numpy2tuple(self, nump):

        s = []
        for x in nump:
            tup = tuple(map(tuple, x))[0]
            s.append(tup)
        return s

    def create_blank(self, width, height, rgb_color=(255, 255, 255)):

        image = np.zeros((height, width, 3), np.uint8)
        color = tuple(reversed(rgb_color))
        image[:] = color

        return image


#path = '/Volumes/SanDiskSSD/experimentos_tesis/distorsion/misCirculos3.png'
#x = GetAbCromatic()
#print( x.getAberration(path))