
#The algorithm to solve the SFR/MTF is taken from the source code of Bhavin Nayak (2015)
#https://github.com/bvnayak/PDS_Compute_MTF

import math
import cv2
import numpy as np
from scipy import interpolate
from scipy.signal import savgol_filter
from warning_class import AppWarningsClass


class GetMTFClass:

    def __init__(self, filename):

        #self.im = ImgTransformClass(filename, None)
        #self.ratio = self.im.get_ratio_transform()

        #self.filename = filename
        #self.roi = self.scale_coordinates(roi)

        #image_data = cv2.imread(self.filename, cv2.IMREAD_GRAYSCALE)

        #if image_data is None:
        #    return AppWarningsClass.critical_warn("Unsupported image format")

        #self.compute_roi()

        #ancho = self.roi[2] - self.roi[0]
        #alto = self.roi[3] - self.roi[1]
        #print("---coordenadas----")
        #print(ancho)
        #print(alto)
        #print("-------")

        self.data = filename
        #self.data = image_data[int(self.roi[1]):int(self.roi[3]), int(self.roi[0]):int(self.roi[2])]

        # se pone el umbral a 100 porque si se pone a 0 no funciona con imagens que no tengan el fonfo blanco
        _, th = cv2.threshold(self.data, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        kernel = np.ones((5, 5), np.uint8)
        th = cv2.erode(th, kernel, iterations=1)
        #cv2.imwrite("thres.png", th)

        self.min = np.amin(self.data)
        self.max = np.amax(self.data)
        self.threshold = th * (self.max - self.min) + self.min
        #cv2.imwrite("threshold_contrast.png", self.threshold)

        below_thresh = ((self.data >= self.min) & (self.data <= self.threshold))
        above_thresh = ((self.data >= self.threshold) & (self.data <= self.max))
        area_below_thresh = self.data[below_thresh].sum() / below_thresh.sum()
        area_above_thresh = self.data[above_thresh].sum() / above_thresh.sum()
        self.threshold = (area_below_thresh - area_above_thresh) / 2 + area_above_thresh
        #cv2.imwrite("threshold_contrast_2.png", self.threshold)
        # esta es la imagen con los bordes
        self.edges = cv2.Canny(th, self.min, self.max - 5, 3, L2gradient=True)

        #cv2.imwrite("edge.png", self.edges)

        row_edge, col_edge = np.where(self.edges == 255)

        #print("row_edge")
        #print(row_edge)
        #print("col_edge")
        #print(col_edge)

        if len(col_edge) > 0 and len(row_edge) > 0:

            z = np.polyfit(np.flipud(col_edge), row_edge, 1)
            angle_radians = np.arctan(z[0])
            angle_deg = angle_radians * (180 / 3.14)
            real_angle = round( 90 - abs(angle_deg),0)
            #print("angle_deg")
            #print(real_angle)


            #if abs(angle_deg) < 45:
            #    self.data = np.transpose(self.data)

            #inicio = np.mean(self.data[:,0])
            #if inicio < 120:
            #    self.data = np.rot90(self.data,2)
            #fin = np.mean(self.data[:,-1])

            #cv2.imwrite("position.png", self.data)

            #self.compute_esf()
            #self.compute_lsf()
            #self.compute_mtf()


    def compute_esf(self):

        kernel = np.ones((3, 3), np.float32) / 9
        smooth_img = cv2.filter2D(self.data, -1, kernel)

        #cv2.imwrite("smoot.png", smooth_img)

        #k_gauss = np.transpose(cv2.getGaussianKernel(7, 1.0))
        #temp = cv2.filter2D(self.data, -1, k_gauss, borderType=cv2.BORDER_REFLECT)

        #cv2.imwrite("smoot2.png", temp)

        row = self.data.shape[0]
        column = self.data.shape[1]
        array_values_near_edge = np.empty([row, 13])
        array_positions = np.empty([row, 13])
        edge_pos = np.empty(row)
        smooth_img = smooth_img.astype(float)
        #abs_diff_max_arr = []
        for i in range(0, row):
            # print(smooth_img[i,:])
            diff_img = smooth_img[i, 1:] - smooth_img[i, 0:(column - 1)]

            abs_diff_img = np.absolute(diff_img)
            abs_diff_max = np.amax(abs_diff_img)
            #abs_diff_max_arr.append(abs_diff_max)

            #print("abs_diff_max")
            #print(abs_diff_max)

            if abs_diff_max == 1:
                return AppWarningsClass.critical_warn("No edge was detect! Move the ROI over a edge")
                # raise IOError('No Edge Found')

            app_edge = np.where(abs_diff_img == abs_diff_max)

            bound_edge_left = app_edge[0][0] - 2
            bound_edge_right = app_edge[0][0] + 3

            strip_cropped = self.data[i, bound_edge_left:bound_edge_right]
            temp_y = np.arange(1, 6)

            # si queremos pillar un canal particular usamos strip_cropped[:,0]
            # f = interpolate.interp1d(strip_cropped[:,0], temp_y, kind='linear')
            if len(strip_cropped) == 0:
                return AppWarningsClass.critical_warn("No edge was detect! Move the ROI over a edge")

            #print(strip_cropped)
            #print(np.amin(strip_cropped))
            #print(self.threshold)
            #print(math.isnan(float(self.threshold)))

            if np.amin(strip_cropped) > self.threshold:
                self.threshold = np.amin(strip_cropped) + 1
                #print(self.threshold)

            if np.amin(strip_cropped) > self.threshold or math.isnan(float(self.threshold)):
                return AppWarningsClass.critical_warn("No edge was detect! Move the ROI over a edge")

            # la desv std controla que se haya detectado el borde en la imagen, normalmente suele esar por encima de 70
            #print(strip_cropped)
            #print(np.std(strip_cropped))
            #print(abs_diff_max)
            if abs_diff_max < 20:
                return AppWarningsClass.critical_warn(
                   "No edge was detect! Perhaps ROI has insuficient contrast")

            #print(strip_cropped)
            f = interpolate.interp1d(strip_cropped, temp_y, kind='nearest')

            edge_pos_temp = f(self.threshold)

            edge_pos[i] = edge_pos_temp + bound_edge_left - 1
            bound_edge_left_expand = app_edge[0][0] - 6
            bound_edge_right_expand = app_edge[0][0] + 7

            temp_v = self.data[i, bound_edge_left_expand:bound_edge_right_expand]
            # para usar con varios canles
            # array_values_near_edge[i, :] = temp_v[:,0]

            if len(temp_v) == 0:
                return AppWarningsClass.critical_warn("No edge was detect! Move the ROI over a edge")

            #print("temp_v",len(temp_v))
            #print("array_values_near_edge",len(array_values_near_edge))

            array_values_near_edge[i, :] = temp_v
            array_positions[i, :] = np.arange(bound_edge_left_expand, bound_edge_right_expand)

        y = np.arange(0, row)
        nans, x = self.nan_helper(edge_pos)

        edge_pos[nans] = np.interp(x(nans), x(~nans), edge_pos[~nans])

        array_positions_by_edge = array_positions - np.transpose(edge_pos * np.ones((13, 1)))

        num_row = array_positions_by_edge.shape[0]
        num_col = array_positions_by_edge.shape[1]
        array_values_by_edge = np.reshape(array_values_near_edge, num_row * num_col, order='F')
        array_positions_by_edge = np.reshape(array_positions_by_edge, num_row * num_col, order='F')

        #mean_abs_diff_max_arr = sum(abs_diff_max_arr) / len(abs_diff_max_arr)
        #print(mean_abs_diff_max_arr)
        #print(min(abs_diff_max_arr))
        #print(max(abs_diff_max_arr))
        #if max(abs_diff_max_arr) > 63:
        #    pixel_subdiv = 0.10
        #else:
        #    pixel_subdiv = 0.09

        #bin_pad = 0.0001
        #pixel_subdiv = 0.10
        bin_pad = 0.0001
        pixel_subdiv = 0.09
        topedge = np.amax(array_positions_by_edge) + bin_pad + pixel_subdiv
        botedge = np.amin(array_positions_by_edge) - bin_pad
        binedges = np.arange(botedge, topedge + 1, pixel_subdiv)
        numbins = np.shape(binedges)[0] - 1

        binpositions = binedges[0:numbins] + (0.5) * pixel_subdiv
        h, whichbin = np.histogram(array_positions_by_edge, binedges)
        whichbin = np.digitize(array_positions_by_edge, binedges)
        binmean = np.empty(numbins)

        # print(binmean)

        for i in range(0, numbins):
            flagbinmembers = (whichbin == i)

            binmembers = array_values_by_edge[flagbinmembers]
            # cuando binmembers tiene longitud 0 np.mean arroja el error de "RuntimeWarning: invalid value encountered in double_scalars"
            binmean[i] = np.mean(binmembers)

        nans, x = self.nan_helper(binmean)
        binmean[nans] = np.interp(x(nans), x(~nans), binmean[~nans])
        esf = binmean
        xesf = binpositions
        xesf = xesf - np.amin(xesf)
        self.xesf = xesf

        esf_smooth = savgol_filter(esf, 25, 3)
        #self.esf = esf
        #self.esf_smooth = esf_smooth

        #return [xesf, esf, esf_smooth]

        return {"xesf":xesf, "esf":esf, "esf_smooth":esf_smooth}

    def compute_lsf(self, xesf, esf, esf_smooth ):

        diff_esf = abs(esf[1:] - esf[0:(esf.shape[0] - 1)])
        diff_esf = np.append(0, diff_esf)
        lsf = diff_esf
        diff_esf_smooth = abs(esf_smooth[0:(esf.shape[0] - 1)] - esf_smooth[1:])
        diff_esf_smooth = np.append(0, diff_esf_smooth)
        lsf_smooth = diff_esf_smooth
        #self.lsf = lsf
        #self.lsf_smooth = lsf_smooth

        return {"xesf":xesf, "lsf":lsf, "lsf_smooth":lsf_smooth}

    def compute_mtf(self,lsf,lsf_smooth):

        mtf = np.absolute(np.fft.fft(lsf, 2048))
        mtf_smooth = np.absolute(np.fft.fft(lsf_smooth, 2048))
        mtf_final = np.fft.fftshift(mtf)
        mtf_final_smooth = np.fft.fftshift(mtf_smooth)

        # plt.subplot(2, 2, 4)
        x_mtf_final = np.arange(0, 1, 1. / 127)

        mtf_final = mtf_final[1024:1151] / np.amax(mtf_final[1024:1151])
        mtf_final_smooth = mtf_final_smooth[1024:1151] / np.amax(mtf_final_smooth[1024:1151])

        #print("x_mtf_final  mtf_final   mtf_final_smooth")
        #for x in range(len(x_mtf_final)):
        #    print(str(x_mtf_final[x])+" "+str(mtf_final[x])+"   "+str(mtf_final_smooth[x]))

        return { "x_mtf_final":x_mtf_final,
                 "mtf_final": mtf_final,
                 "mtf_final_smooth": mtf_final_smooth
                 }


    def showImage(self, image):
        cv2.imshow('Image', image)
        cv2.waitKey(0)

    def nan_helper(self, y):
        """Helper to handle indices and logical indices of NaNs.

        Input:
            - y, 1d numpy array with possible NaNs
        Output:
            - nans, logical indices of NaNs
            - index, a function, with signature indices= index(logical_indices),
              to convert logical indices of NaNs to 'equivalent' indices
        Example:
            >>> # linear interpolation of NaNs
            >>> nans, x= nan_helper(y)
            >>> y[nans]= np.interp(x(nans), x(~nans), y[~nans])
        """

        return np.isnan(y), lambda z: z.nonzero()[0]
