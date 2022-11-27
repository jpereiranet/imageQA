import cv2
import numpy as np
import math
import os
import ntpath

#from sewar.full_ref import uqi, msssim, vifp
#from sewar.full_ref import psnr

class ImgDiffClass():

    MAX_FEATURES = 700
    GOOD_MATCH_PERCENT = 0.10

    def __init__(self, multipleFiles):

        imReference = cv2.imread(multipleFiles[0])
        imReference = cv2.cvtColor(imReference, cv2.COLOR_BGR2GRAY)

        imSample = cv2.imread(multipleFiles[1])
        imSample = cv2.cvtColor(imSample, cv2.COLOR_BGR2GRAY)

        self.imgSampleSize = [imSample.shape[0],imSample.shape[1],round(os.path.getsize(multipleFiles[1])/1024,1), ntpath.basename(multipleFiles[1]) ]
        self.imgReferenceSize = [imReference.shape[0],imReference.shape[1],round(os.path.getsize(multipleFiles[0])/1024,1), ntpath.basename(multipleFiles[0]) ]

        if imSample.shape[0] == imReference.shape[0] and imSample.shape[1] == imReference.shape[1]:
            self.im2Sample = imSample
            self.im2Reference = imReference
        else:
            self.im2Sample, self.im2Reference = self.alignImages(imSample, imReference)


    def alignImages(self, im1, im2):
        # not necessary
        #im2 = self.scaleImages(im2, im1)

        # Detect ORB features and compute descriptors.
        # orb = cv2.ORB_create(self.MAX_FEATURES)
        orb = cv2.ORB_create(scaleFactor=1.2, scoreType=cv2.ORB_FAST_SCORE, nfeatures=self.MAX_FEATURES)
        keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
        keypoints2, descriptors2 = orb.detectAndCompute(im2, None)

        # Match features.
        # matcher = cv2.DescriptorMatcher_create("BruteForce-Hamming")
        matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)

        matches = matcher.match(descriptors1, descriptors2, None)

        # Sort matches by score
        matches.sort(key=lambda x: x.distance, reverse=False)

        # Remove not so good matches
        numGoodMatches = int(len(matches) * self.GOOD_MATCH_PERCENT)
        matches = matches[:numGoodMatches]

        # Extract location of good matches
        points1 = np.zeros((len(matches), 2), dtype=np.float32)
        points2 = np.zeros((len(matches), 2), dtype=np.float32)

        for i, match in enumerate(matches):
            points1[i, :] = keypoints1[match.queryIdx].pt
            points2[i, :] = keypoints2[match.trainIdx].pt

        # Find homography
        h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
        # h es la matriz de homografia

        # Use homography
        height, width = im2.shape
        im1Reg = cv2.warpPerspective(im1, h, (width, height))

        im1Reg = self.convolve(im1Reg)
        im2 = self.convolve(im2)

        return im1Reg, im2

    def scaleImages(self, ref, img):

        Rheight = ref.shape[0]
        Rwidth = ref.shape[1]

        Iheight = img.shape[0]
        Iwidth = img.shape[1]

        ratio = float(Iwidth) / float(Rheight)

        newW = int(Rwidth * ratio)
        newH = int(Rheight * ratio)

        dim = (newW, newH)

        resized = cv2.resize(ref, dim)

        return resized


    def convolve(self, img):
        filter = cv2.bilateralFilter(img, 9, 75, 75)
        return filter


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
        #cv2.imwrite("/Users/jpereira/Documents/LiClipse_Workspace/imageQAV5/image.jpg",thresh )
        return [ssim_map.mean(),diff]

    def calculate_ssim(self,img1, img2):
        '''calculate SSIM
        the same outputs as MATLAB's
        img1, img2: [0, 255]
        '''
        if not img1.shape == img2.shape:
            raise ValueError('Input images must have the same dimensions.')
        if img1.ndim == 2:
            return self.ssim(img1, img2)
        elif img1.ndim == 3:
            if img1.shape[2] == 3:
                ssims = []
                for i in range(3):
                    ssims.append(self.ssim(img1, img2))
                return np.array(ssims).mean()
            elif img1.shape[2] == 1:
                return self.ssim(np.squeeze(img1), np.squeeze(img2))
        else:
            raise ValueError('Wrong input image dimensions.')


    def image_stats(self):

        ssim_data, ssim_img = self.calculate_ssim(self.im2Sample, self.im2Reference)
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