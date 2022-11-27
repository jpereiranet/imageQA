import os
import platform
import sys
from plist_set import ProcessSettingsClass


class DefinePathsClass:

    @staticmethod
    def create_resource_path(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        path_icon = os.path.join(application_path, "line-icons", fn)
        return path_icon

    @staticmethod
    def create_reference_paths(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        subpath = ""
        path_icon = os.path.join(application_path, subpath, "reference", fn)

        return path_icon

    @staticmethod
    def create_configuration_paths(fn):

        # application_path = sys._MEIPASS
        application_path = os.path.dirname(sys.argv[0])
        subpath = ""
        path_icon = os.path.join(application_path, subpath, "configuration", fn)

        return path_icon

    @staticmethod
    def get_icc_folder_path():

        params = ProcessSettingsClass()

        if params.setting_contains("iccFolder") and params.setting_restore("iccFolder") != "":
            icc_folder = str(params.setting_restore("iccFolder"))
            if not os.path.isdir(icc_folder):
                icc_folder = None
        else:
            icc_folder = None

        ps = platform.system()

        if ps == "Windows":
            # self.PATH = os.path.expanduser('~user')
            if icc_folder is None:
                icc_folder = "C:\Windows\System32\spool\drivers\color"
                if not os.path.isdir(icc_folder):
                    icc_folder = None
                else:
                    params.save_setting("iccFolder", icc_folder)

        elif ps == "Darwin":
            path = os.path.expanduser('~')
            if icc_folder is None:
                icc_folder = os.path.join(path, "Library/ColorSync/Profiles/")
                if not os.path.isdir(icc_folder):
                    icc_folder = "/Library/ColorSync/Profiles/"
                    if not os.path.isdir(icc_folder):
                        icc_folder = None
                else:
                    params.save_setting("iccFolder", icc_folder)

        return icc_folder
