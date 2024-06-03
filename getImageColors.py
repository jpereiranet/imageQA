# -*- coding: utf-8 -*-
import io

from PIL import Image, ImageCms, ImageStat
from ImgTransformClass import ImgTransformClass
from get_icc_tags import GetICCtags
from app_paths import DefinePathsClass
import configparser
from os import path



class getImageColors:

    def __init__(self, pos, rgb_image, profile_path):

        self.config = configparser.ConfigParser()
        path_conf_file = DefinePathsClass.create_configuration_paths("configuration.ini")
        if path.exists(path_conf_file):
            self.config.read(path_conf_file)
            self.sampling_size = int(self.config['SAMPLING']['SAMPLE_SIZE'])
            self.default_gamma = float(self.config['SAMPLING']['DEFAULT_GAMMA'])
            self.illum = self.config['SAMPLING']['DEFAULT_ILLUMINANT']
        else:
            self.sampling_size = 60
            self.illum = "D50"
            self.default_gamma = 2.2

        self.im = ImgTransformClass(rgb_image, profile_path)

        self.ratio = self.im.get_ratio_transform()

        self.rgb_image = Image.open(rgb_image)

        if len(pos) == 4:
            self.pos = self.scale_coordinates_roi(pos)
        else:
            self.pos = self.scale_coordinates(pos)

        self.profile_path = profile_path

    def scale_coordinates(self, pos):

        npos = []
        for c in pos:
            cx = int(c[0] * self.ratio[7])
            cy = int(c[1] * self.ratio[7])
            npos.append([cx, cy])

        return npos

    def scale_coordinates_roi(self, pos):

        npos = []
        for c in pos:
            value = int(c * self.ratio[7])
            npos.append(value)
        return npos

    def embebed_profile(self):
        # print(bool(self.profile_path))

        if bool(self.profile_path):
            # print("carga nuevo perfil")
            return ImageCms.getOpenProfile(self.profile_path)
        else:
            # print("carga perfil incorporado")
            return self.getICC()

    def getICC(self):
        """
        Extrae el perfill ICC de la imagen para usarlo en las conversiones RGB -> Lab
        """
        icc = self.rgb_image.info.get('icc_profile')

        #obtiene la gamma del perfil si es posible
        #tags = GetICCtags()
        #sTags = tags.getGamma(icc)
        #self.gamma = sTags
        #print(self.gamma)

        #print(icc)
        if icc:
            if type(icc) == tuple:
                f = io.BytesIO(icc[0])  # esto es necesario para tiff porque el perfil aparece como tuple no str
            else:
                f = io.BytesIO(icc)

            self.rgb_profile = ImageCms.ImageCmsProfile(f)

            #if hasattr(self.rgb_profile.profile, "media_white_point_temperature"):
            #    self.illum = str(self.rgb_profile.profile.media_white_point_temperature)
                #print(self.rgb_profile.profile. profile_description)
            #else:
            #    self.illum = "5000"

        else:
            #self.illum = "5000"
            self.rgb_profile = ImageCms.createProfile(colorSpace='sRGB')

            # self.warning("ICC profile not found, use sRGB")

        return self.rgb_profile


    def get_icc_info(self):
        """
        Extrae alguna informacion sobre el perfil usado en la imagen
        """
        # https://pillow.readthedocs.io/en/4.2.x/reference/ImageCms.html#PIL.ImageCms.CmsProfile
        self.iccDescription = ImageCms.getProfileDescription(self.rgb_profile)
        self.iccInfo = ImageCms.getProfileInfo(self.rgb_profile)


        # print(self.iccDescription)
        # print(self.iccInfo)

    def icc_translate(self):
        """
        Aplica el pefil extraido de la imagen a la imagen para pasarla a valores Lab
        """
        # rgb_profile = ImageCms.createProfile(colorSpace='sRGB')
        # rgb_profile = ImageCms.getOpenProfile("/Users/jpereira/Library/ColorSync/Profiles/1_NIKON_D7200_-2_RX400.icc")
        lab_profile = ImageCms.createProfile(colorSpace='LAB')

        rgb_to_lab_transform = ImageCms.buildTransform(
            inputProfile=self.embebed_profile(),
            outputProfile=lab_profile,
            inMode='RGB',
            outMode='LAB'
        )

        self.lab_image = ImageCms.applyTransform(
            im=self.rgb_image,
            transform=rgb_to_lab_transform
        )

    def get_lab_values(self):
        """
        Recorre toda la imagen, y llama a la funcion cortar() para quedarnos con el centro de cada parche
        """
        self.getICC()
        self.icc_translate()

        self.Lab = []
        for x in range(len(self.pos)):
            im1 = self.slice_image(self.pos[x], self.lab_image)
            s = self.image_stats(im1, "LAB")
            self.Lab.append(s)

        return self.Lab

    def get_all_lab_values_dowscale(self):

        left = self.pos[0]
        top = self.pos[1]
        right = self.pos[2]
        bottom = self.pos[3]
        self.rgb_image = self.rgb_image.crop((left, top, right, bottom))

        self.getICC()
        self.icc_translate()

        size = self.sampling_size, self.sampling_size
        self.lab_image.thumbnail(size, Image.ANTIALIAS)
        #self.lab_image.save("newlab.tiff")

        pixels = self.lab_image.load()
        width, height = self.lab_image.size

        all_pixels = []
        for x in range(width):
            for y in range(height):
                cpixel = pixels[x, y]
                all_pixels.append(self.normalize_lab_values(cpixel))

        return all_pixels



    def get_rgb_values(self):
        self.RGB = []
        for x in range(len(self.pos)):
            im = self.slice_image(self.pos[x], self.rgb_image)
            s = self.image_stats(im, "RGB")
            self.RGB.append(s)

        return self.RGB

    def merge_colorimetry(self):

        self.imageFullStats = []
        i = 0
        for x in self.Lab:
            self.imageFullStats.append(self.merge_two_dicts(x, self.RGB[i]))
            i += 1
        return self.imageFullStats

    def merge_two_dicts(self, x, y):

        z = x.copy()  # start with x's keys and values
        z.update(y)  # modifies z with y's keys and values & returns None
        return z

    def slice_image(self, coo, im):
        """
        Corta el centro de cada parche y aplica la funcion ImageStat para obtener el promedio de los pixeles del recorte
        Con estos recortes se podria componer una nueva imagen para realizar una comparativa visual entre resultados
        !este metodo hay que organizarlo en varios!
        """

        offset = 5
        left = coo[0] - offset
        top = coo[1] - offset
        right = coo[0] + offset
        bottom = coo[1] + offset
        im1 = im.crop((left, top, right, bottom))

        # im1.save(str(coo[0])+"-"+str(coo[1])+"lab.tiff", format='TIFF')
        # self.guardaSecciones(coo, im)
        return im1

    def image_stats(self, im, mode):

        st = ImageStat.Stat(im)
        promedio = st.mean
        ex = st.extrema

        if mode == "LAB":
            color = self.normalize_lab_values(promedio)  # crea Lab
            luma = 'NA'
            desvY = 'NA'
        else:
            color = promedio
            luma = self.get_luma(color)

            #para calcular la desviación de la imagen en luma solo
            imgGray = im.convert('LA')
            stY = ImageStat.Stat(imgGray)
            desvY = stY.stddev[0]


        desv = st.stddev  # Crea desviacion estandar
        pixeles = st.count  # apunta los pixeles promedidados
        # snr = self.calculaRuido(promedio, desv )

        # guadar en un array valores lab, Des y Pixeles, Esto puede variar!
        return {mode: color,
                mode + "_DESV": desv,
                mode + "_YDESV": desvY,
                mode + "_nPixeles": pixeles,
                mode + "_extrema": ex,
                mode + "_LUMA": luma,
                }

    # lab_image.save('lab.tiff', format='TIFF')

    def getGammaFactor(self):

        icc = self.rgb_image.info.get('icc_profile')
        tags = GetICCtags()
        sTags = tags.getGamma(icc)
        return sTags


    def lineriza(self, RGB, gamma):
        Lr = (((RGB[0]/255)**gamma)**(1/self.default_gamma))*255
        Lg = (((RGB[1]/255)**gamma)**(1/self.default_gamma))*255
        Lb = (((RGB[2]/255)**gamma)**(1/self.default_gamma))*255

        return (Lr,Lg,Lb)

    def get_luma(self, RGB):

        gamma = self.getGammaFactor()
        RGB = self.lineriza(RGB, gamma)

        if len(RGB) > 1:
            y = 0.2126 * RGB[0] + 0.7152 * RGB[1] + 0.0722 * RGB[2]
        else:
            y = RGB[0]

        return round(y,0)

    def get_roi_image(self):

        # img = self.rgb_image
        # img.thumbnail((600,600), Image.ANTIALIAS)

        img = self.im.image_thumbnail()

        image = Image.new('RGBA', (20, 20), (0, 255, 0))
        for c in self.pos:
            x = int(c[0] / self.ratio[7]) - 10
            y = int(c[1] / self.ratio[7]) - 10
            img.paste(image, (x, y))

        # self.rgb_image.show()

        temp = self.image_to_byte_array(img)

        return temp

    def get_visual_roi(self, RGB):

        # img2 = self.rgb_image
        # img2.thumbnail((600,600), Image.ANTIALIAS)
        img2 = self.im.image_thumbnail()

        i = 0
        for c in self.pos:
            R = int(RGB[i]["RGB_R"])
            G = int(RGB[i]["RGB_G"])
            B = int(RGB[i]["RGB_B"])

            x = int(c[0] / self.ratio[7]) - 20
            y = int(c[1] / self.ratio[7]) - 20

            image = Image.new('RGBA', (40, 40), (R, G, B))
            img2.paste(image, (x, y))
            i = i + 1

        # self.rgb_image.show()
        temp = self.image_to_byte_array(img2)

        return temp

    def image_to_byte_array(self, image):

        imgByteArr = io.BytesIO()
        image.save(imgByteArr, format="jpeg")
        imgByteArr = imgByteArr.getvalue()

        return imgByteArr

    def normalize_lab_values(self, rgb):
        """
        La imagen Lab construida presenta los valores de sus canales en RGB y se deben normalizar como Lab
        """
        cieL = round((float(rgb[0]) / 255) * 100,2)
        ciea = round((float(rgb[1]) - 128), 2)
        cieb = round((float(rgb[2]) - 128), 2)
        # iStd = "D"+self.illum[0:2] #el iluminante se manda para las funciones que calculan los deltas
        #iStd = "D50"  # tiene que ser por rangos D50 o D55 o D65
        return [cieL, ciea, cieb, self.illum.strip('"')]
