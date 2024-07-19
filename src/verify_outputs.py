import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import utils
def get_NewTrueMag_arrays(filename):

    date, x, y, z, x_m, y_m, z_m = [], [], [], [], [], [], [] 
    with open(filename, "r") as fp:
        
        for line in fp:
            row = line.split()
            if row[0] == "#":
                continue
            else:
                date.append(str(row[0]) + " " + str(row[1]))
                x.append(row[2])
                y.append(row[3])
                z.append(row[4])
                x_m.append(row[5])
                y_m.append(row[6])
                z_m.append(row[7])
    
    x = np.array(x, dtype = float)    
    y = np.array(y, dtype = float)
    z = np.array(z, dtype = float)
    x_m = np.array(x_m, dtype = float)    
    y_m = np.array(y_m, dtype = float)
    z_m = np.array(z_m, dtype = float)
    
    return date, x, y, z, x_m, y_m, z_m


def main():

    newModel_folder= "Martin_text_files_with_GSM_fields"
    newModel_folder_path = os.path.abspath(newModel_folder)

    pom_folder = "results/global"
    pom_folder_path = os.path.join(pom_folder)

    time_tag = "20150623"
    inputs_data = f"inputs/cloud_data_inputs_{time_tag}.txt"
   
    plot_path = os.path.abspath("plots/data_from_cloud_gsm") 
    start_time = utils.get_starttime(inputs_data)
    end_time = utils.get_endtime(inputs_data)
    
    utils.plot_region(pom_folder_path, newModel_folder_path, "HBK", plot_path, time_tag, start_time, end_time) 
    #utils.write_outputs(time_tag, newModel_folder_path, pom_folder_path, start_time, end_time, "rms")
if __name__=="__main__":

    main()
 
