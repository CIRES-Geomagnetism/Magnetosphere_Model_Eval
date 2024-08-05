import os.path
import unittest

from src import create_fyear_inputs
from src import pomme_preprocess
from src import plot_results


class Test_pomme_io(unittest.TestCase):

    def setUp(self):
        self.test_folder = os.path.dirname(__file__)
        self.top_folder = os.path.dirname(self.test_folder)
        self.output_folder = os.path.join(self.top_folder, "results")

        self.inp_folder = os.path.join(self.top_folder, "Martin_text_files_with_GSM_fields_2")

    def test_deciaml_year(self):
        year = 2015
        month = 3
        day = 1

        dyear = create_fyear_inputs.DateTimeToDecimalYear(year, month, day, 0, 30)

        print(dyear)

    def test_extract_outputs_byTime(self):

        min_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 1, 0, 30)
        max_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 31, 23, 30)



        pom_omni_outfile = os.path.join(self.top_folder, "pomme_all_results", "pomme_ASC.txt")

        Bx, By, Bz = pomme_preprocess.extract_outputs_byTime(min_time, max_time, pom_omni_outfile)

        self.assertEqual(-49.30464, Bx[0])
        self.assertEqual(10.64355, By[0])
        self.assertEqual(0.22724, Bz[0])

    def test_get_location_list(self):

        loc = pomme_preprocess.get_location_list(self.top_folder, "results")

        self.assertEqual(len(loc), 15)

    def test_compare_cloud_omni_inputs(self):

        cloud_folder = "pomme_cloud_results"
        omni_folder = "pomme_all_results"

        min_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 1, 0, 30)
        max_time = create_fyear_inputs.DateTimeToDecimalYear(2015, 3, 31, 23, 30)



        cloud_file = os.path.join(self.top_folder, cloud_folder, f"pomme_ASC.txt")
        omni_file = os.path.join(self.top_folder, omni_folder, f"pomme_ASC.txt")

        date, cx, cy, cz = pomme_preprocess.extract_outputs_byTime(min_time, max_time, cloud_file)
        date, mx, my, mz = pomme_preprocess.extract_outputs_byTime(min_time, max_time, omni_file)

        pred_x = [cx, mx]
        pred_y = [cy, my]
        pred_z = [cz, mz]

        labels = ["Database at GCP", "NASA Omni"]

        path = os.path.join(self.top_folder, "results")

        plot_results.plot_results_from_arr(date, pred_x, labels, "Bx", path, "ASC")
        plot_results.plot_results_from_arr(date, pred_y, labels, "By", path, "ASC")
        plot_results.plot_results_from_arr(date, pred_z, labels, "Bz", path, "ASC")





