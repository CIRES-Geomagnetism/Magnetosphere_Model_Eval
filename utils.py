import numpy as np
import math
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt

def get_PommeMag_arrays(filename): 
   
    x, y, z = [], [], []
    has_nan_value = False 
    with open(filename, "r") as fp:
        
        for i, line in enumerate(fp):
            row = line.split(",")
            if i == 0:
                continue
            else: 
                x.append(row[7])
                y.append(row[8])
                z.append(row[9])
   
    x = np.array(x, dtype = float)    
    y = np.array(y, dtype = float)
    z = np.array(z, dtype = float)
              
    return x, y, z


def RMS(arr):
    
    sqrarr = arr*arr
    mean_sqrarr = np.nanmean(sqrarr)

    return np.sqrt(mean_sqrarr)

def RMSE(true, pred):

    sqr_mean = 0
    N = len(pred)
    
    diff = (true - pred)**2
    sqr_mean = np.nanmean(diff)

    rmse = np.sqrt(sqr_mean)
    
    return rmse

def get_std_index(filename, top_number):
    
    std_row = []
    
    with open(filename, "r") as fp:
        
        for i, line in enumerate(fp):
            row = line.split(",")
            if i == 0:
                continue
            else:
                std_row.append([float(row[6]),i])
    std_row = sorted(std_row)
    
    
    return std_row[-top_number:]

def not_nan_MutualMask(array1, array2):
    
    arr1 = np.ma.masked_invalid(array1)
    arr2 = np.ma.masked_invalid(array2)

    msk = (~arr1.mask & ~arr2.mask)
    
    return msk    


def get_NewTrue_results(filename, start_time_obj, end_time_obj):

    date, x, y, z, x_m, y_m, z_m = [], [], [], [], [], [], [] 
    collect = 0

    time_format = "%Y%m%d %H:%M"
    start_time = start_time_obj.strftime(time_format)
    end_time = end_time_obj.strftime(time_format)
    
    with open(filename, "r") as fp:
        
        for line in fp:
            row = line.split()
            if row[0] == "#":
                continue
            else:
                date_str = str(row[0]) + " " + str(row[1])
                if date_str == start_time or collect == 1: 
                    date.append(str(row[0]) + " " + str(row[1]))
                    x.append(row[2])
                    y.append(row[3])
                    z.append(row[4])
                    x_m.append(row[5])
                    y_m.append(row[6])
                    z_m.append(row[7])
                
                    collect = 1
                if date_str == end_time:
                    break
    
    x = np.array(x, dtype = float)    
    y = np.array(y, dtype = float)
    z = np.array(z, dtype = float)
    x_m = np.array(x_m, dtype = float)    
    y_m = np.array(y_m, dtype = float)
    z_m = np.array(z_m, dtype = float)
    
    return date, x, y, z, x_m, y_m, z_m

def to_datetime(dates):
    
    new_dates = []
    fmt = "%Y%m%d %H:%M"

    for date in dates:
        new_dates.append(dt.datetime.strptime(date, fmt))
    
    return new_dates

def check_folder(folder_path):

	if not os.path.isdir(folder_path):
		os.mkdir(folder_path)

def plot_results(dates, true, preds, labels, elm_name, start_time, end_time, plot_folder_path, time_tag, location):

    check_folder(plot_folder_path)
    dates_dt = to_datetime(dates)
    
    fig, ax = plt.subplots()
    
    ax.set_title(f"{elm_name} prediction at {location} from {start_time} to {end_time}")   
    myFmt = mdates.DateFormatter('%Y%m%d %H:%M')  

    ax.plot(dates_dt, true, label="True", linewidth = 0.8)

    for i in range(len(preds)):
        res = preds[i]
        rmse = RMSE(true, res)
        ax.plot(dates_dt, res, label=labels[i], linewidth=0.5)                    
        ax.format_xdata = mdates.DateFormatter(myFmt)
        plt.text(0.25,0.1+0.1*i,f"RMSE of {labels[i]}: {round(rmse,2)}", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
    plt.xticks(rotation=45)         
    plt.legend(loc = "upper right")

    check_folder(plot_folder_path)
    plt.savefig(f"{plot_folder_path}/{elm_name}_{location}_{time_tag}.png")

    plt.show() 

def get_starttime(filename):

    start_time = ""
    time_format = "%Y-%m-%d %H:%M"	
    with open(filename, "r") as fp:
	    for i, line in enumerate(fp):
		    row = line.split(",")
		    if i == 0:
			    continue
		    else:
			    			    
			    start_time = row[0]  
			    break
    dt_obj = dt.datetime.strptime(start_time[:-3], time_format)
    	
    return dt_obj

def get_endtime(filename):

    time_format = "%Y-%m-%d %H:%M"
    with open(filename, 'rb') as f:
	    try:  # catch OSError in case of a one line file 
		    f.seek(-2, os.SEEK_END)
		    while f.read(1) != b'\n':
			    f.seek(-2, os.SEEK_CUR)
	    except OSError:
		    f.seek(0)
	    last_line = f.readline().decode()
    res = last_line.split(",")

    dt_obj = dt.datetime.strptime(res[0][:-3], time_format)
    return dt_obj

def rmse_results(writer, location, x, y, z, x_p, y_p, z_p, x_n, y_n, z_n):

    rmse_px = round(RMSE(x, x_p), 2)
    rmse_nx = round(RMSE(x, x_n), 2)
       
    rmse_py = round(RMSE(y, y_p), 2)
    rmse_ny = round(RMSE(y, y_n), 2)
     
    rmse_pz = round(RMSE(z, z_p), 2)
    rmse_nz = round(RMSE(z, z_n), 2)

    writer.write(f"{location},{rmse_nx},{rmse_px},{rmse_ny},{rmse_py},{rmse_nz},{rmse_pz}\n")        

def rms_results(writer, location, x, y, z, x_p, y_p, z_p, x_n, y_n, z_n):

    rms_x = round(RMS(x), 2)
    rms_px = round(RMS(x_p), 2)
    rms_nx = round(RMS(x_n), 2)
    
    rms_y = round(RMS(y), 2)    
    rms_py = round(RMS(y_p), 2)
    rms_ny = round(RMS(y_n), 2)
     
    rms_z = round(RMS(z), 2) 
    rms_pz = round(RMS(z_p), 2)
    rms_nz = round(RMS(z_n), 2)

    writer.write(f"{location},{rms_x},{rms_nx},{rms_px},{rms_y},{rms_ny},{rms_py},{rms_z},{rms_nz},{rms_pz}\n")        
                       
def write_outputs(time_tag, newModel_path, pom_path, start_time, end_time, stat):
    
    if stat == "rmse":
        res_filename = f"results/global_RMSE_{time_tag}.txt"
    else:
        res_filename = f"results/global_RMS_{time_tag}.txt"
 
    res_fp = open(res_filename, "w")
    res_fp.write("location,Bx_true,Bx_new,Bx_pom,By_true,By_new,By_pom,Bz_true,Bz_new,Bz_pom\n")
    
     
    files = os.listdir(pom_path)
 
    for location in files:
        if len(str(location)) > 3:
            continue
        pomme_outs = os.path.join(pom_path, location, f"pomme_cloud_results_{time_tag}.txt")
        nm_filename = os.path.join(newModel_path, f"Data_vs_Model_{location}_19970101_20221231_wGSM.txt")    
        print(location)
        with open(nm_filename, "r") as fp:
            x_p, y_p, z_p = get_PommeMag_arrays(pomme_outs)
            date, x, y, z, x_n, y_n, z_n = get_NewTrue_results(nm_filename, start_time, end_time)
            if stat == "rmse":
                rmse_results(res_fp, location, x, y, z, x_p, y_p, z_p, x_n, y_n, z_n)
            else:
                rms_results(res_fp, location, x, y, z, x_p, y_p, z_p, x_n, y_n, z_n)
                         
    res_fp.close()

def stat_results_by_hours(dates, trues, preds, elm_name, labels, num_hours, folder):

    check_folder(folder)
    
    M = len(preds[0])
    filename = f"{folder}/{elm_name}_{dates[0][:8]}_{dates[-1][:8]}.csv"

    with open(filename, 'w') as file:
        j = 0
        file.write(f"start_idx,end_idx,start_time,end_time,max_{elm_name},min_{elm_name},std,NewModel_rmse,PomExt_rmse,PomSM_rmse,corr_coef:new, corr_coef:pm_ext, corr_coef:pm_sm\n")
        while j < M:

            if j + num_hours < M - num_hours:
                period = dates[j:j+num_hours]
                true = trues[j:j+num_hours]
                res_n = preds[0][j:j+num_hours]
                res_e = preds[1][j:j+num_hours]
                res_m = preds[2][j:j+num_hours]
            
            else:
                period = dates[j:]
                true = trues[j:]
                res_n = preds[0][j:]
                res_e = preds[1][j:]
                res_m = preds[2][j:]
                j = M
           
            file.write(f"{j},{j+num_hours-1},{period[0]},{period[-1]},{max(true)},{min(true)},{round(np.std(true),2)},")
            
           
            rmse_n = round(RMSE(true, res_n),2)
            rmse_e = round(RMSE(true, res_e),2)
            rmse_m = round(RMSE(true, res_m),2)
            
            msk = not_nan_MutualMask(res_n, true) 
            coef_nt = round(np.corrcoef(res_n[msk], true[msk])[0,1],3)
            msk = not_nan_MutualMask(res_e, true)
            coef_et = round(np.corrcoef(res_e[msk], true[msk])[0,1],3)
            msk = not_nan_MutualMask(res_m, true)
            coef_mt = round(np.corrcoef(res_m[msk], true[msk])[0,1],3)

            file.write(f"{rmse_n},{rmse_e},{rmse_m},{coef_nt},{coef_et},{coef_mt}\n")
            j += num_hours
            
            
          
        


    #plt.show()
      
def plot_region(pom_path, newModel_path, location, plot_folder, time_tag, start_time, end_time):

    pomme_outs = os.path.join(pom_path, location, f"pomme_cloud_results_{time_tag}.txt")
       

    x_p, y_p, z_p = get_PommeMag_arrays(pomme_outs)
    nm_filename = os.path.join(newModel_path, f"Data_vs_Model_{location}_19970101_20221231_wGSM.txt")    
    date, x, y, z, x_n, y_n, z_n = get_NewTrue_results(nm_filename, start_time, end_time)
            

    labels = ["New Model", "Pomme"]
    preds_x = [x_n, x_p]
    preds_y = [y_n, y_p]
    preds_z = [z_n, z_p]


    plot_results(date, x, preds_x, labels, "Bx", start_time, end_time, plot_folder, time_tag, location)
    plot_results(date, y, preds_y, labels, "By", start_time, end_time, plot_folder, time_tag, location)
    plot_results(date, z, preds_z, labels, "Bz", start_time, end_time, plot_folder, time_tag, location)
   
