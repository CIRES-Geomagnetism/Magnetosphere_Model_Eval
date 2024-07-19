import verify_outputs as vo
import numpy as np
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from datetime import datetime
def plot_sub_result(elm_name, folder, dates, trues, preds, labels, top_number):

    filename = f"{folder}/{elm_name}_{dates[0][:8]}_{dates[-1][:8]}.csv"
    std_idx_set = vo.get_std_index(filename, top_number)
    idx = 0
    row_idx = []
    
    for std, ix in std_idx_set:
        row_idx.append(ix)

    row_idx = sorted(row_idx)
    dates_forplot = to_datetime(dates)
   
    plot_folder_path = folder + "/plots"
    vo.check_folder(plot_folder_path)
    
    myFmt = mdates.DateFormatter('%Y%m%d %H:%M') 
    
    with open(filename, "r") as fp:
        for i, line in enumerate(fp):
            if idx == top_number:
                break
            row = line.split(",")         
            std_idx = row_idx[idx]

            fig, ax = plt.subplots()
            if i == std_idx:
                
                start, end = int(row[0]), int(row[1])
                
                period = dates_forplot[start:end+1]
                true = trues[start:end+1]                
                ax.set_title(f"{elm_name} prediction from {period[0]} to {period[-1]}")
                
                ax.plot(period, true, label="True", linewidth = 0.8)
                for j in range(len(preds)):
                    res = preds[j][start:end+1]
                    rmse = vo.RMSE(true, res)
                
                    ax.plot(period, res, label=labels[j], linewidth=0.5)
                    ax.format_xdata = mdates.DateFormatter(myFmt)

                    plt.text(0.25,0.1+0.1*j,f"RMSE of {labels[j]}: {round(rmse,2)}", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
                
                plt.xticks(rotation=45)         
                plt.legend(loc = "upper right")
                plt.savefig(f"{plot_folder_path}/{elm_name}_std{idx}.png")
                idx += 1
                        
                
def plot_results(dates, trues, preds, elm_name, labels, num_hours, filename):

    N = len(preds)
    M = len(preds[0])

    with open(filename, 'w') as file:
        j = 0
        while j < M - num_hours:
            fig, ax = plt.subplots()

            period = dates[j:j+num_hours]
            true = trues[j:j+num_hours]
            ax.set_title(f"{elm_name} prediction from {round(period[0],2)} to {round(period[-1],2)}")
        
            ax.plot(period, true, label="True", linewidth = 0.5)      
            for i in range(N):
                res = preds[i][j:j+num_hours]
                ax.plot(period, res, label=labels[i], linewidth=0.5)
                rmse = vo.RMSE(true, res)
                plt.text(0.25,0.1,f"RMSE of {labels[i]} is: {round(rmse,3)}", horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        plt.legend(loc = "upper right")
        plt.savefig(f"results/years/{elm_name}_{period[0]}_{period[-1]}.png")
        j += 8760
          
        


    #plt.show()

def to_datetime(dates):
    
    new_dates = []
    fmt = "%Y%m%d %H:%M"

    for date in dates:
        new_dates.append(datetime.strptime(date, fmt))
    
    return new_dates
    
    

def main():
    
    nm_filename = "Data_vs_Model_HON_19970101_20221231.txt"
    pomme_ext_filename = "pomme_calc_ext_results.txt"
    pomme_sm_filename = "pomme_calc_sm_results.txt"
    res_folder = "results/monthly"
    top_number = 10

   
    
    date, x, y, z, x_n, y_n, z_n = vo.get_NewTrueMag_arrays(nm_filename)
    x_e, y_e, z_e = vo.get_PommeMag_arrays(pomme_ext_filename)
    #x_m, y_m, z_m = vo.get_PommeMag_arrays(pomme_sm_filename)
    
    M = min(len(x_e), len(x))
    print(M)
    
    x, y, z = x[:M], y[:M], z[:M]
    x_n, y_n, z_n = x_n[:M], y_n[:M], z_n[:M]
    x_e, y_e, z_e = x_e[:M], y_e[:M], z_e[:M]
    #x_m, y_m, z_m = x_m[:M], y_m[:M], z_m[:M]
    date = date[:M]
    
    preds_Bx = [x_n, x_e]
    preds_By = [y_n, y_e]
    preds_Bz = [z_n, z_e] 
    labels = ["New Model", "Pomme_ext"]
    num_hours = 2160
    
   
    plot_sub_result("Bx", res_folder, date, x, preds_Bx, labels, top_number)
    plot_sub_result("By", res_folder, date, y, preds_By, labels, top_number) 
    plot_sub_result("Bz", res_folder, date, z, preds_Bz, labels, top_number)  
if __name__=="__main__":
    
    main()
