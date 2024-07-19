import math
import os
import shutil

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
        out_name = f"{file_path}/data_model_p50_0.csv"
    elif 0 <= dst < 50:
        out_name = f"{file_path}/data_model_p0_50.csv"
    elif 50 <= dst < 100:
        out_name = f"{file_path}/data_model_p50_100.csv"
    elif dst >= 100: 
        out_name = f"{file_path}/data_model_p100_inf.csv"

    return out_name      

def group(inp_filename, out_folder, location, break_time="202301"):

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

