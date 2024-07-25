import math
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

        writter.write("dYear,est,ist,imf_by,em,f107\n")

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

                writter.write(f"{fyear},{round(est,6)},{round(ist,6)},{imf_by},{round(em,6)},{f107}\n")

        writter.close()

















