import math
import numpy as np
import os

import src.plot_results
import src.average_f107
import src.create_fyear_inputs


def compute_Em(y, z, swv):
    B_t = math.sqrt(y**2 + z**2)
    if B_t == 0 :
        return 0
    else:
        theta = math.acos(z/B_t)
        em = swv * B_t * math.sin(theta/2)**2 / 1000
        return round(em, 6)


def get_est_ist(dst):

    est = dst*0.7
    ist = dst*0.3

    return est, ist



def create_inpus_file(m_file, omni_file, f107_file, out_file):

    dates = src.create_fyear_inputs.get_time_from_inputs(m_file)
    fyears = src.create_fyear_inputs.get_decimalYear_arr(dates)
    N = len(fyears)

    f107_arr = src.average_f107.f107_to_array(f107_file)

    ptr_f107 = 0
    hour = 0

    with open(omni_file, "r") as omni_fp:

        writter = open(out_file, "w")

        writter.write("dYear,est,ist,imf_by,em,f107,dst\n")

        for i, line in enumerate(omni_fp):
            vals = line.split()
            if i == 0:
                continue
            elif i - 1 == N:
                break
            else:
                if hour == 24:
                    ptr_f107 += 1
                    hour = 0
                hour += 1

                print(i)
                fyear = fyears[i-1]
                imf_by = float(vals[3])
                imf_bz = float(vals[4])
                speed = float(vals[5])
                dst = float(vals[6])
                f107 = f107_arr[ptr_f107]

                est, ist = get_est_ist(dst)

                em = compute_Em(imf_by, imf_bz, speed)

                writter.write(f"{fyear},{round(est,6)},{round(ist,6)},{imf_by},{round(em,6)},{f107},{dst}\n")

        writter.close()


def extract_outputs_byTime(min_dyear, max_dyear, filename):

    date, Bx, By, Bz = [], [], [], []
    with open(filename, "r") as file:
        for i, line in enumerate(file):

            vals = line.split(",")

            if i == 0:
                continue
            else:
                dyear = float(vals[0])

                if min_dyear <= dyear <= max_dyear:
                    date.append(dyear)
                    Bx.append(vals[1])
                    By.append(vals[2])
                    Bz.append(vals[3])
                elif dyear > max_dyear:
                    break

    date = np.array(date, dtype=float)
    Bx = np.array(Bx, dtype=float)
    By = np.array(By, dtype=float)
    Bz = np.array(Bz, dtype=float)

    return date, Bx, By, Bz

def get_location_list(top_dir, res_dirname):

    res_dir = os.path.join(top_dir, res_dirname)

    files = os.listdir(str(res_dir))

    locations = []

    for loc in files:
        path = os.path.join(str(res_dir), loc)
        if os.path.isdir(path):
            locations.append(loc)

    return locations


def compare_cloud_omni_inputs(top_dir, cloud_dir, omni_dir, location_list, min_dyear, max_dyear):

    cloud_dir = os.path.join(top_dir, cloud_dir)
    omni_dir = os.path.join(top_dir, omni_dir)

    for loc in location_list:
        print(loc)
        cloud_file = os.path.join(cloud_dir, f"pomme_{loc}.txt")
        omni_file = os.path.join(omni_dir, f"pomme_{loc}.txt")

        date, cx, cy, cz = extract_outputs_byTime(min_dyear, max_dyear, cloud_file)
        date, mx, my, mz = extract_outputs_byTime(min_dyear, max_dyear, omni_file)

        pred_x = [cx, mx]
        pred_y = [cy, my]
        pred_z = [cz, mz]

        labels = ["Database at GCP", "NASA Omni"]

        path = os.path.join(top_dir, "results")

        src.plot_results.plot_results_from_arr(date, pred_x, labels, "Bx", path, loc)
        src.plot_results.plot_results_from_arr(date, pred_y, labels, "By", path, loc)
        src.plot_results.plot_results_from_arr(date, pred_z, labels, "Bz", path, loc)



















