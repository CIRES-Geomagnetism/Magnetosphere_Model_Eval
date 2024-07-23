import average_f107
import create_fyear_inputs
import get_cloud_data


def create_inpus_file(m_file, omni_file, f107_file, out_file):

    dates = create_fyear_inputs.get_time_from_inputs(m_file)

    f107_arr = average_f107.f107_to_array(f107_file)

    writter = open(out_file, "w")
    ptr_f107 = 0

    with open(omni_file, "r") as omni_fp:

        for i, line in enumerate(omni_fp):
            vals = line.split()
            if i == 0:
                continue
            else:
                imf_by = vals[3]
                imf_bz = vals[4]
                speed = vals[5]

                em = get_cloud_data.compute_Em(imf_by, imf_bz, speed)















