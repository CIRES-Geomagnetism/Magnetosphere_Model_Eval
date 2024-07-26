import os
from src import group_by_dst




def run_group_forAllLocation(inp_folder, output_folder, stop_time="202301"):
    files = os.listdir(output_folder)

    for location in files:
        if len(str(location)) > 3:
            continue
        else:
            print(location)
            filename = os.path.join(inp_folder, f"Data_vs_Model_{location}_19970101_20221231_wGSM.txt")
            group_by_dst.group(filename, output_folder, location, stop_time)

def main():

    top_folder = os.path.dirname(__file__)
    inp_folder = os.path.join(top_folder, "Martin_text_files_with_GSM_fields_2")

    output_folder = os.path.join(top_folder, "results", "global")

    run_group_forAllLocation(inp_folder, output_folder)

if __name__=="__main__":
    main()