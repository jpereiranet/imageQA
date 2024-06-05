import io

from PIL import Image, ImageCms, ImageQt
from PyQt5 import QtGui


class ImgTransformClass:

    def __init__(self, image_path, profile_path):

        self.in_image = Image.open(image_path)
        self.mode = self.in_image.mode

        self.width, self.height = self.in_image.size

        self.factor = float(self.height) / float(self.width)

        self.profile_path = profile_path

    def embebed_profile(self):
        # print(bool(self.profile_path))

        if bool(self.profile_path):
            # print("lzan perfil")
            return ImageCms.getOpenProfile(self.profile_path)
        else:
            # print("extrae perfil")
            return self.get_icc_profile()

    def get_icc_profile(self):

        icc = self.in_image.info.get('icc_profile')

        if icc:

            if type(icc) == tuple:
                f = io.BytesIO(icc[0])  # esto es necesario para tiff porque el perfil aparece como tuple no str
            else:
                f = io.BytesIO(icc)

            rgb_profile = ImageCms.ImageCmsProfile(f)
        else:
            rgb_profile = False

        return rgb_profile

    def get_ratio_transform(self):

        MAXWIDTH = 600
        MAXHEIGHT = 400

        # dMAX = math.sqrt((MAXWIDTH*MAXWIDTH)+(MAXHEIGHT*MAXHEIGHT ))
        width, height = self.in_image.size
        # dImg = math.sqrt((width*width)+(height*height ))

        if (width <= MAXWIDTH and height <= MAXHEIGHT):
            aspectRatio = 1
            aspectRatioTransform = 1
        else:
            rel = float(width) / float(height)

            x_ratio = MAXWIDTH / width
            y_ratio = MAXHEIGHT / height

            xt_ratio = width / MAXWIDTH
            yt_ratio = height / MAXHEIGHT

            # if width > height:
            if rel > 1.3:
                aspectRatio = x_ratio
                aspectRatioTransform = xt_ratio
            # elif height > width:
            if rel < 1.3:
                aspectRatio = y_ratio
                aspectRatioTransform = yt_ratio
            # elif height == width:
            #    aspectRatio = y_ratio
            #    aspectRatioTransform = yt_ratio

            # aspectRatio =  dMAX / dImg
            # aspectRatioTransform =   dImg / dMAX

        # rel = float(width) / float(height)

        # if rel > 2:
        #    aspectRatioTransform = aspectRatioTransform / 1.2
        #   aspectRatio = aspectRatio / 1.2

        newWidth = int(width * aspectRatio)
        newHeight = int(height * aspectRatio)

        d = [MAXWIDTH, MAXHEIGHT, width, height, newWidth, newHeight, aspectRatio, aspectRatioTransform]

        # print(d)

        return d

    def image_thumbnail(self):

        imgSizing = self.get_ratio_transform()

        newimg = self.in_image.resize((imgSizing[4], imgSizing[5]))

        pilImage = self.rgb2rgb(newimg)

        return pilImage

    def image_previsualization(self):

        imgSizing = self.get_ratio_transform()

        newimg = self.in_image.resize((imgSizing[4], imgSizing[5]))

        s = self.rgb2rgb(newimg)

        # toqpixmap solo esta presente en la version > 4.3.0 de PIL
        # con version 10.3 no funciona, usar funcion alternativa
        #qimage = ImageQt.toqpixmap(s)

        qimage = self.pil2pixmap(s)

        return qimage
        # self.in_image.close()  #esto peta en linux???

    def pil2pixmap(self, im):
        '''
        from Michael https://stackoverflow.com/questions/34697559/pil-image-to-qpixmap-conversion-issue
        '''
        if im.mode == "RGB":
            r, g, b = im.split()
            im = Image.merge("RGB", (b, g, r))
        elif im.mode == "RGBA":
            r, g, b, a = im.split()
            im = Image.merge("RGBA", (b, g, r, a))
        elif im.mode == "L":
            im = im.convert("RGBA")
        # Bild in RGBA konvertieren, falls nicht bereits passiert
        im2 = im.convert("RGBA")
        data = im2.tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, im.size[0], im.size[1], QtGui.QImage.Format_ARGB32)
        pixmap = QtGui.QPixmap.fromImage(qim)
        return pixmap

    def rgb2rgb(self, in_image):

        if self.embebed_profile() and self.mode == "RGB":
            #
            out_profile = ImageCms.createProfile(colorSpace='sRGB')

            rgb_to_rgb_transform = ImageCms.buildTransform(
                inputProfile=self.embebed_profile(),
                outputProfile=out_profile,
                inMode='RGB',
                outMode='RGB'
            )

            self.out_image = ImageCms.applyTransform(
                im=in_image,
                transform=rgb_to_rgb_transform
            )

        else:
            self.out_image = in_image

        return self.out_image
