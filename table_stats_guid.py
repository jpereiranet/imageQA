# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtWidgets

from save_report import saveReportToFileClass

import csv, io

try:
    _encoding = QtWidgets.QApplication.UnicodeUTF8


    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtWidgets.QApplication.translate(context, text, disambig)


class TableStatsUI(object):

    def __init__(self, value, key, patches):

        self.value = value
        self.key = key

        if key == "CIE76" or key == "CIE00" or key == "CMC" or key == "CIE94" or key == "DEC" or key == "DEH" or key == "DEL":
            report = saveReportToFileClass( value, None, None)
            self.data = report.save_deltae_color(key)


        elif key == "OECF" or key == "GREEN" or key == "BLUE" or key == "RED":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_oecf()

        elif key == "LGAIN":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_lgain()

        elif key == "RGB":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_rgb()


        elif key == "DEV" or key == "WB":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_delta_ev()

        elif key == "SNR" or key == "RDEV":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_snr(key)


        elif key == "SNR-RGB":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_snr_rgb()

        elif key == "C_NOISE":

            report = saveReportToFileClass(None, value, None, None)
            self.data = report.save_croma_noise()

        elif key == "NPS_RGB_X" or key == "NPS_RGB_Y":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_nps_rgb()

        elif key == "HISTO":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_histo()

        elif key == "MTF" or key == "LSF" or key == "ESF":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_mtf(key)

        elif key == "CIE76_MULTI" or key == "CIE00_MULTI" or key == "CMC_MULTI":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_deltae_color_multiple()

        elif key == "DEV_MULTI":
            report = saveReportToFileClass( value, None, None)
            self.data = report.save_delta_ev_multiple()

        elif key == "SNR_MULTI":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_snr_multiple()

        elif key == "OECF_MULTI":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_oecf_multiple()

        elif key == "SENSITOMETRY_MULTI":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_sensitometry()

        elif key == "MTF_MULTI":

            report = saveReportToFileClass( value, None, None)
            self.data = report.save_mtf_multiple()

        # print(self.data)

    def setupUi(self, Dialog):
        super(TableStatsUI, self).__init__()
        Dialog.setObjectName("Dialog")
        Dialog.resize(670, 431)
        Dialog.setWindowTitle(_translate("Data Table", "Data Table " + self.key, None))

        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(20, 10, 600, 371))
        self.tableWidget.setObjectName("tableWidget")

        self.tableWidget.setRowCount(len(self.data))
        self.tableWidget.setColumnCount(len(self.data[0]))

        for i, row in enumerate(self.data):
            for j, col in enumerate(row):
                item = QtWidgets.QTableWidgetItem(col)
                self.tableWidget.setItem(i, j, item)

        self.btClose = QtWidgets.QPushButton(Dialog)
        self.btClose.setGeometry(QtCore.QRect(20, 390, 113, 32))
        self.btClose.setObjectName("pushButton")
        self.btClose.setText(_translate("Dialog", "Close", None))
        self.btClose.clicked.connect(Dialog.close)

        self.btCopy = QtWidgets.QPushButton(Dialog)
        self.btCopy.setGeometry(QtCore.QRect(143, 390, 113, 32))
        self.btCopy.setObjectName("pushButton")
        self.btCopy.setText(_translate("Dialog", "Copy", None))
        self.btCopy.clicked.connect(self.copySelection)
        self.btCopy.setEnabled(False)

        self.tableWidget.itemSelectionChanged.connect(self.enableButton)


        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # self.setData()

    def enableButton(self):
        self.btCopy.setEnabled(True)

    # add event filter
    def eventFilter(self, source, event):
        if (event.type() == QtCore.QEvent.KeyPress and
            event.matches(QtWidgets.QKeySequence.Copy)):
            self.copySelection()
            return True
        return super(TableStatsUI, self).eventFilter(source, event)

    # add copy method
    def copySelection(self):
        selection = self.tableWidget.selectedIndexes()
        if selection:
            rows = sorted(index.row() for index in selection)
            columns = sorted(index.column() for index in selection)
            rowcount = rows[-1] - rows[0] + 1
            colcount = columns[-1] - columns[0] + 1
            table = [[''] * colcount for _ in range(rowcount)]
            for index in selection:
                row = index.row() - rows[0]
                column = index.column() - columns[0]
                table[row][column] = index.data()
            stream = io.StringIO()
            csv.writer(stream, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL).writerows(table)
            QtWidgets.qApp.clipboard().setText(stream.getvalue())
