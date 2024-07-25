import datetime as dt
import os




def get_f107_end_date(end_time):

    time_fmt = "%Y%m%d %H:%M:%S"

    end_time_obj = dt.datetime.strptime(end_time, time_fmt)
    ave_end_time_obj = end_time_obj + dt.timedelta(days=41)


    ave_s_year = ave_end_time_obj.year
    ave_s_day = ave_end_time_obj.timetuple().tm_yday

    return ave_s_year, ave_s_day


def get_f107_start_index(start_time: str, filename:str):

    time_fmt = "%Y%m%d %H:%M:%S"

    start_time_obj = dt.datetime.strptime(start_time, time_fmt)
    ave_start_time_obj = start_time_obj - dt.timedelta(days=40)


    ave_s_year = ave_start_time_obj.year
    ave_s_day = ave_start_time_obj.timetuple().tm_yday


    with open(filename, "r") as file:
        for l, line in enumerate(file):
            row = line.split()

            if row[0] == str(ave_s_year) and row[1] == str(ave_s_day):
                    return l

    return -1

def write_output(filename, val):

    with open(filename, "a") as file:
        ave = round(val/82, 2)
        file.write(f"{ave}\n")

def create_f107_80ave(start_time, num_of_date, inp_filename, out_filename):

    start_index = get_f107_start_index(start_time, inp_filename)
    #end_year, end_day = get_f107_end_date(end_time)

    f107_sum = 0
    que = [0]
    count  = 0

    if os.path.isfile(out_filename):
        os.remove(out_filename)

    with open(inp_filename, "r") as fp:
        for i, line in enumerate(fp):
            if i < start_index:
                continue
            else:
                vals = line.split()
                if count == num_of_date:

                    break


                que.append(vals[3])
                f107_sum += float(vals[3])

                if i + 1 < 82:
                   continue
                else:
                    remove_val = que.pop(0)
                    f107_sum -= float(remove_val)
                    write_output(out_filename, f107_sum)
                    count += 1



def f107_to_array(filename):
    arr = []

    with open(filename, "r") as file:
        for f107 in file:
            arr.append(float(f107))

    return arr


