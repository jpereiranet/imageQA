import cv2
import numpy as np
import math
import os
import ntpath
from warning_class import AppWarningsClass

#from sewar.full_ref import uqi, msssim, vifp
#from sewar.full_ref import psnr

'''

Esta clase no funciona no esta registrando las images de diferente tamaño

'''


class ImgDiffClass():


    def __init__(self, multipleFiles):

        image_a = cv2.imread(multipleFiles[0])
        image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        image_b = cv2.imread(multipleFiles[1])
        image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

        self.im2Sample, self.im2Reference = self.OrbsRegister(image_a, image_b)

        self.imgSampleSize = [image_a.shape[0],image_a.shape[1],round(os.path.getsize(multipleFiles[1])/1024,1), ntpath.basename(multipleFiles[1]) ]
        self.imgReferenceSize = [image_b.shape[0],image_b.shape[1],round(os.path.getsize(multipleFiles[0])/1024,1), ntpath.basename(multipleFiles[0]) ]



    def checkSize(self, img1, img2):
        '''
        Sort images by size. Reference image always fit was smaller
        '''
        height1, width1 = img1.shape
        height2, width2 = img2.shape

        one = height1 * width1
        two = height2 * width2

        if one > two:
            return img1, img2
        else:
            return img2, img1


    def OrbsRegister(self, img1_color, img2_color):

        features = 5000
        maxmatches = 0.9

        img1, img2 = self.checkSize(img1_color, img2_color)
        height, width = img2.shape

        orb_detector = cv2.ORB_create(features)

        kp1, d1 = orb_detector.detectAndCompute(img1, None)
        kp2, d2 = orb_detector.detectAndCompute(img2, None)

        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

        matches = matcher.match(d1, d2)

        matches = sorted(matches, key=lambda x: x.distance)

        matches = matches[:int(len(matches) * maxmatches)]
        no_of_matches = len(matches)

        p1 = np.zeros((no_of_matches, 2))
        p2 = np.zeros((no_of_matches, 2))

        for i in range(len(matches)):
            p1[i, :] = kp1[matches[i].queryIdx].pt
            p2[i, :] = kp2[matches[i].trainIdx].pt

        homography, mask = cv2.findHomography(p1, p2, cv2.RANSAC)

        transformed_img = cv2.warpPerspective(img1_color, homography, (width, height))

        return transformed_img, img2_color

    def ssim(self,img1, img2):
        C1 = (0.01 * 255) ** 2
        C2 = (0.03 * 255) ** 2

        img1 = img1.astype(np.float64)
        img2 = img2.astype(np.float64)
        kernel = cv2.getGaussianKernel(11, 1.5)
        window = np.outer(kernel, kernel.transpose())

        mu1 = cv2.filter2D(img1, -1, window)[5:-5, 5:-5]  # valid
        mu2 = cv2.filter2D(img2, -1, window)[5:-5, 5:-5]
        mu1_sq = mu1 ** 2
        mu2_sq = mu2 ** 2
        mu1_mu2 = mu1 * mu2
        sigma1_sq = cv2.filter2D(img1 ** 2, -1, window)[5:-5, 5:-5] - mu1_sq
        sigma2_sq = cv2.filter2D(img2 ** 2, -1, window)[5:-5, 5:-5] - mu2_sq
        sigma12 = cv2.filter2D(img1 * img2, -1, window)[5:-5, 5:-5] - mu1_mu2

        ssim_map = ((2 * mu1_mu2 + C1) * (2 * sigma12 + C2)) / ((mu1_sq + mu2_sq + C1) *
                                                                (sigma1_sq + sigma2_sq + C2))

        #cv2.imsave("image",ssim_map)
        diff = (ssim_map * 255).astype("uint8")
        #diff = cv2.bitwise_not(diff)  # INVER IMAGE
        #thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        diff = cv2.applyColorMap(diff, cv2.COLORMAP_JET)
        #import time
        #timestr = time.strftime("%Y%m%d-%H%M%S")
        #cv2.imwrite("/Users/lito1/Python/imageQAV5/images/diff"+timestr+".jpg",diff )

        return [ssim_map.mean(), diff]

    def calculate_ssim(self,img1, img2):
        '''calculate SSIM
        the same outputs as MATLAB's
        img1, img2: [0, 255]
        '''
        #print(img1.shape)
        #print(img2.shape)
        if  img1.shape != img2.shape:
            AppWarningsClass.critical_warn('Input images must have the same dimensions.')
            return False, False
            #raise ValueError('Input images must have the same dimensions.')
        elif img1.ndim == 2:
            return self.ssim(img1, img2)
        elif img1.ndim == 3:
            if img1.shape[2] == 3:
                #Esto es para el caso que se usen imágenes en color
                #aquí da un error np.array(ssims).mean()
                #actualmente se parte de imágenes en BN
                ssims = []
                for i in range(3):
                    ssims.append(self.ssim(img1, img2))
                return np.array(ssims).mean()
            elif img1.shape[2] == 1:
                return self.ssim(np.squeeze(img1), np.squeeze(img2))
        else:
            AppWarningsClass.critical_warn('Input images must have the same dimensions.')
            return False,False
            #raise ValueError('Wrong input image dimensions.')


    def image_stats(self):
        self.np_im = None
        ssim_data, ssim_img = self.calculate_ssim(self.im2Sample, self.im2Reference)
        if ssim_data:
            mseData = self.mse(self.im2Sample, self.im2Reference)
            psnrData = self.psnr(self.im2Sample, self.im2Reference)
            rmseData = self.rmse(self.im2Sample, self.im2Reference)

            self.np_im = self.resizeImg(ssim_img)
            #cv2.imwrite("/Users/jpereira/Documents/LiClipse_Workspace/imageQAV5/image.jpg",ssim_img )

            # guadar en un array valores lab, Des y Pixeles, Esto puede variar!
            return {"ssim": ssim_data,
                    "mse": mseData,
                    "psnr": psnrData,
                    "rmse": rmseData,
                    "sizeSample": self.imgSampleSize,
                    "sizeReference": self.imgReferenceSize
                    }
        else:
            return False

    def mse(self, imgA, imgB):

        return np.mean((imgA.astype(np.float64) - imgB.astype(np.float64)) ** 2)

    def rmse(self, imgA, imgB):

        return np.sqrt(self.mse(imgA, imgB))

    def psnr(self, imgA, imgB, MAX=None):

        if MAX is None:
            MAX = np.iinfo(imgA.dtype).max

        mse_value = self.mse(imgA, imgB)
        if mse_value == 0.:
            return np.inf
        return 10 * np.log10(MAX ** 2 / mse_value)

    def resizeImg(self,np_im):

        width = int(np_im.shape[1])
        height = int(np_im.shape[0])

        if width > 900 or height > 900:

            diagonal = math.sqrt(  height*height + height*height  )
            factor = diagonal / 900
            dim = (int(width/factor), int(height/factor))
            np_im = cv2.resize(np_im, dim, interpolation=cv2.INTER_AREA)

            # im1.save('ROI.tiff', format='TIFF')
        return np_im