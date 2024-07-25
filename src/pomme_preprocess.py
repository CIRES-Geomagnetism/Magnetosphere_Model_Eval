import average_f107
import create_fyear_inputs
import get_cloud_data
import utils

def get_est_ist(dst):

    est = dst*0.7
    ist = dst*0.3

    return est, ist


def create_inpus_file(m_file, omni_file, f107_file, out_file):

    dates = create_fyear_inputs.get_time_from_inputs(m_file)
    fyears = create_fyear_inputs.get_decimalYear_arr(dates)

    f107_arr = average_f107.f107_to_array(f107_file)

    writter = open(out_file, "w")
    ptr_f107 = 0
    hour = 0

    with open(omni_file, "r") as omni_fp:

        for i, line in enumerate(omni_fp):
            vals = line.split()
            if i == 0:
                continue
            else:
                if hour == 24:
                    ptr_f107 += 1
                    hour = 0
                hour += 1

                fyear = fyears[i-1]
                imf_by = vals[3]
                imf_bz = vals[4]
                speed = vals[5]
                dst = vals[6]

                est, ist = get_est_ist(dst)

                em = get_cloud_data.compute_Em(imf_by, imf_bz, speed)

                omni_fp.write(f"{fyear},{imf_by},{imf_bz},{speed},{est},{ist},{em}")

















