import csv
import os
import time


class saveReportToFileClass:

    def __init__(self, values, path, key):

        self.values = values
        self.path = path


        self.timestr = time.strftime("%Y%m%d-%H%M%S")

        #if patches is not None:
        #    self.patches = patches   #posiblemente en desuso

        if key == "CIE76" or key == "CIE00" or key == "CIE94" or key == "CMC" or key == "DEC" or key == "DEH" or key == "DEL":

            o = self.save_deltae_color(key)
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "OECF" or key == "GREEN" or key == "BLUE" or key == "RED":

            o = self.save_oecf()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "LGAIN":

            o = self.save_lgain()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "RGB":

            o = self.save_rgb()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)


        elif key == "DEV":

            o = self.save_delta_ev()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "SNR" or key == "RDEV":

            o = self.save_snr(key)
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "SNR-RGB":

            o = self.save_snr_rgb()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "C_NOISE":

            o = self.save_croma_noise()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "NPS_RGB_X" or key == "NPS_RGB_Y":

            o = self.save_nps_rgb()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "HISTO":

            o = self.save_histo()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "MTF" or key == "LSF" or key == "ESF":

            o = self.save_mtf(key)
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "CIE76_MULTI" or key == "CIE00_MULTI" or key == "CMC_MULTI":

            o = self.save_deltae_color_multiple()
            path = os.path.join(str(self.path), key + "_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "DEV_MULTI":

            o = self.save_delta_ev_multiple()
            path = os.path.join(str(self.path), "DEV_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "SNR_MULTI":

            o = self.save_snr_multiple()
            path = os.path.join(str(self.path), "SNR_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "OECF_MULTI":

            o = self.save_oecf_multiple()
            path = os.path.join(str(self.path), "OECF_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "SENSITOMETRY_MULTI":

            o = self.save_sensitometry()
            path = os.path.join(str(self.path), "SENSITOMETRY_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

        elif key == "MTF_MULTI":

            o = self.save_mtf_multiple()
            path = os.path.join(str(self.path), "MTF_" + self.timestr + ".txt")
            self.save_to_csv(path, o)

    def save_deltae_color(self,key):
        # [[A01,A02, ....,D06 ],[ mean, max, min, desv]]
        # [[10.175514728995289, 9.546067253062903, 6.525296928109862, 16.395734201309804, 6.1793931740908015, 18.146277855251746, 20.179365698653662, 12.269396888192999, 11.538422769165637, 14.562589055521686, 30.095032812741707, 24.781295365658348, 18.448663908261754, 25.28281234356653, 15.775195719863511, 32.079136522044976, 17.12263998336705, 17.74225464815563, 5.498008730440508, 8.148275891254546, 8.945999105745535, 9.477710694044209, 7.937537401486682, 6.616955493276347], [14.73, 32.08, 5.5, 7.44]]

        i = 0

        if key == "CIE76" or key == "CIE00" or key == "CMC" or key == "CIE94":

            o = [["Patch","L_ref","a_ref","b_ref","L_sample","a_sample","b_sample", "Delta"]]

            for x in self.values["curve"]:
                o.append([self.values["x_axis"][i],
                          str(self.values["colorOrig"][i][0]),str(self.values["colorOrig"][i][1]),str(self.values["colorOrig"][i][2]),
                          str(self.values["colorDest"][i][0]), str(self.values["colorDest"][i][1]),str(self.values["colorDest"][i][2]),
                          str(round(x, 2))])
                i = i + 1

        elif key == "DEC":

            o = [["Patch", "C_ref", "C_sample", "DeltaC"]]

            for x in self.values["curve"]:
                o.append([self.values["x_axis"][i],
                          str(self.values["colorOrig"][i]),
                          str(self.values["colorDest"][i]),
                          str(round(x, 2))])
                i = i + 1

        elif key == "DEH":

            o = [["Patch", "H_ref", "H_sample", "DeltaH"]]

            for x in self.values["curve"]:
                o.append([self.values["x_axis"][i],
                          str(self.values["colorOrig"][i]),
                          str(self.values["colorDest"][i]),
                          str(round(x, 2))])
                i = i + 1

        elif key == "DEL":

            o = [["Patch", "L_ref", "L_sample", "DeltaL"]]

            for x in self.values["curve"]:
                o.append([self.values["x_axis"][i],
                          str(self.values["colorOrig"][i]),
                          str(self.values["colorDest"][i]),
                          str(round(x, 2))])
                i = i + 1


        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value)])


        return o

    def save_oecf(self):

        # [[[[ sample, reference ],[ sample, reference ],.... ], {'Err Min': '00', 'Err Average': '00', 'Err Max': '00', 'Err Desv': 00}]]
        # [[[[92.0, 96.0], [72.0, 79.0], [56.0, 64.0], [39.0, 47.0], [26.0, 33.0], [13.0, 19.0]], {'Err Min': '4.0', 'Err Average': '6.67', 'Err Max': '8.0', 'Err Desv': 1.0}]]

        i = 0

        o = [["Density", "Sample", "Reference"]]

        for x in self.values["curve"]:
            o.append([str(self.values["x_axis"][i]), str(round(x[0], 2)), str(round(x[1], 2))])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value)])

        return o

    def save_lgain(self):

        i = 0

        o = [["Density", "L_GAIN"]]

        for x in self.values["curve"]:
            o.append([str(self.values["x_axis"][i]), str(round(x, 2))])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value)])

        return o

    def save_rgb(self):

        # [[[[236.1, 234.0, 239.3], [186.8, 183.45, 192.97], [143.51, 141.96, 149.76], [100.23, 98.7, 104.52], [66.06, 65.8, 70.57], [34.95, 33.99, 36.87]], {'Err Min': '1.2', 'Err Average': '2.56', 'Err Max': '3.94', 'Err Desv': 1.0}]]

        i = 0
        o = [["Density", "Red", "Green", "Blue"]]
        # tf.write(head+'\n')

        for x in self.values["curve"]:
            o.append([str(self.values["x_axis"][i]), str(int(x[0])), str(int(x[1])), str(int(x[2]))])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value)])

        return o


    def save_croma_noise(self):

        # [[[[236.1, 234.0, 239.3], [186.8, 183.45, 192.97], [143.51, 141.96, 149.76], [100.23, 98.7, 104.52], [66.06, 65.8, 70.57], [34.95, 33.99, 36.87]], {'Err Min': '1.2', 'Err Average': '2.56', 'Err Max': '3.94', 'Err Desv': 1.0}]]

        i = 0

        o = [["X", "Red", ]]

        for x in self.values["curve"]:

            o.append([str(self.values["x_axis"][i]), str(float(x)) ])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):

            o.append([key, str(value[0]) + " " + str(value[1])])

        return o

    def save_snr_rgb(self):

        # [[[[236.1, 234.0, 239.3], [186.8, 183.45, 192.97], [143.51, 141.96, 149.76], [100.23, 98.7, 104.52], [66.06, 65.8, 70.57], [34.95, 33.99, 36.87]], {'Err Min': '1.2', 'Err Average': '2.56', 'Err Max': '3.94', 'Err Desv': 1.0}]]

        i = 0

        o = [["X", "Red", "Green", "Blue"]]

        for x in self.values["curve"]:
            o.append([str(self.values["x_axis"][i]), str(int(x[0])), str(int(x[1])), str(int(x[2]))])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):

            o.append([key, str(value[0]) + " " + str(value[1])])

        return o

    def save_histo(self):

        i = 0
        totalChn = len(self.values["curve"])

        if totalChn == 3:
            o = [["X", "Red", "Green", "Blue"]]
        elif totalChn == 1:
            o = [["X", "Luma"]]

        total = len(self.values["x_axis"])

        for x in range(total):

            if totalChn == 3:
                o.append([str(self.values["x_axis"][i]), str(float(self.values["curve"][0][i])),
                          str(float(self.values["curve"][1][i])), str(float(self.values["curve"][2][i]))])
            elif totalChn == 1:
                o.append([str(self.values["x_axis"][i]), str(float(self.values["curve"][0][i]))])

            i = i + 1

        return o

    def save_nps_rgb(self):

        i = 0
        totalChn = len(self.values["curve"][0])

        if totalChn == 3:
            o = [["X", "Red", "Green", "Blue"]]
        elif totalChn > 3:
            o = [["X", "Luma"]]

        total = len(self.values["x_axis"])

        for x in range(total):

            if totalChn == 3:
                o.append( [str(self.values["x_axis"][i]), str(float(self.values["curve"][0][0][i])), str(float(self.values["curve"][0][1][i])), str(float(self.values["curve"][0][2][i]))]      )
            elif totalChn > 3:
                o.append( [str(self.values["x_axis"][i]), str(float(self.values["curve"][0][i])) ] )

            i = i + 1

        return o

    def save_delta_ev(self):

        # [[[-0.06076036545392528, -0.12553088208385946, -0.18632134097921205, -0.2848811081320429, -0.33839640574312607, -0.5133144596125951], {'Err Min': '-0.51', 'Err Average': '-0.25', 'Err Max': '-0.06', 'Err Desv': 0.0}]]

        i = 0

        o = [["Density", "De"]]

        for x in self.values["curve"]:
            # line = self.patches[i]+";"+str(round(x,2))
            o.append([str(self.values["x_axis"][i]), str(round(x, 2))])
            # tf.write(line+'\n')
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value)])
            # tf.write(key+": "+str(value)+'\n')
        return o




    def save_snr(self, key):

        # [[[105.89903777448205, 109.31752174785206, 105.7638850825043, 99.6386900492993, 87.01634009129585, 76.26421863860946], {'Min': '76.26db', 'Average': '97.32db', 'Max': '109.32db', 'Desv': '11.86db'}]]
        i = 0
        o = [["EV", key]]

        for x in self.values["curve"]:
            o.append([str(self.values["x_axis"][i]), str(round(x, 2))])
            i = i + 1

        for key, value in sorted(self.values["stats"].items()):
            o.append([key, str(value[0])+" "+str(value[1])])
        return o


    def save_mtf(self, index):

        xscale = []
        #curveraw = []
        curvesmoot = []
        MTF50 = None
        LPmm = None
        LW_PH = None
        LPH = None

        if index == "MTF":
            xscale = self.values["GRAY"]["x_mtf_final"]
        if index == "ESF" or index == "LSF":
            xscale = self.values["GRAY"]["xesf"]

        metrics = ["MTF50", "MTF30", "MTF10"]

        #h = [ "CH","MTF50", "LP/mm", "LW/PH", "LP/PH"]

        h = ["CH"]

        if index == "MTF":
            for head in metrics:
                h.append( head  )
                h.append("% (" + head + ")")
                h.append( "Sensor Lp/mm ("+head+")" )
                h.append( "LW/PH ("+head+")" )
                h.append( "LP/PH("+head+")" )

                h.append("Img Nyquist Lp/mm (" + head + ")")
                h.append("Img Lp/mm (" + head + ")")
                h.append("Img Lp/mm % (" + head + ")")

        if index == "ESF":
            h.append("CA pixel")
            h.append("RISE pixel")
            #h.append("Rise GREEN pixel")
            #h.append("Rise BLUE pixel")
            #h.append("Rise GRAY pixel")

        for p in range(len(xscale)):
            h.append(str(xscale[p]))

        o = [h]

        for key in self.values:
            p = []
            if key is not "INFO":
                p.append(str(key))

                if index == "MTF":
                    curvesmoot = self.values[key]["mtf_final"]

                    for metric in metrics:

                        p.append(str(self.values[key][metric]['MTF']))
                        p.append(str(self.values[key][metric]['MTFpercent']))
                        p.append(str(self.values[key][metric]['LPmm']))
                        p.append(str(self.values[key][metric]['LW_PH']))
                        p.append(str(self.values[key][metric]['LPH']))

                        p.append(str(self.values[key][metric]['lpNyquist']))
                        p.append(str(self.values[key][metric]['imgLPmm']))
                        p.append(str(self.values[key][metric]['lpPercent']))

                if index == "ESF":

                    #xscale = self.values[key]["xesf"]
                    #curveraw = self.values[key]["esf"]
                    if "esf_smooth" in self.values[key]:
                        curvesmoot = self.values[key]["esf_smooth"]

                    p.append(str(self.values["INFO"]['CA']))

                    p.append(str(self.values["INFO"]['RAISE_'+key]))
                    #p.append(str(self.values["INFO"]['RAISE_GREEN']))
                    #p.append(str(self.values["INFO"]['RAISE_BLUE']))
                    #p.append(str(self.values["INFO"]['RAISE_GRAY']))


                if index == "LSF":
                    curveraw = self.values[key]["lsf"]
                    curvesmoot = self.values[key]["lsf_smooth"]

                for x in curvesmoot:
                    p.append(str(x))

                o.append(p)

        #print(o)


        return o


    def save_deltae_color_multiple(self):
        # [('filename', De mean), ('filename', De mean)]
        # [('DSC_0205.jpg', 26.03), ('DSC_0205.tif', 14.75)]

        o = [["Filename", "delta"]]
        for x in self.values:
            o.append([x[0], str(x[1])])

        return o

    def save_delta_ev_multiple(self):  ### no esta en uso

        # [('filename', [white, grey, black]), ....]
        # [('DSC_0205.jpg', [-0.9462287435590191, -1.1732048717089165, -1.158219500790033]), ('DSC_0205.tif', [-0.06506783945196473, -0.2863332421659552, -0.5049509866779681])]

        h = ["Filename", "White", "MiddleGrey", "Black"]
        o = []
        o.append(h)
        for x in self.values:
            # line = x[0]+";"+str(x[1][0])+";"+str(x[1][1])+";"+str(x[1][2])
            o.append([x[0], str(x[1][0]), str(x[1][1]), str(x[1][2])])
            # tf.write(line+'\n')

        return o

    def save_oecf_multiple(self):
        # [{'File': 'DSC_4115.TIF', 'shutter': '1/25', 'aperture': '2.5', 'iso': '50', 'curve': [[92.0, 96.0], [76.0, 79.0], [61.0, 64.0], [46.0, 47.0], [34.0, 33.0], [22.0, 19.0]], 'stats': {'units': '%', 'Err Avg': '2.5', 'Err Max': '4.0', 'Err Min': '1.0', 'Err Desv': '1.12'}}, {'File': 'DSC_4116.TIF', 'shutter': '1/30', 'aperture': '2.8', 'iso': '64', 'curve': [[91.0, 96.0], [75.0, 79.0], [61.0, 64.0], [46.0, 47.0], [34.0, 33.0], [22.0, 19.0]], 'stats': {'units': '%', 'Err Avg': '2.83', 'Err Max': '5.0', 'Err Min': '1.0', 'Err Desv': '1.46'}}]

        h = []
        h.append("Filename")
        h.append("Shutter")
        h.append("Aperture")
        h.append("ISO")


        for z in self.values[0]["x_axis"]:
            # head = head + ";GS"+str(z+1)
            h.append("OD_" + str(z ))

        h.append("Units")
        h.append("ErrMin")
        h.append("ErrAverage")
        h.append("ErrMax")
        h.append("ErrDesv")

        i = 0
        o = []

        ref = []

        o.append(h)

        for x in self.values:
            z = []
            # line = str(x[0])
            z.append(str(x["File"]))
            z.append(str(x["shutter"]))
            z.append(str(x["aperture"]))
            z.append(str(x["iso"]))

            ref = []
            for y in x["curve"]:
                # line = line +";"+str( y[0] );
                z.append(str(y[0]))
                ref.append(y[1])

            for k, v in x["stats"].items():
                # line = line +";"+str( v );
                z.append(v)

            # tf.write(line+'\n')
            o.append(z)
            i = i + 1

        r = []
        r.append("Reference")
        r.append("NA")
        r.append("NA")
        r.append("NA")
        for re in ref:
            # r = r +";"+str(re)
            r.append(str(re))

        o.append(r)

        return o

    def save_snr_multiple(self):

        # {'File': 'DSC_4115.TIF', 'ISO': '50', 'curve': [48.04091236476219, 49.132763958979105, 45.808161400024865, 43.80176719047952, 41.792386871632985, 35.46662970108684], 'stats': {'Average': ['44.01', 'db'], 'Max': ['49.13', 'db'], 'Min': ['35.47', 'db'], 'Desv': ['4.54', 'db'], 'EV': ['7.33', 'EV'], 'Contrast': ['161:1', '']}}
        o = []
        h = []

        h.append("Filename")
        h.append("ISO")

        for z in range(len(self.values[0]["curve"])):
            # head = head + ";GS"+str(z+1)
            h.append(str(self.values[0]["x_axis"][z]))

        h.append("Average")
        h.append("Max")
        h.append("Min")
        h.append("Desv")
        h.append("EV")
        h.append("Contrast")

        o.append(h)
        # i = 0
        for x in self.values:

            z = []
            z.append(x["File"])
            z.append(x["ISO"])

            for y in x["curve"]:
                z.append(str(int(y)))

            for k, v in x["stats"].items():
                z.append(str(v[0])+" "+str(v[1]))

            o.append(z)

        return o

    def save_sensitometry(self):

        # [(('1/125', '9', '200', 'DSC_0205.jpg'), [60.0, 50.0, 40.0]), (('1/125', '9', '200', 'DSC_0205.tif'), [93.0, 75.0, 59.0])]

        o = []
        o.append(["Filename", "Shutter", "Aperture", "ISO", "White", "MiddleGrey", "Black"])
        for x in self.values:
            # line = x[0][3]+";"+x[0][0]+";"+x[0][1]+";"+str(x[0][2])+";"+str(x[1][0])+";"+str(x[1][1])+";"+str(x[1][2])
            o.append([x[0][3], x[0][0], x[0][1], str(x[0][2]), str(x[1][0]), str(x[1][1]), str(x[1][2])])

        return o

    def save_mtf_multiple(self):


        a = []
        b = []
        b1 = []
        b2 = []
        b3 = []

        metrics = ["MTF50", "MTF30", "MTF10"]

        h = ["filename", "shutter", "aperture", "ISO"]

        for head in metrics:
            h.append(head)
            h.append("% (" + head + ")")
            h.append("LP/mm (" + head + ")")
            h.append("LW/PH (" + head + ")")
            h.append("LP/PH (" + head + ")")

            h.append("Image Nyquist Lp/mm (" + head + ")")
            h.append("Image Lp/mm (" + head + ")")
            h.append("Image Lp/mm % (" + head + ")")

        #for p in range(127):
        #    h.append(str(p))
        #print(self.values[0]['x_mtf_final'])

        for p in self.values[0]['x_mtf_final']:
            h.append(str(p))
        o = [h]

        derivadas = {}
        for metric in metrics:
            derivadas[metric] = []

            derivadas[metric + 'MTFpercent'] = []
            derivadas[metric + 'LPmm'] = []
            derivadas[metric + 'LW_PH'] = []
            derivadas[metric + 'LPH'] = []

            derivadas[metric + 'lpNyquist'] = []
            derivadas[metric + 'imgLPmm'] = []
            derivadas[metric + 'lpPercent'] = []

        for value in self.values:

            b.append(value['filename'])
            b1.append(value['shutter'])
            b2.append(value['aperture'])
            b3.append(value['iso'])

            for metric in metrics:

                derivadas[metric].append(value[metric])
                derivadas[metric + 'MTFpercent'].append(value[metric + 'MTFpercent'])
                derivadas[metric+'LPmm'].append(value[metric+'LPmm'])
                derivadas[metric+'LW_PH'].append(value[metric+'LW_PH'])
                derivadas[metric+'LPH'].append(value[metric+'LPH'])
                derivadas[metric+'lpNyquist'].append(value[metric + 'lpNyquist'])
                derivadas[metric+'imgLPmm'].append(value[metric+'imgLPmm'])
                derivadas[metric+'lpPercent'].append(value[metric+'lpPercent'])


            #if value == 0:
                #a.append(value['x_mtf_final'])  # hay que revisar el eje de valores este
            a.append(value['mtf_final'])

        # print( zip(*a) )

        for y in range(len(a)):

            w = [
                b[y],
                str(b1[y]),
                str(b2[y]),
                str(b3[y])]

            for metric in metrics:
                w.append( str(derivadas[metric][y] ))
                w.append( str(derivadas[metric + 'MTFpercent'][y]))
                w.append( str(derivadas[metric+'LPmm'][y]))
                w.append( str(derivadas[metric+'LW_PH'][y]))
                w.append( str(derivadas[metric+'LPH'][y]))

                w.append(str(derivadas[metric + 'lpNyquist'][y]))
                w.append(str(derivadas[metric + 'imgLPmm'][y]))
                w.append(str(derivadas[metric + 'lpPercent'][y]))

            for z in a[y]:
                w.append(str(z))

            o.append(w)

        return o

    def save_to_csv(self, path, data):

        with open(path, mode='w') as data_file:
            writer = csv.writer(data_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            for x in data:
                writer.writerow(x)
