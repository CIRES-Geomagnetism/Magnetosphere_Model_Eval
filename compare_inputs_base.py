import os
from src import pomme_preprocess
from src import create_fyear_inputs

def main():

    top_dir = os.path.dirname(__file__)

    cloud_folder = "pomme_cloud_results"
    omni_folder = "pomme_all_results"

    min_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 1, 0, 30)
    max_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 31, 23, 30)

    locations = pomme_preprocess.get_location_list(top_dir, "results")

    pomme_preprocess.compare_cloud_omni_inputs(top_dir, cloud_folder, omni_folder, locations, min_time, max_time)

if __name__=="__main__":
    main()
