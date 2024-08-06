import math
import os
import shutil
from collections import defaultdict
import matplotlib.pyplot as plt

import numpy as np

import src.utils

class rmse_map:

    def __init__(self, group_dst_number):

        self.group = group_dst_number
        self.xmap = defaultdict(list)
        self.ymap = defaultdict(list)
        self.zmap = defaultdict(list)


    def insert_map(self, min_dst: float, x, y, z):

        N = len(self.group)

        if min_dst < self.group[1]:
            self.xmap[0].append(x)
            self.ymap[0].append(y)
            self.zmap[0].append(z)

        elif min_dst >= self.group[N-1]:
            self.xmap[N-1].append(x)
            self.ymap[N-1].append(y)
            self.zmap[N-1].append(z)
        else:
            for i in range(1, N - 1):
                if self.group[i] <= min_dst < self.group[i+1]:
                    self.xmap[i].append(x)
                    self.ymap[i].append(y)
                    self.zmap[i].append(z)
                    break

    def items_to_numpy_array(self):

        for key in self.xmap.keys():
            self.xmap[key] = np.array(self.xmap[key], dtype=float)
            self.ymap[key] = np.array(self.ymap[key], dtype=float)
            self.zmap[key] = np.array(self.zmap[key], dtype=float)










def remove_past_resfile(file_dict, output_folder, location):

    loc_path = os.path.join(output_folder, location)
    files = os.listdir(loc_path)

    filenames = [name for key, name in file_dict.items()]

    for file in files:

        if file in filenames:
            os.remove(os.path.join(loc_path, file))


def remove_folder(folder_path):
    
    if os.path.isdir(folder_path):
        shutil.rmtree(folder_path)
        os.mkdir(folder_path)

def output_path(dst, location, out_folder):

    dst = float(dst)
    file_path = f"{out_folder}/{location}"
    out_name =""



    if dst < -300: 
        out_name = f"{file_path}/data_model_ninf_300.csv"
    elif -300 <= dst < -250:
        out_name = f"{file_path}/data_model_n300_250.csv"
    elif -250 <= dst < -200:
        out_name = f"{file_path}/data_model_n250_200.csv"
    elif -200 <= dst < -150:
        out_name = f"{file_path}/data_model_n200_150.csv"
    elif -150 <= dst < -100:
        out_name = f"{file_path}/data_model_n150_100.csv"
    elif -100 <= dst < -50:
        out_name = f"{file_path}/data_model_n100_50.csv"
    elif -50 <= dst < 0:
        out_name = f"{file_path}/data_model_n50_0.csv"
    elif 0 <= dst < 50:
        out_name = f"{file_path}/data_model_p0_50.csv"
    elif 50 <= dst :
        out_name = f"{file_path}/data_model_p50_inf.csv"


    return out_name      

def group(inp_filename, out_folder, location, break_time="202301"):

    file_dict = setup_dstgroup_dict()
    remove_past_resfile(file_dict, out_folder, location)

    with open(inp_filename, "r") as inp:
        
        for i, line in enumerate(inp):
            vals = line.split(",")
            
            if i == 0:
                continue
            elif vals[0][:6] == break_time:
                break
            else:
                date = vals[0]
                x = vals[1]
                y = vals[2]
                z = vals[3]
                xm = vals[4]
                ym = vals[5]
                zm = vals[6]
                xp = vals[7]
                yp = vals[8]
                zp = vals[9]
                dst = vals[10]

                if math.isnan(float(dst)):
                    continue

                out_name = output_path(dst, location, out_folder)


                if not os.path.isfile(out_name):
                    try:
                        file = open(out_name, "w")
                        file.write("date,Bx,By,Bz,Mx,My,Mz,Px,Py,Pz,dst\n")
                    except:
                        print(date)
                else:
                    file = open(out_name, "a")
                file.write(f"{date},{x},{y},{z},{xm},{ym},{zm},{xp},{yp},{zp},{dst}")

def read_trueNewModel_results(filename):

    date, x, y, z, x_m, y_m, z_m, x_p, y_p, z_p = [], [], [], [], [], [], [], [], [], []

    with open(filename, "r") as fp:

        for i, line in enumerate(fp):
            if i == 0:
                continue
            else:
                row = line.split(",")


                date.append(row[0])
                x.append(row[1])
                y.append(row[2])
                z.append(row[3])
                x_m.append(row[4])
                y_m.append(row[5])
                z_m.append(row[6])
                x_p.append(row[7])
                y_p.append(row[8])
                z_p.append(row[9])

    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    z = np.array(z, dtype=float)
    x_m = np.array(x_m, dtype=float)
    y_m = np.array(y_m, dtype=float)
    z_m = np.array(z_m, dtype=float)
    x_p = np.array(x_p, dtype=float)
    y_p = np.array(y_p, dtype=float)
    z_p = np.array(z_p, dtype=float)

    return date, x, y, z, x_m, y_m, z_m, x_p, y_p, z_p


def dst_vs_rmse(writter, out_folder_path, location, key, file_dict, dst_group):

    inp_filename = os.path.join(out_folder_path, location, file_dict[key])


    date, x, y, z, x_m, y_m, z_m, x_p, y_p, z_p = read_trueNewModel_results(inp_filename)
    rmse_xm = round(src.utils.RMSE(x, x_m), 6)
    rmse_ym = round(src.utils.RMSE(y, y_m), 6)
    rmse_zm = round(src.utils.RMSE(z, z_m), 6)

    rmse_xp = round(src.utils.RMSE(x, x_p), 6)
    rmse_yp = round(src.utils.RMSE(y, y_p), 6)
    rmse_zp = round(src.utils.RMSE(z, z_p), 6)

    min_dst = dst_group[key]

    if min_dst == -1*np.inf:
        min_dst = "-inf"
        max_dst = -300
    elif min_dst == 50:

        max_dst = "inf"
    else:
        max_dst = min_dst + 50



    writter.write(f"{location},{min_dst},{max_dst},{rmse_xm},{rmse_ym},{rmse_zm},{rmse_xp},{rmse_yp},{rmse_zp}\n")



def setup_dstgroup_dict():

    group = {}

    group[0] = "data_model_ninf_300.csv"
    group[1] = "data_model_n300_250.csv"
    group[2] = "data_model_n250_200.csv"
    group[3] = "data_model_n200_150.csv"
    group[4] = "data_model_n150_100.csv"
    group[5] = "data_model_n100_50.csv"
    group[6] = "data_model_n50_0.csv"
    group[7] = "data_model_p0_50.csv"
    group[8] = "data_model_p50_inf.csv"

    return group

def setup_dstgroup_num():

    arr = [0.0]*9

    arr[0] = -1 * np.inf
    arr[1] = -300.0

    for i in range(2, 9):
        arr[i] = arr[i-1] + 50

    return arr

def write_results_file(out_folder_path, location, writter):

    file_dict = setup_dstgroup_dict()
    dst_group = setup_dstgroup_num()





    for key, filename in file_dict.items():

        dst_vs_rmse(writter, out_folder_path, location, key, file_dict, dst_group)

def attach_three_results(pomme_file, martin_file, out_file):

    with open(martin_file, "r") as m_file, open(pomme_file, "r") as p_file:

        for _ in range(2):
            p_file.readline()
        p_start = p_file.tell()
        p_file.seek(p_start)

        for _ in range(5):
            m_file.readline()
        m_start = m_file.tell()
        m_file.seek(m_start)

        writter = open(out_file,"w")
        writter.write("date,x,y,z,xm,ym,zm,xp,yp,zp,dst\n")

        for line_m, line_p in zip(m_file, p_file):
            res_m = line_m.split()
            res_p = line_p.split(",")


            date = str(res_m[0]) + " " + str(res_m[1])
            x, y, z = res_m[2],  res_m[3],  res_m[4]
            xm, ym, zm = res_m[5],  res_m[6],  res_m[7]
            dst = res_m[8]

            xp, yp, zp = res_p[1], res_p[2], res_p[3]


            writter.write(f"{date},{x},{y},{z},{xm},{ym},{zm},{xp},{yp},{zp},{dst}\n")

def create_loc_map(rmse_file):

    dst_group = setup_dstgroup_num()

    mt_map = rmse_map(dst_group)
    pom_map = rmse_map(dst_group)


    with open(rmse_file, "r") as file:

        for i, line in enumerate(file):

            if i == 0:
                continue

            vals = line.split(",")

            min_dst = vals[1]



            if min_dst == -np.inf:
                min_dst = -99999.0
            elif min_dst == np.inf:
                min_dst = 99999.0
            else:
                min_dst = float(min_dst)

            xm, ym, zm = vals[3], vals[4], vals[5]
            xp, yp, zp = vals[6], vals[7], vals[8]

            mt_map.insert_map(min_dst, xm, ym, zm)
            pom_map.insert_map(min_dst, xp, yp, zp)

    mt_map.items_to_numpy_array()
    pom_map.items_to_numpy_array()

    return mt_map, pom_map

def output_rmsgroup_results(mt_map, pom_map, out_file, dst_group):

    with open(out_file, "w") as file:

        file.write("min_dst, max_dst,rms_XM,rms_YM,rms_ZM,rms_XP,rms_YP,rms_ZP\n")

        for key in mt_map.xmap.keys():

            rms_xm = src.utils.RMS(mt_map.xmap[key])
            rms_ym = src.utils.RMS(mt_map.ymap[key])
            rms_zm = src.utils.RMS(mt_map.zmap[key])

            rms_xp = src.utils.RMS(pom_map.xmap[key])
            rms_yp = src.utils.RMS(pom_map.ymap[key])
            rms_zp = src.utils.RMS(pom_map.zmap[key])

            min_dst = dst_group[key]

            if min_dst == -1 * np.inf:
                min_dst = "-inf"
                max_dst = -300
            elif min_dst == 50:

                max_dst = "inf"
            else:
                max_dst = min_dst + 50

            file.write(f"{min_dst},{max_dst},{rms_xm},{rms_ym},{rms_zm},{rms_xp},{rms_yp},{rms_zp}\n")

def plot_rms(dst, xm, xp, labels, elm):

    xm = np.array(xm, dtype=float)
    xp = np.array(xp, dtype=float)

    plt.title(f"RMS of {elm} RMSE in 15 locations from 19970101 to 20221231")
    plt.plot(dst, xm, 'o-', label=labels[0])
    plt.plot(dst, xp, 'o-', label=labels[1])
    plt.xlabel("DST")
    plt.ylabel("RMS")
    plt.legend(loc="upper right")
    plt.show()


def plot_rms_Allresults(rms_file):


    xm, ym, zm, xp, yp, zp = [], [], [], [], [], []


    dst = np.arange(-325, 125, 50)

    with open(rms_file, "r") as fp:

        for i, line in enumerate(fp):
            vals = line.split(",")

            if i == 0:
                continue

            xm.append(vals[2])
            ym.append(vals[3])
            zm.append(vals[4])

            xp.append(vals[5])
            yp.append(vals[6])
            zp.append(vals[7])

    labels = ["Martin", "Pomme"]

    plot_rms(dst, xm, xp, labels, "Bx")
    plot_rms(dst, ym, yp, labels, "By")
    plot_rms(dst, zm, zp, labels, "Bz")


def plot_rmse(dst, xm, xp, labels, elm, loc, out_dir):

    xm = np.array(xm, dtype=float)
    xp = np.array(xp, dtype=float)

    filename = os.path.join(out_dir, loc, f"{loc}_{elm}_dst_rmse.png")

    plt.title(f"RMSE of {elm} of DST group in {loc} from 19970101 to 20221231")
    plt.plot(dst, xm, 'o-', label=labels[0])
    plt.plot(dst, xp, 'o-', label=labels[1])
    plt.xlabel("DST")
    plt.ylabel("RMSE")
    plt.legend(loc="upper right")
    plt.savefig(filename)
    plt.show()

def plot_dst_rmse(filename, out_dir):




    xm, ym, zm, xp, yp, zp = [], [], [], [], [], []
    dst = np.arange(-325, 125, 50)
    labels = ["Martin", "Pomme"]

    with open(filename, "r") as file:
        for i, line in enumerate(file):

            if i == 0:
                continue

            vals = line.split(",")
            loc = vals[0]
            xm.append(vals[3])
            ym.append(vals[4])
            zm.append(vals[5])

            xp.append(vals[6])
            yp.append(vals[7])
            zp.append(vals[8])

            if i % 9  == 0:

                plot_rmse(dst, xm, xp, labels, "Bx", loc, out_dir)
                plot_rmse(dst, ym, yp, labels, "By", loc, out_dir)
                plot_rmse(dst, zm, zp, labels, "Bz", loc, out_dir)
                xm, ym, zm, xp, yp, zp = [], [], [], [], [], []



















































