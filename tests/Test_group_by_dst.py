import unittest
import os
import numpy as np

from src import group_by_dst
from src import create_fyear_inputs

class Test_group_dst(unittest.TestCase):

    def setUp(self) -> None:

        
        self.test_folder = os.path.dirname(__file__)
        self.top_folder = os.path.dirname(self.test_folder)         
        self.output_folder = os.path.join(self.top_folder, "results", "global")

        self.inp_folder = os.path.join(self.top_folder, "Martin_text_files_with_GSM_fields_2")
    def test_output_path(self):
        
        location = "ASC"
        self.assertEqual(self.output_folder, "/Users/lily/Projects/Magnetosphere_Model_Eval/results/global")
        filename = group_by_dst.output_path(-100, location, self.output_folder)
        
        true_filename = f"/Users/lily/Projects/Magnetosphere_Model_Eval/results/global/{location}/data_model_n100_50.csv"
        self.assertEqual(filename, true_filename)
    
    def test_group(self):
        
        location = "ASC"
        stop_time = "202301"
        filename = os.path.join(self.inp_folder, f"Data_vs_Model_{location}_19970101_20221231_wGSM.txt")
        group_by_dst.group(filename, self.output_folder, location, stop_time)

    def test_read_trueNewModel_results(self):

        filename = os.path.join(self.output_folder, "ASC", "data_model_ninf_300.csv")

        date, x, y, z, x_m, y_m, z_m = group_by_dst.read_trueNewModel_results(filename)

        print(date[:5])
        print(z_m[:5])

    def test_setup_dstgroup_num(self):

        arr = group_by_dst.setup_dstgroup_num()

        print(arr)

    def test_write_results_file(self):

        location = "ASC"
        group_by_dst.write_results_file(self.output_folder, location)

    def test_dst_vs_rmse(self):

        location = "ASC"
        key = 0

        file_dict = group_by_dst.setup_dstgroup_dict()
        dst_group = group_by_dst.setup_dstgroup_num()

        res_filename = os.path.join(self.output_folder, location, "dst_rmse.csv")
        group_by_dst.dst_vs_rmse(self.output_folder, location, key, file_dict, dst_group, res_filename)

    def test_attach_1st_results(self):

        files = os.listdir(self.output_folder)
        file_dict = group_by_dst.setup_dstgroup_dict()
        dst_group = group_by_dst.setup_dstgroup_num()

        key = 0

        for location in files:
            if os.path.isdir(os.path.join(self.output_folder, location)):
                res_filename = os.path.join(self.output_folder, location, "dst_rmse.csv")
                group_by_dst.dst_vs_rmse(self.output_folder, location, key, file_dict, dst_group, res_filename)

    def test_create_fyear_inputs(self):

        m_file = os.path.join(self.inp_folder, "Data_vs_Model_ASC_19970101_20221231_wGSM.txt")

        dates = create_fyear_inputs.get_time_from_inputs(m_file)
        fyears = create_fyear_inputs.get_decimalYear_arr(dates)

        print(len(fyears))

        self.assertEqual(len(dates), len(fyears))






         
