from metadata_class import GetMetadataClass
from plist_set import ProcessSettingsClass
from warning_class import AppWarningsClass


class CameraInformationClass:

    def __init__(self):

        self.params = ProcessSettingsClass()

    def rese_camera_information(self):

        self.params = ProcessSettingsClass()
        self.params.save_setting("camera/widthSensor", "")
        self.params.save_setting("camera/heightSensor", "")
        self.params.save_setting("camera/imgWidth", "")
        self.params.save_setting("camera/imgHeight", "")
        self.params.save_setting("camera/pitch", "")

        self.params.save_setting("camera/rulePixel", "")
        self.params.save_setting("camera/ruleReal", "")
        self.params.save_setting("camera/resolution", "")

    def set_camera_information(self, filename):

        self.meta = GetMetadataClass(filename)
        cameraInfo = self.meta.get_sensor_information()

        self.params.save_setting("camera/widthSensor", cameraInfo["widthSensor"])
        self.params.save_setting("camera/heightSensor", cameraInfo["heightSensor"])
        self.params.save_setting("camera/imgWidth", cameraInfo["imgWidth"])
        self.params.save_setting("camera/imgHeight", cameraInfo["imgHeight"])
        self.params.save_setting("camera/pitch", cameraInfo["pitch"])

        self.params.save_setting("camera/rulePixel", "")
        self.params.save_setting("camera/ruleReal", "")
        self.params.save_setting("camera/resolution", "")

    def get_metadata(self):

        widthSensor = self.params.setting_restore("camera/widthSensor")
        heightSensor = self.params.setting_restore("camera/heightSensor")
        imgWidth = self.params.setting_restore("camera/imgWidth")
        imgHeight = self.params.setting_restore("camera/imgHeight")
        pitch = self.params.setting_restore("camera/pitch")

        rulePixel = self.params.setting_restore("camera/rulePixel")
        ruleReal = self.params.setting_restore("camera/ruleReal")
        resolution = self.params.setting_restore("camera/resolution")


        o = {}

        if rulePixel != None:
            o["rulePixel"] = rulePixel
        else:
            o["rulePixel"] = ""

        if ruleReal is not None:
            o["ruleReal"] = ruleReal
        else:
            o["ruleReal"] = ""

        if resolution is not None:
            o["resolution"] = resolution
        else:
            o["resolution"] = ""

        if widthSensor is not None:
            o["widthSensor"] = widthSensor
        else:
            o["widthSensor"] = ""

        if heightSensor is not None:
            o["heightSensor"] = heightSensor
        else:
            o["heightSensor"] = ""

        if imgWidth is not None:
            o["imgWidth"] = imgWidth
        else:
            o["imgWidth"] = ""

        if imgHeight is not None:
            o["imgHeight"] = imgHeight
        else:
            o["imgHeight"] = ""

        if pitch is not None:
            o["pitch"] = pitch
        else:
            o["pitch"] = ""


        return o



    def check_if_number(self, value):

        try:
            float(value)
            return True
        except ValueError:
            return False

    def save_camera_values(self, values):

        noValidate = ["rulePixel", "ruleReal"]
        for key, value in values.items():

            if key not in noValidate:
                if not self.check_if_number(value):
                    AppWarningsClass.status_warn("Some value is empty or not numeric")
                    return False

        self.params.save_setting("camera/widthSensor", values["widthSensor"])
        self.params.save_setting("camera/heightSensor", values["heightSensor"])
        self.params.save_setting("camera/imgWidth", values["imgWidth"])
        self.params.save_setting("camera/imgHeight", values["imgHeight"])
        self.params.save_setting("camera/pitch", values["pitch"])

        self.params.save_setting("camera/rulePixel", values["rulePixel"])
        self.params.save_setting("camera/ruleReal", values["ruleReal"])
        self.params.save_setting("camera/resolution", values["resolution"])

        if float(values["pitch"]) > 7:
            std = AppWarningsClass.informative_true_false(
                "Pixel pitch is too long, perhaps the size of your sensor is wrong. Continue?")
        else:
            AppWarningsClass.status_warn("Camera information saved!")
            std = True

        return std

    def check_pitch(self):

        pitch = self.params.setting_restore("camera/pitch")

        if pitch is not None:
            try:
                float(pitch)

                if float(pitch) > 7:
                    notes = "Pixel pitch is not set or is too long, MTF (Lp / mm) will not be accurate. You must set the pixel pitch in the camera information dialog"
                    return False, notes

                if float(pitch) < 7:
                    notes = ""
                    return True, notes

            except ValueError:

                notes = "Pixel pitch is not set. You must set the pixel pitch in the camera information dialog it order to calculate the MTF in Lp / mm"
                return False, notes
        else:

            notes = "Pixel pitch is not set. You must set the pixel pitch in the camera information dialog it order to calculate the MTF in Lp / mm"
            return False, notes
