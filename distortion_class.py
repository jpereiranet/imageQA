import cv2
import math
import numpy as np
from app_paths import DefinePathsClass
import configparser
from os import path


class GetDistortion:

    def __init__(self):

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


    def getDistortion(self, path):

        self.corners2, ret, self.width, self.height = self.find_corners(path)

        if ret:

            self.imgBlank = self.create_blank(self.width, self.height, rgb_color=(255, 255, 255))

            x_pred, y_pred, center_x, center_y = self.get_predition(self.corners2)

            ref_points = self.draw_reference_grid(x_pred, y_pred, center_x, center_y)

            sample = self.numpy2tuple(self.corners2)
            deltas = self.euclidean_distance(ref_points, sample)

            # self.getDiagonal(deltas)
            s = self.getDiagonalPercent(deltas)

            avg = self.average(s)

            if avg > 0:
                kind = "Pincushion"
                maxV = max(s)
            if avg < 0:
                kind = "Barrel"
                maxV = min(s)

            return {"curve":s, "stats":{"MAX":maxV,"KIND": kind }}

        else:

            return None

        # img_sample = self.draw_circles(self.imgBlank, self.corners2, (255, 0, 0), True)
        # cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/misCirculos.png", img_sample)

    def average(self, lst):
        return sum(lst) / len(lst)

    def getDiagonal(self, deltas):

        d1 = deltas[150][1]
        d2 = deltas[169][1]
        d3 = (deltas[168][1] + deltas[188][1]) / 2
        d4 = deltas[187][1]
        d5 = deltas[206][1]
        d6 = (deltas[225][1] + deltas[205][1]) / 2
        d7 = deltas[224][1]
        d8 = deltas[243][1]
        d9 = deltas[262][1]
        d10 = (deltas[261][1] + deltas[281][1]) / 2
        d11 = deltas[280][1]

        diagonal = [d1, d2, d3, d4, d5, d6, d7, d8, d9, d10, d11]

        return diagonal

    def getDiagonalPercent(self, deltas):

        indexDiag = [150, 168, 206, 224, 262, 280]

        i = 0
        s = []
        for x in deltas:
            if x[0] in indexDiag:
                d0 = math.sqrt((deltas[150][2] - x[2]) ** 2 + (deltas[150][3] - x[3]) ** 2)
                d = math.sqrt((deltas[150][4] - x[4]) ** 2 + (deltas[150][5] - x[5]) ** 2)

                distorsion = round(((d - d0) / d0) * 100, 2)
                s.append(distorsion)

        return s

    # def getDiagonalDistance(self,deltas):

    #    print(deltas[280]) #esto detecta la esquina superior izda, es decir el 300

    #    d0 = math.floor( math.sqrt((deltas[150][2] - deltas[280][2])**2 + (deltas[150][3] - deltas[280][3])**2) )
    #    d = math.ceil( math.sqrt((deltas[150][4] - deltas[280][4]) ** 2 + (deltas[150][5] - deltas[280][5]) ** 2) )

    #   distorsion = round( ((d - d0)/d0) * 100, 2)

    #   print(d,d0,distorsion)

    def find_corners(self, img):

        sim = cv2.CALIB_CB_SYMMETRIC_GRID + cv2.CALIB_CB_CLUSTERING
        # asim = cv2.CALIB_CB_ASYMMETRIC_GRID
        # criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

        img = cv2.imread(img)
        height = img.shape[0]
        width = img.shape[1]
        self.radio = int(self.radio * float(width))
        self.text = self.text * float(width)
        self.despTxt_x = math.ceil(self.despTxt_x * float(width))
        self.despTxt_y = math.ceil(self.despTxt_y * float(width))
        # print(self.despTxt_x)
        # print(self.despTxt_y)

        self.gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        params = cv2.SimpleBlobDetector_Params()
        params.maxArea = 10e4
        params.minArea = 10
        params.minDistBetweenBlobs = 5
        blobDetector = cv2.SimpleBlobDetector_create(params)
        ret, corners = cv2.findCirclesGrid(self.gray, (self.w, self.h), sim, blobDetector, None)

        if ret:
            # cv2.cornerSubPix(gray, corners, (w, h), (-1, -1), criteria)
            # imgBlank = create_blank(width, height, rgb_color=(255, 255, 255))
            # drawn_frame = cv2.drawChessboardCorners(imgBlank, (w, h), corners, ret)
            # print(corners)
            # cv2.imshow("calib", drawn_frame)
            # cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/circles.png",drawn_frame )
            return corners, ret, width, height

        return (None,ret, None, None)

    def drawPoss(self, w, h, corners, ret, imgBlank):

        drawn_frame = cv2.drawChessboardCorners(imgBlank, (w, h), corners, ret)
        # cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/circles.png", drawn_frame)
        return drawn_frame

    def create_blank(self, width, height, rgb_color=(255, 255, 255)):

        image = np.zeros((height, width, 3), np.uint8)
        color = tuple(reversed(rgb_color))
        image[:] = color

        return image

    def draw_circles(self, imgBlank, corners, color, labeling):
        i = 0

        for c in corners:
            x, y = tuple(map(tuple, c))[0]
            # x = c[0]
            # y = c[1]
            if i == 150:
                cv2.circle(imgBlank, (int(x), int(y)), self.radio, (36, 255, 12), cv2.FILLED, 8, 0)
            else:
                if labeling:
                    cv2.putText(imgBlank, str(i), (int(x) - 60, int(y) - 30), cv2.FONT_HERSHEY_SIMPLEX, self.text,
                                (36, 255, 12), 2)
                cv2.circle(imgBlank, (int(x), int(y)), self.radio, color, cv2.FILLED, 8, 0)

            i = i + 1

        return imgBlank

    # def normalize_corners(corners):
    #    return cv2.normalize(corners, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

    def numpy2tuple(self, nump):

        s = []
        for x in nump:
            tup = tuple(map(tuple, x))[0]
            s.append(tup)
        return s

    def normalice_values(self, corners, width, height):
        s = []
        for c in corners:
            x = c[0] * width
            y = c[1] * height
            s.append((x, y))
        return s

    def get_predition(self, corners):

        arr = self.numpy2tuple(self.corners2)

        d_left = arr[150][0] - arr[151][0]
        d_right = arr[149][0] - arr[150][0]

        avrg_x = math.ceil((d_left + d_right) / 2)

        # print("avrg_x", avrg_x)

        d_top = arr[150][1] - arr[170][1]
        d_bottom = arr[130][1] - arr[150][1]

        avrg_y = math.floor((d_top + d_bottom) / 2)

        # print("avrg_y",avrg_y)

        return (avrg_x, avrg_y, arr[150][0], arr[150][1])

    def draw_reference_grid(self, x_pred, y_pred, center_x, center_y):

        mgBlank3 = self.create_blank(self.width, self.height, rgb_color=(255, 255, 255))

        points = []
        # cv2.circle(mgBlank3, (int(center_x), int(center_y)), 60, (20, 20, 20), cv2.FILLED, 8, 0)

        i = 150
        avance_x_left = center_x
        for x1 in range(10):

            avance_y_top = center_y
            avance_y_bt = center_y + y_pred

            j = i + 20
            for y1 in range(8):
                points.append((j, int(avance_x_left), int(avance_y_top)))

                cv2.putText(mgBlank3, str(j), (int(avance_x_left - 80), int(avance_y_top - 60)),
                            cv2.FONT_HERSHEY_SIMPLEX, self.text, (36, 255, 12), 2)
                cv2.circle(mgBlank3, (int(avance_x_left), int(avance_y_top)), self.radio, (255, 0, 255), cv2.FILLED, 8,
                           0)
                avance_y_top = avance_y_top - y_pred
                # print("avance_y_top", avance_y_top)

                j = j + 20

            h = i
            for y1 in range(7):
                points.append((h, int(avance_x_left), int(avance_y_bt)))
                cv2.putText(mgBlank3, str(h), (int(avance_x_left - 80), int(avance_y_bt - 60)),
                            cv2.FONT_HERSHEY_SIMPLEX, self.text, (36, 255, 12), 2)
                cv2.circle(mgBlank3, (int(avance_x_left), int(avance_y_bt)), self.radio, (0, 255, 0), cv2.FILLED, 8, 0)

                avance_y_bt = avance_y_bt + y_pred
                # print("avance_x_bt", avance_y_bt )

                h = h - 20

            avance_x_left = avance_x_left - x_pred
            i = i + 1

        l = 149
        avance_x_left = center_x + x_pred
        for x1 in range(10):
            avance_y_top = center_y
            avance_y_bt = center_y + y_pred

            m = l + 20
            for y1 in range(8):
                points.append((m, int(avance_x_left), int(avance_y_top)))
                cv2.putText(mgBlank3, str(m), (int(avance_x_left - 80), int(avance_y_top - 60)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            self.text, (36, 255, 12), 2)
                cv2.circle(mgBlank3, (int(avance_x_left), int(avance_y_top)), self.radio, (255, 0, 0), cv2.FILLED, 8, 0)

                avance_y_top = avance_y_top - y_pred
                # print("avance_y_top",avance_y_top)

                m = m + 20

            n = l
            for y1 in range(7):
                points.append((n, int(avance_x_left), int(avance_y_bt)))
                cv2.putText(mgBlank3, str(n), (int(avance_x_left - 80), int(avance_y_bt - 60)),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            self.text, (36, 255, 12), 2)
                cv2.circle(mgBlank3, (int(avance_x_left), int(avance_y_bt)), self.radio, (0, 0, 255), cv2.FILLED, 8, 0)

                avance_y_bt = avance_y_bt + y_pred
                # print("avance_y_top",avance_y_top)

                n = n - 20

            avance_x_left = avance_x_left + x_pred
            l = l - 1

        #cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/misCirculos33.png", mgBlank3)
        points.sort(key=lambda x: x[0], reverse=False)
        # print(points)

        return points

    '''
    def deduplicate_item(self, a):

        source_ips = []
        new_list = []
        for i in range(len(a)):
            if a[i][0] != None:
                if a[i][0] not in source_ips:
                    source_ips.append(a[i][0])
                    new_list.append(a[i])
        return new_list
    '''

    def euclidean_distance(self, arr_r, arr_s):

        mgBlank2 = self.create_blank(self.width, self.height, rgb_color=(255, 255, 255))
        # mgBlank2 = self.gray
        s = []
        i = 0
        for x in arr_r:

            e = math.sqrt((x[1] - arr_s[i][0]) ** 2 + (x[2] - arr_s[i][1]) ** 2)

            cv2.circle(mgBlank2, (int(x[1]), int(x[2])), self.radio, (255, 0, 255), cv2.FILLED, 8, 0)

            cv2.putText(mgBlank2, str(int(e)), (int(arr_s[i][0] - self.despTxt_x), int(arr_s[i][1] - self.despTxt_y)),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        self.text, (30,30,30), 2)
            s.append((x[0], math.floor(e), x[1], x[2], arr_s[i][0], arr_s[i][1]))
            # print(str(x[0])+" "+str(int(e))+" "+str(x[1])+" "+str(x[2])+" "+str(arr_s[i][0])+" "+str(arr_s[i][1]) )
            i = i + 1

        i = 0
        for x in arr_r:
            cv2.circle(mgBlank2, (int(arr_s[i][0]), int(arr_s[i][1])), self.radio, (0, 255, 0), cv2.FILLED, 8, 0)
            i = i + 1

        self.imgDistortion = mgBlank2
        #cv2.imwrite("/Volumes/SanDiskSSD/experimentos_tesis/distorsion/misCirculos3.png", mgBlank2)
        return s




#path = '/Volumes/SanDiskSSD/experimentos_tesis/distorsion/practica/DSC_4398_2B.TIF'
#x = GetDistortion()
#print( x.getDistortion(path) )



