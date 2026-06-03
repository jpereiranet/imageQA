from colormath.color_conversions import convert_color
from colormath.color_objects import LabColor, sRGBColor

import math
import re
import shlex


class CGATSError(ValueError):
    pass


class GetCGATSClass:

    REQUIRED_FIELDS = ("SAMPLE_ID", "LAB_L", "LAB_A", "LAB_B")

    def __init__(self, cgatsFile):
        self.cgatsFile = cgatsFile
        with open(self.cgatsFile, "r", encoding="utf-8-sig", errors="replace") as cgats_handle:
            self.lines = cgats_handle.readlines()

        self.fields = self.get_lab_from_cgats()
        self.read_cgats_file()
        #self.get_patch_name()
        #self.lab_to_rgb()

    def _split_cgats_line(self, line):

        lexer = shlex.shlex(line, posix=True)
        lexer.whitespace_split = True
        lexer.commenters = "#"
        return list(lexer)

    def _get_section_indexes(self, begin_tag, end_tag):

        start = None
        end = None

        for idx, item in enumerate(self.lines):
            tokens = self._split_cgats_line(item)
            if not tokens:
                continue

            marker = tokens[0].upper()
            if marker == begin_tag:
                start = idx
            elif marker == end_tag and start is not None:
                end = idx
                break

        if start is None or end is None or end <= start:
            raise CGATSError("CGATS file does not contain a valid " + begin_tag + "/" + end_tag + " section")

        return start, end

    def get_lab_from_cgats(self):

        fields = []
        start, end = self._get_section_indexes("BEGIN_DATA_FORMAT", "END_DATA_FORMAT")

        for idx, item in enumerate(self.lines):
            if start < idx < end:
                fields.extend(self._split_cgats_line(item))

        if not fields:
            raise CGATSError("CGATS DATA_FORMAT section is empty")

        missing = [field for field in self.REQUIRED_FIELDS if field not in fields]
        if missing:
            raise CGATSError("CGATS file does not contain required tag(s): " + ", ".join(missing))

        return fields

    def _get_field_value(self, values, field_index, field_name):

        index = field_index.get(field_name)
        if index is None:
            return None

        if index >= len(values):
            raise CGATSError("CGATS data row does not contain a value for " + field_name)

        return values[index]

    def read_cgats_file(self, fields=None):

        if fields is None:
            fields = self.fields

        start, end = self._get_section_indexes("BEGIN_DATA", "END_DATA")
        field_index = {field: index for index, field in enumerate(fields)}

        self.labCGATS = []

        for idx, item in enumerate(self.lines):

            if start < idx < end:
                values = self._split_cgats_line(item)
                if not values:
                    continue

                if len(values) < len(fields):
                    raise CGATSError("CGATS data row " + str(idx + 1) + " has fewer values than DATA_FORMAT")

                sample_id = self._get_field_value(values, field_index, "SAMPLE_ID")
                sample_name = self._get_field_value(values, field_index, "SAMPLE_NAME")

                lab_l = round(self.string_to_float(self._get_field_value(values, field_index, "LAB_L")), 2)
                lab_a = round(self.string_to_float(self._get_field_value(values, field_index, "LAB_A")), 2)
                lab_b = round(self.string_to_float(self._get_field_value(values, field_index, "LAB_B")), 2)

                rgbr, rgbg, rgbb = self.lab_to_rgb_2(lab_l, lab_a, lab_b)
                luma = self.rgb_to_luma(rgbr, rgbg, rgbb)

                dvis = self._get_field_value(values, field_index, "D_VIS")
                if dvis is None:
                    dvis = self.RGB_to_density(luma)

                refDic = {
                    "SAMPLE_ID": sample_id,
                    "SAMPLE_NAME": sample_name,
                    "PATCH_NAME": sample_name or sample_id,
                    "LAB_L": lab_l,
                    "LAB_A": lab_a,
                    "LAB_B": lab_b,
                    "RGB_R": rgbr,
                    "RGB_G": rgbg,
                    "RGB_B": rgbb,
                    "D_VIS": round(self.string_to_float(dvis), 2),
                    "LUMA": luma,
                    "IS_GRAY": self.is_gray_patch(sample_id, sample_name, lab_a, lab_b)
                }
                self.labCGATS.append(refDic)
                #self.labCGATS.append([values[0],self.string_to_float(values[1]),self.string_to_float(values[2]),self.string_to_float(values[3])])

        self.mark_classic_colorchecker_gray_patches()

        #print(self.labCGATS)
        return self.labCGATS

    def is_gray_patch(self, sample_id, sample_name, lab_a, lab_b):

        return math.hypot(lab_a, lab_b) <= 5

    def normalize_patch_name(self, patch_name):

        patch_name = (patch_name or "").strip().upper()
        match = re.fullmatch(r"([A-Z]+)0*(\d+)", patch_name)
        if not match:
            return patch_name

        return match.group(1) + str(int(match.group(2)))

    def mark_classic_colorchecker_gray_patches(self):

        if len(self.labCGATS) != 24:
            return

        names = {self.normalize_patch_name(patch["PATCH_NAME"]) for patch in self.labCGATS}
        classic_names = {
            row + str(column)
            for row in ("A", "B", "C", "D")
            for column in range(1, 7)
        }

        if names != classic_names:
            return

        for patch in self.labCGATS:
            patch_name = self.normalize_patch_name(patch["PATCH_NAME"])
            if re.fullmatch(r"D[1-6]", patch_name):
                patch["IS_GRAY"] = True

    def rgb_to_luma(self, rgbr, rgbg, rgbb):

        y = 0.2126 * rgbr + 0.7152 * rgbg + 0.0722 * rgbb
        return round(y,0)

    def RGB_to_density(self, luma):

        luma = max(float(luma), 1.0)
        density = round( math.log10(math.pow((255 / luma), 2.2)), 2)
        return density


    def lab_to_rgb_2(self, CIEL,CIEa,CIEb):
        '''
        Convierte a RGB para colorear las barras de los graficos para una comprension viusal
        '''
        CIEL = self.string_to_float(CIEL)
        CIEa = self.string_to_float(CIEa)
        CIEb = self.string_to_float(CIEb)
        lab = LabColor(CIEL,CIEa,CIEb)
        rgb = convert_color(lab, sRGBColor)
        a = vars(rgb)
        g = self.check_rgb_range(round(a["rgb_g"] * 255))
        r = self.check_rgb_range(round(a["rgb_r"] * 255))
        b = self.check_rgb_range(round(a["rgb_b"] * 255))
        return r, g, b

    def string_to_float(self, string):

        string = str(string).strip().strip('"').replace(',', '.')
        try:
            return float(string)
        except:
            return float(string)
    '''
    def get_patch_name(self):

        self.patchName = []
        for patch in self.labCGATS:
            self.patchName.append(patch[0])

        # print(self.patchName)
    '''
    def lab_to_rgb(self):
        '''
        Convierte a RGB para colorear las barras de los graficos para una comprension viusal
        '''
        self.RGB = []
        for patch in self.labCGATS:
            # aRGB = []
            lab = LabColor(patch[1], patch[2], patch[3])
            rgb = convert_color(lab, sRGBColor)
            a = vars(rgb)
            g = self.check_rgb_range(round(a["rgb_g"] * 255))
            r = self.check_rgb_range(round(a["rgb_r"] * 255))
            b = self.check_rgb_range(round(a["rgb_b"] * 255))
            self.RGB.append([r, g, b])



    def check_rgb_range(self, value):

        return max(0, min(255, int(value)))
