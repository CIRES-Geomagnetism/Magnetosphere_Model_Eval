import json
import requests
from datetime import datetime
import verify_outputs as vp

def get_json_data(url)->dict:

    #url = "https://hdgm-rt-test.appspot.com/?lat1=21.19&lon1=-158&altitude=0&year=2019&month=7&day=25&hour=11&minute=30&resultFormat=json"
    response = requests.get(url)
    data = response.json()# changed here
    
    return data

def create_url(year, month, day, hour, minute, lat=21.19, lon=-158, elv=0):

    url = f"https://hdgm-rt-test.appspot.com/?lat1={lat}&lon1={lon}&altitude={elv}&year={year}&month={month}&day={day}&hour={hour}&minute={minute}&resultFormat=json"
    
    return url
def send_pomme_requests(inp_filename, out_filename, start_time, end_time):

    fmt1 = "%Y-%m-%d %H:%M"
    fmt2 = "%Y%m%d %H:%M"
    time_s = datetime.strptime(start_time, fmt1)
    time_e = datetime.strptime(end_time, fmt1)    


    dates, Bx, By, Bz = [], [], [], []
    fp_out = open(out_filename, "w")
    fp_out.write("date,Bx,By,Bz\n")    
    with open(inp_filename, "r") as fp:
        
        for i, line in enumerate(fp):
            row = line.split()
            if row[0] == "#":
                continue
           
            date = str(row[0]) + " " + str(row[1])
            curr = datetime.strptime(date, fmt2)
            if curr >= time_s and curr <= time_e:
                url = create_url(curr.year, curr.month, curr.day, curr.hour, curr.minute)
                results = get_json_data(url)
                B_pomme = results["B_m"]
                                
                fp_out.write(f"{date},{B_pomme["X"]},{B_pomme["Y"]},{B_pomme["Z"]}\n")
    fp_out.close()

def output_results(filename, dates, Bx, By, Bz):

    with open(filename, "w")as fp:
       
        fp.write("date,Bx,By,Bz\n")
        for date, x,y,z in zip(dates, Bx, By, Bz):
            fp.write(f"{date},{x},{y},{z}")  
        
def verify_outputs(inp_file, out_file):

    date, x, y, z, x_m, y_m, z_m = vp.get_NewTrueMag_arrays(inp_filename)
    x_p, y_p, z_p = [], [], []

    with open(out_file, "r") as fp:
        for line in fp:
                           
def main():
    
    inp_filename = "Data_vs_Model_HON_19970101_20221231.txt"
    start_time = "2015-03-13 00:00"
    end_time = "2015-03-21 00:00"

    out_filename = "pomme_rt_results.txt"
       
    send_pomme_requests(inp_filename, out_filename, start_time, end_time)             
    #output_results(out_filename, dates, Bx, By, Bz)
if __name__=="__main__":
    main()   
   
      
