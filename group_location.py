import os
from src import group_by_dst


def run_merge_three_results(p_folder, m_folder, output_folder):


    files = os.listdir(output_folder)

    for location in files:

        if os.path.isdir(os.path.join(output_folder, location)):
            p_file = os.path.join(p_folder, f"pomme_{location}.txt")
            m_file = os.path.join(m_folder, f"Data_vs_Model_{location}_19970101_20221231_wGSM.txt")
            o_file = os.path.join(output_folder, f"martin_pomme_{location}.txt")

            group_by_dst.attach_three_results(p_file, m_file, o_file)




def run_group_forAllLocation(output_folder, stop_time="202301"):
    files = os.listdir(output_folder)


    for location in files:

        if os.path.isdir(os.path.join(output_folder, location)):
            print(location)
            filename = os.path.join(output_folder, location, f"martin_pomme_{location}.txt")
            group_by_dst.group(filename, output_folder, location, stop_time)

def main():

    top_folder = os.path.dirname(__file__)
    inp_folder = os.path.join(top_folder, "Martin_text_files_with_GSM_fields_2")
    pom_folder = os.path.join(top_folder, "pomme_results")
    output_folder = os.path.join(top_folder, "results")

    run_group_forAllLocation(output_folder)
    #run_merge_three_results(pom_folder, inp_folder, output_folder)

if __name__=="__main__":
    main()