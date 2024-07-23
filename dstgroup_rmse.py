import os

from src import group_by_dst



def main():

    top_folder = os.path.dirname(__file__)


    output_folder = os.path.join(top_folder, "results", "global")

    files = os.listdir(output_folder)

    for location in files:
        print(location)
        if os.path.isdir(os.path.join(output_folder, location)):
            group_by_dst.write_results_file(output_folder, location)





if __name__=="__main__":
    main()