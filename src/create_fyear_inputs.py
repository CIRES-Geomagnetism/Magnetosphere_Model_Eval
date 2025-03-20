from datetime import datetime

def DateToDecimalYear(year, month, day):
    temp = 0
    ExtraDay = 0
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        ExtraDay = 1
    MonthDays = [0, 31, 28+ExtraDay, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(month):
        temp += MonthDays[i]
    temp += day
    DecimalYear = year + (temp - 1) / (365.0 + ExtraDay)
    return DecimalYear

def DateTimeToDecimalYear(year, month, day, hour, minute):
    temp = 0
    ExtraDay = 0
    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        ExtraDay = 1
    MonthDays = [0, 31, 28+ExtraDay, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(month):
        temp += MonthDays[i]
    temp += day
    print(f"Get day: {temp}")
    temp += (minute/60.0+hour)/24.0

    print(f"ExtraDay: {ExtraDay}")
    DecimalYear = year + (temp - 1) / (365.0 + ExtraDay)

    return DecimalYear


def get_time_from_inputs(filename):

    dates = []

    with open(filename, "r") as file:

        for line in file:
            if line[0] == "#":
                continue
            info = line.split()
            date_str = ""

            date = info[0]
            time = info[1]

            date_str += date
            date_str += " "
            date_str += time

            dates.append(date_str)


    return dates

def toDecimalYear(date_str):

    format = "%Y%m%d %H:%M"

    parse_date = datetime.strptime(date_str, format)

    year = parse_date.year
    totalDaysYear = 365

    if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
        totalDaysYear += 1.0

    
    day = parse_date.timetuple().tm_yday
    hour = parse_date.timetuple().tm_hour
    minute = parse_date.timetuple().tm_min


    fyear = year + (day - 1 + (hour + minute/60.0)/24.0) /totalDaysYear

    return fyear

def get_decimalYear_arr(TimeArr):

    decimalYears = []



    for dates in TimeArr:
        fyear = toDecimalYear(dates)
        decimalYears.append(fyear)


    return decimalYears

def attached_fyear_toinputs(inp_file, fyears, out_file):

    out_f = open(out_file, "w")


    idx = 0

    with open(inp_file, "r") as inp_f:

        for line in inp_f:
            if line[0] == "%":
                continue

            info = line.split()
            for val in info:
                out_f.write(f"{val} ")
            out_f.write(f"{fyears[idx]}\n")
            idx += 1


    out_f.close()




def main():

    date_inp_filename = "Data_vs_Model_HON_19970101_20221231.txt"
    val_inp_file = "HON_POMME_Input.txt"
    out_filename = "HON_POMME_inputs_fyear.txt"
    dates = get_time_from_inputs(date_inp_filename)

    fyears = get_decimalYear_arr(dates)
    #fyear = toDecimalYear("20190725 11:30")
    #print(f"decimal year: {fyear}")

    attached_fyear_toinputs(val_inp_file, fyears, out_filename)

    


if __name__=="__main__":
    main()








