import io
import os

from PIL import Image, ImageCms


class GetImgInfo():
    def __init__(self, rgb_image):

        self.rgb_image = Image.open(rgb_image)
        self.get_icc_info()
        self.rgb_image.close()

    def get_icc_info(self):

        icc = self.rgb_image.info.get('icc_profile')

        if icc:
            if type(icc) == tuple:
                f = io.BytesIO(icc[0])  # esto es necesario para tiff porque el perfil aparece como tuple no str
            else:
                f = io.BytesIO(icc)

            self.profile = ImageCms.ImageCmsProfile(f)

            self.iccDescription = ImageCms.getProfileDescription(self.profile)
            # self.iccInfo = ImageCms.getProfileInfo(self.profile) #copyright
            # self.iccModel = ImageCms.getProfileModel(self.profile) #vacio

            # print(self.iccDescription)
            illum = str(self.profile.profile.media_white_point_temperature)
            self.iccInfoDic = {
                "fileName": self.profile.profile.profile_description,
                "copyright": self.profile.profile.copyright,
                # "fecha":self.profile.profile.creation_date, #he detectado algun error con el formato de algunas fechas, revisar!
                "blanco": "D" + illum[0:2],
                "pcs": self.profile.profile.xcolor_space,
                "version": self.profile.profile.manufacturer,
                "model": self.profile.profile.model,
                "type": self.profile.profile.device_class  # scnr son los input
            }


        else:
            self.iccInfoDic = {
                "fileName": "Warning no ICC Profile Found!",
                "copyright": "", "fecha": "", "blanco": "?", "pcs": "", "version": "", "model": "", "type": ""
            }

        # print(self.iccInfoDic)
        return self.iccInfoDic

    def image_name(self):

        return os.path.basename(self.rgb_image.filename)
        # return(exif)

# a = getImgInfo("/Users/jpereira/Pictures/DSC_0205.tif")
# print(a.imageMetadata())
