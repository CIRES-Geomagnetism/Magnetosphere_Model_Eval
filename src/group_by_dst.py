import math
import os
import shutil
import numpy as np

import src.utils

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

def group_Mmodel(inp_filename, out_folder, location, break_time="202301"):

    remove_folder(os.path.join(out_folder, location))

    with open(inp_filename, "r") as inp:
        
        for line in inp:
            vals = line.split()
            
            if vals[0] == "#":
                continue
            elif vals[0][:6] == break_time:
                break
            else:
                date = str(vals[0]) + " " + str(vals[1])
                x = vals[2]
                y = vals[3]
                z = vals[4]
                xm = vals[5]
                ym = vals[6]
                zm = vals[7]
                dst = vals[8]

                if math.isnan(float(dst)):
                    continue

                out_name = output_path(dst, location, out_folder)


                if not os.path.isfile(out_name):
                    try:
                        file = open(out_name, "w")
                        file.write("date,Bx,By,Bz,Mx,My,Mz,dst\n")
                    except:
                        print(date)
                else:
                    file = open(out_name, "a")
                file.write(f"{date},{x},{y},{z},{xm},{ym},{zm},{dst}\n")

def read_trueNewModel_results(filename):

    date, x, y, z, x_m, y_m, z_m = [], [], [], [], [], [], []

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

    x = np.array(x, dtype=float)
    y = np.array(y, dtype=float)
    z = np.array(z, dtype=float)
    x_m = np.array(x_m, dtype=float)
    y_m = np.array(y_m, dtype=float)
    z_m = np.array(z_m, dtype=float)

    return date, x, y, z, x_m, y_m, z_m


def dst_vs_rmse(out_folder_path, location, key, file_dict, dst_group, res_filename):

    inp_filename = os.path.join(out_folder_path, location, file_dict[key])
    print(inp_filename)

    date, x, y, z, x_m, y_m, z_m = read_trueNewModel_results(inp_filename)
    rmse_x = src.utils.RMSE(x, x_m)
    rmse_y = src.utils.RMSE(y, y_m)
    rmse_z = src.utils.RMSE(z, z_m)

    min_dst = dst_group[key]

    if min_dst == -1*np.inf:
        min_dst = "-inf"
        max_dst = -300
    elif min_dst == 50:

        max_dst = "inf"
    else:
        max_dst = min_dst + 50

    with open(res_filename, "a") as fp:
        print(f"{rmse_x},{rmse_y},{rmse_z}\n")
        fp.write(f"{min_dst},{max_dst},{rmse_x},{rmse_y},{rmse_z}\n")



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

def write_results_file(out_folder_path, location):

    file_dict = setup_dstgroup_dict()
    dst_group = setup_dstgroup_num()

    res_filename = os.path.join(out_folder_path, location, "dst_rmse.csv")

    with open(res_filename, "w") as fp:

        fp.write("min_dst,max_dst,BX_RMSE,BY_RMSE,BZ_RMSE\n")

        for key, filename in file_dict.items():
            print(dst_group[key])
            dst_vs_rmse(out_folder_path, location, key, file_dict, dst_group, res_filename)












