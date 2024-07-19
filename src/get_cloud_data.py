import mysql.connector
from mysql.connector import Error
import datetime as dt
import math

DSCOVER_TIME = dt.datetime(2017, 6, 1, 0, 0, 0)

def execute_query(cursor, query, start_time, end_time):
    
    cursor.execute(query, (start_time, end_time))
    rows = cursor.fetchall()

    return rows

def get_db_data_ashour(cursor, table, time_col, start_time, end_time):

    query = f"""
            SELECT t1.* 
            FROM {table} t1
            INNER JOIN (
            SELECT
                DATE_FORMAT({time_col}, '%Y-%m-%d %H:%M:%S') AS hour,
                MIN({time_col}) AS min_timestamp
            FROM
                {table}
            WHERE 
                obsTime BETWEEN %s AND %s
            GROUP BY hour
            ) t2 
            ON DATE_FORMAT(t1.{time_col}, '%Y-%m-%d %H:%M:%S') = t2.hour
            AND t1.{time_col} = t2.min_timestamp
            ORDER BY t1.{time_col}
        """
    results = execute_query(cursor, query, start_time, end_time)

    return results

def get_db_data2(cursor, table, time_col, start_time, end_time):

    
    query = f"""
             SELECT MIN({time_col}) as timestamp, , MIN(id) as id
      FROM {table}
      GROUP BY DATE({time_col}), HOUR({time_col});
            """

    results = execute_query(cursor, query, start_time, end_time)

    return results

def adjust_delay_time(start_time, end_time, delay_min):

    time_format = "%Y-%m-%d %H:%M:%S"

    start_time_obj = dt.datetime.strptime(start_time, time_format) - dt.timedelta(minutes=delay_min)
    end_time_obj = dt.datetime.strptime(end_time, time_format) - dt.timedelta(minutes=delay_min)
    
    new_st = start_time_obj.strftime(time_format)
    new_et = end_time_obj.strftime(time_format)
  

    return new_st, new_et
def ist_est_atcloud(cursor, table, start_time, end_time):
     
    time_col = "obsTime"
    fmt = "%Y-%m-%d %H:%M:%S"
    
    time_s = dt.datetime.strptime(start_time, fmt) - dt.timedelta(hours=1)
    new_time_s = time_s.strftime(fmt)
    rows = get_db_data_ashour(cursor, table, time_col, new_time_s, end_time)

    last_t = ""    
    Est, Ist = [], []
    #print("est ist time")
    time_step = dt.datetime.strptime(new_time_s, fmt)
    time_step += dt.timedelta(minutes=30)
    for time, dst ,est, ist in rows:
        if time_step.strftime(fmt) != time:
            #time_obj = dt.datetime.strptime(time, fmt)
            while time_step != time:
                Est.append(float("nan"))
                Ist.append(float("nan"))
                print(f"get data time at: {time} but real time should be {time_step}")
 
                time_step += dt.timedelta(hours=1)
                break
        if est > 9999:
            est = float("nan")
        if ist > 9999:
            ist = float("nan")
        Est.append(round(est,6))
        Ist.append(round(ist,6))
        time_step += dt.timedelta(hours=1)        

    print(f"last time at {time}")

    return Est, Ist

def get_db_data_min(cursor, table, time_col, start_time, end_time):
    
    query = f"""SELECT * FROM {table} WHERE {time_col} BETWEEN %s AND %s;"""

    cursor.execute(query, (start_time, end_time))
    rows = cursor.fetchall()

    return rows

def IMFBy_atcloud(cursor, table, start_time, end_time):
     
    time_col = "delayTime"
    delay_min = 35
    time_format = "%Y-%m-%d %H:%M:%S"
    
    time_s, time_e = adjust_delay_time(start_time, end_time, delay_min)

    time_step = dt.datetime.strptime(time_s, time_format)
    if time_step > DSCOVER_TIME:
        table = "DSCOVR_IMF"        
   
    rows = get_db_data_min(cursor, table, time_col, time_s, time_e)
    last_time = ""    
    By = []
    #print("IMF By time")
    idx = 0
 
    for i, (time_o, time_d, x, y, z, swv, dens) in enumerate(rows):
       delay_t = time_d.strftime(time_format)
       
  
       if delay_t[-5:] == "55:00":
           if time_step != time_d:
#                time_obj = dt.datetime.strptime(time, time_format)
                print(time_step)
                print(time_d)
                while time_step != time_d:
                    By.append(float("nan"))
                    time_step += dt.timedelta(hours=1)
         
       
           
           if y > 9999:
               y = float("nan")
               print(f"Fill nan since {y} > 9999 at {time_d}")
           By.append(round(y,6))
                    
           time_step = time_step + dt.timedelta(hours=1)

           
    print(f"last time for IMF_BY: {last_time}")
       

    return By
def compute_Em(y, z, swv):
    B_t = math.sqrt(y**2 + z**2)
    if B_t == 0 :
        return 0
    else:
        theta = math.acos(z/B_t)
        em = swv * B_t * math.sin(theta/2)**2 / 1000
        return round(em, 6)
     
def Em_atcloud(cursor, table, start_time, end_time):
     
    time_col = "delayTime"
    delay_min = 60
    select_at_min = "00"
    time_format = "%Y-%m-%d %H:%M:%S"

    time_s, time_e = adjust_delay_time(start_time, end_time, delay_min)
    time_step = dt.datetime.strptime(time_s, time_format) 
    
    if time_step > DSCOVER_TIME:
        table = "DSCOVR_IMF"        
   

    rows = get_db_data_min(cursor, table, time_col, time_s, time_e)


            
    Em = []
    print(f"use {table}")    
    for time_o, time_d, x, y, z, swv, dens in rows:
        
        delay_t = time_d.strftime(time_format);        
        #print(delay_t)
        if delay_t[-5:] == "30:00":
           if time_step  != time_d:
                #time_obj = dt.datetime.strptime(time_format)
                while time_step != time_d:
                    Em.append(float("nan"))
                    time_step += dt.timedelta(hours=1)
                print(time_step)
           if y < 9999 and z < 9999 and swv < 9999:
                em =compute_Em(y, z, swv)
                Em.append(em)
            
           else:
                Em.append(float("nan"))
           time_step += dt.timedelta(hours=1) 

    return Em
def adjust_F107_time(time):

    #f107_time = time - dt.timedelta(hours=14610)
    f107_time = time.replace(hour=0, minute =0)
    f107_ave_start = f107_time - dt.timedelta(days=40)
    f107_ave_end = f107_time + dt.timedelta(days=41)

    return f107_ave_start, f107_ave_end

def F107_atcloud(cursor, table, start_time, end_time):


    time_format = "%Y-%m-%d %H:%M:%S"
    time_s = dt.datetime.strptime(start_time, time_format) 
    time_e = dt.datetime.strptime(end_time, time_format) 
     
    query = f"""SELECT AVG(data) FROM {table} WHERE obsTime BETWEEN 
            %s AND %s and data < 9999"""

    curr = time_s + dt.timedelta(days=1)
    time_e += dt.timedelta(days=1)
    f107_ave = []
    while curr <= time_e:
        f107_ave_start, f107_ave_end = adjust_F107_time(curr)
        results = execute_query(cursor, query, f107_ave_start, f107_ave_end)
        for i in range(24):        
            f107_ave.append(round(results[0][0],6))
        curr = curr + dt.timedelta(days=1)

    return f107_ave

def create_dates_arr(start_time, end_time):

    time_format = "%Y-%m-%d %H:%M:%S"

    time_s = dt.datetime.strptime(start_time, time_format);
    time_e = dt.datetime.strptime(end_time, time_format);
    time_step = time_s

    dates = []
    dec_year = []
    while time_step <= time_e:
        time_str = time_step.strftime(time_format)
        dyear = toDecimalYear(time_step)
      
        dec_year.append(round(dyear,6))
        dates.append(time_str)
        time_step = time_step + dt.timedelta(hours=1)

    return dates, dec_year

def check_dates(true_date, data, idx):

    
    if true_date == data[0]:
        return data[1], idx + 1
    else:
        return(float("nan")), idx

def output_data_to_file(dates, dec_year, est, ist, by, em, f107, filename):

    N = len(dates)
    idx_e, idx_i, idx_y, idx_m, idx_f = 0, 0, 0, 0, 0
    with open(filename, "w") as fp:
        fp.write("dates,decYear,est,ist,by,em,f107\n")
        for i in range(N):
#            Est, idx_e = check_dates(dates[i], est[idx_e], idx_e)
#            Ist, idx_i = check_dates(dates[i], ist[idx_i], idx_i)
#            By, idx_y = check_dates(dates[i], by[idx_y], idx_y)
#            Em, idx_m = check_dates(dates[i], em[idx_m], idx_m)
#            F107, idx_f = check_dates(dates[i], f107[idx_f], idx_f)
            fp.write(f"{dates[i]},{dec_year[i]},{est[i]},{ist[i]},{by[i]},{em[i]},{f107[i]}\n")
           

def toDecimalYear(date):

    year = date.year
    totalDaysYear = 365

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        totalDaysYear += 1.0

    
    day = date.timetuple().tm_yday
    hour = date.timetuple().tm_hour
    minute = date.timetuple().tm_min

    fyear = year + (day - 1 + (hour + minute/60.0)/24.0) /totalDaysYear

    return fyear

   
   
def main():

    start_time = "2015-12-15 00:30:00"
    end_time = "2015-12-25 23:30:00"

    hostname = "23.236.60.213"
    db = "geomag"
    username = "root"
    passwd = "iwtlnk"

    out_filename = "cloud_data_inputs_20151220.txt" 
    
    try:
        conn = mysql.connector.connect(
            host=hostname,
            database=db,
            user=username,
            password=passwd
        )

        cursor = conn.cursor()

        
        est, ist  = ist_est_atcloud(cursor, "DSTKyoto", start_time, end_time)
        By = IMFBy_atcloud(cursor, "IMF", start_time, end_time)
        Em = Em_atcloud(cursor, "IMF", start_time, end_time)
        f107_ave = F107_atcloud(cursor, "F107", start_time, end_time)
        
        dates, dec_year = create_dates_arr(start_time, end_time)
        print(len(dates))
        print(len(est))
        print(len(By))
        print(len(Em))
        print(len(f107_ave))
        #assert len(Em) == len(dates)

        output_data_to_file(dates, dec_year,  est, ist, By, Em, f107_ave, out_filename);
        cursor.close()
        conn.close()

    except mysql.connector.Error as err:
        print(f"Error: {err}")
if __name__=="__main__":
    
    main()    
        

