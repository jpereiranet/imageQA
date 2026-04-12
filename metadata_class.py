import exifread
from PIL import Image

from xmp_parser import XmpParser


# print(sys.path)

class GetMetadataClass:

    def __init__(self, filename):

        self.filename = filename

        with Image.open(self.filename) as img:
            self.img_format = img.format
            self.img_info = dict(img.info)
            self.img_size = img.size

        # print(self.getSensorInfo() )

    def get_exposure(self):

        exposure = 0
        aperture = 0
        iso = 0

        if self.img_format == "PNG" and 'XML:com.adobe.xmp' in self.img_info:
            data = self.img_info['XML:com.adobe.xmp']
            var = XmpParser(data).read_meta
            var = var["http://ns.adobe.com/exif/1.0/"]

            if 'ExposureTime' in var:
                exposure = var['ExposureTime']
            else:
                exposure = 0

            if 'FNumber' in var:
                aperture = var['FNumber']
                aperture = self.normalize_aperture(aperture)
            else:
                aperture = 0

            if 'ISOSpeedRatings' in var:
                iso = var['ISOSpeedRatings']
            else:
                iso = 0

        elif self.img_format == "JPEG" or self.img_format == "TIFF":
            with open(self.filename, 'rb') as image_file:
                metadata = exifread.process_file(image_file)

            if "EXIF ExposureTime" in metadata:
                exposure = metadata["EXIF ExposureTime"]
            else:
                exposure = 0
            if "EXIF FNumber" in metadata:
                aperture = metadata["EXIF FNumber"]
                aperture = self.normalize_aperture(str(aperture))
            else:
                aperture = 0

            if "EXIF ISOSpeedRatings" in metadata:
                iso = metadata["EXIF ISOSpeedRatings"]
            else:
                iso = 0

        return str(exposure), str(aperture), str(iso)

    def normalize_aperture(self, aperture):

        if '/' in aperture:
            v = aperture.split("/")
            o = float(v[0]) / float(v[1])
        else:
            o = aperture

        return o

    def forcelanscape(self, width, height):

        arr = [width,height]
        arr.sort(reverse=True)

        return arr[0],arr[1]

    def computeFocal(self, cadena):
        print(cadena)
        if cadena.find("/") > 0:
            arr = cadena.split("/")
            focal = float(arr[0]) / float(arr[1])
            print("FOCAL ", focal)
            return focal
        else:
            print("CADENA: ", cadena)
            return cadena



    def get_sensor_information(self):
        imgWidth = 0
        imgHeigh = 0
        factorCrop = 0
        widthSensor = 0
        heightSensor = 0
        pitch = 0

        if (self.img_format == "PNG") and ('XML:com.adobe.xmp' in self.img_info):
            factorCrop = 0
            widthSensor = 0
            heightSensor = 0
            pitch = 0

            #considrar usar "Focal Plane X Resolution"?
            data = self.img_info['XML:com.adobe.xmp']
            var = XmpParser(data).read_meta
            if "http://ns.adobe.com/exif/1.0/" in var:
                var = var["http://ns.adobe.com/exif/1.0/"]

                if "ExifImageWidth" in var and "ExifImageLength" in var:
                    imgWidth = str(var["EXIF ExifImageWidth"])
                    imgHeigh = str(var["EXIF ExifImageLength"])
                    imgWidth,imgHeigh = self.forcelanscape(imgWidth, imgHeigh)

                else:
                    width, height = self.img_size
                    imgWidth,imgHeigh = self.forcelanscape(width, height)

                if "FocalLengthIn35mmFilm" in var and "FocalLength" in var:
                    focal35 = self.normalize_aperture(str(var["FocalLengthIn35mmFilm"]))
                    focal = self.normalize_aperture(str(var["FocalLength"]))

                    factorCrop = round(float(focal35) / float(focal), 2)

                    widthSensor = 36 / factorCrop
                    heightSensor = 24 / factorCrop

                    widthSensor, heightSensor = self.forcelanscape(widthSensor, heightSensor)

                    if imgWidth != 0:
                        pitch = round((float(widthSensor) / float(imgWidth)) * 1000, 2)



        elif self.img_format == "JPEG" or self.img_format == "TIFF":
            with open(self.filename, 'rb') as image_file:
                metadata = exifread.process_file(image_file)
            # print(meta)

            if "EXIF ExifImageWidth" in metadata and "EXIF ExifImageLength" in metadata:
                imgWidth = str(metadata["EXIF ExifImageWidth"])
                imgHeigh = str(metadata["EXIF ExifImageLength"])
                imgWidth, imgHeigh = self.forcelanscape(imgWidth, imgHeigh)
            else:
                width, height = self.img_size
                imgWidth, imgHeigh = self.forcelanscape(width, height)

            if "EXIF FocalLengthIn35mmFilm" in metadata and "EXIF FocalLength" in metadata:
                focal35 = str(metadata["EXIF FocalLengthIn35mmFilm"])
                focal = str(metadata["EXIF FocalLength"])

                if focal35 != "0":
                    factorCrop = round(float(focal35) / float(focal), 2)

                    widthSensor = 36 / factorCrop
                    heightSensor = 24 / factorCrop

                    widthSensor, heightSensor = self.forcelanscape(widthSensor, heightSensor)


                    if imgWidth != 0:
                        pitch = round((float(widthSensor) / float(imgWidth)) * 1000, 2)


        o = {"imgWidth": imgWidth, "imgHeight": imgHeigh, "factorCrop": factorCrop, "widthSensor": int(widthSensor),
             "heightSensor": int(heightSensor), "pitch": pitch}


        return o



# getMetadata("/Users/jpereira/Pictures/DSC_0205.tif")

# getMetadata("/Volumes/Macintosh_HD_ENC/CURSOS/colorchecker/DSC_0206_LINEAL_RX400.tif")
# getMetadata("/Volumes/Macintosh_HD_DATA/imageIQ/jpeg-vinheteado/DSC_3687.jpg")
