import cv2
import numpy as np
import gc
import configparser
import json
import os
#from blendmodes.blend import blendLayers, BlendType



import cv2
import numpy as np


class RegisterImages:
    '''
    Sort images by size. Reference image always fit was smaller
    '''
    def checkSize(self,  img1, img2):
        height1, width1, _ = img1.shape
        height2, width2, _ = img2.shape

        one = height1 * width1
        two = height2 * width2

        if one > two:
            return img1, img2
        else:
            return img2, img1


    def OrbsRegister(self, img1_color, img2_color):

        features = 5000
        maxmatches= 0.9

        img1_color, img2_color = self.checkSize( img1_color, img2_color)
        height, width, _ = img2_color.shape

        img1 = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
        img2 = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

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



if __name__ == '__main__':

    r = RegisterImages()

    pathA = f"/Users/lito1/Python/imageQAV5/images/DSC_3510_B.jpg"
    pathB = "/Users/lito1/Python/imageQAV5/images/DSC_3510.jpg"

    image_b = cv2.imread(pathA)
    image_a = cv2.imread(pathB)

    aling, ref = r.OrbsRegister(image_a, image_b)

    cv2.imwrite(os.path.join( "/Users/lito1/Python/imageQAV5/images/","a.jpeg"), ref)
    cv2.imwrite(os.path.join( "/Users/lito1/Python/imageQAV5/images/","b.jpeg"), aling)

