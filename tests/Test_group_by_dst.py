import unittest
import os
import numpy as np

from src import group_by_dst
from src import create_fyear_inputs


class Test_group_dst(unittest.TestCase):

    def setUp(self) -> None:

        
        self.test_folder = os.path.dirname(__file__)
        self.top_folder = os.path.dirname(self.test_folder)         
        self.output_folder = os.path.join(self.top_folder, "results")

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
        filename = os.path.join(self.output_folder, location, f"martin_pomme_{location}.txt")
        group_by_dst.group(filename, self.output_folder, location, stop_time)

    def test_read_trueNewModel_results(self):

        filename = os.path.join(self.output_folder, "ASC", "data_model_ninf_300.csv")

        date, x, y, z, x_m, y_m, z_m = group_by_dst.read_trueNewModel_results(filename)

        print(date[:5])
        print(z_m[:5])

    def test_setup_dstgroup_num(self):

        arr = group_by_dst.setup_dstgroup_num()

        print(arr)

    def test_dst_vs_rmse(self):

        location = "ASC"
        key = 0

        file_dict = group_by_dst.setup_dstgroup_dict()
        dst_group = group_by_dst.setup_dstgroup_num()

        res_filename = os.path.join(self.output_folder, "dst_rmse.csv")
        writter = open(res_filename, "w")
        group_by_dst.dst_vs_rmse(writter, self.output_folder, location, key, file_dict, dst_group)

    def test_write_results_file(self):

        location = "ASC"
        res_filename = os.path.join(self.output_folder, "dst_rmse.csv")
        writter = open(res_filename, "w")
        writter.write("location,min_dst,max_dst,MX_RMSE,MY_RMSE,MZ_RMSE,PX_RMSE,PY_RMSE,PZ_RMSE\n")
        group_by_dst.write_results_file(self.output_folder, location, writter)


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

    def test_attach_three_results(self):

        p_file = os.path.join(self.top_folder,"pomme_all_results", "pomme_ASC.txt")
        m_file = os.path.join(self.inp_folder, "Data_vs_Model_ASC_19970101_20221231_wGSM.txt")

        out_file = os.path.join(self.output_folder, "ASC", "martin_pomme_ASC.txt")

        group_by_dst.attach_three_results(p_file, m_file, out_file)

    def test_get_name_from_dict(self):

        file_dict = group_by_dst.setup_dstgroup_dict()

        filenames = [name for key, name in file_dict.items()]

        print(filenames)

    def test_remove_past_resfile(self):

        file_dict = group_by_dst.setup_dstgroup_dict()

        group_by_dst.remove_past_resfile(file_dict, self.output_folder, "ASC")

    def test_create_loc_map(self):

        dst_file = os.path.join(self.output_folder, "dst_rmse.csv")
        mt_map, pom_map = group_by_dst.create_loc_map(dst_file)

        print(mt_map.x_map[0])

    def test_output_rmsgroup_results(self):

        dst_group = group_by_dst.setup_dstgroup_num()

        dst_file = os.path.join(self.output_folder, "dst_rmse.csv")
        mt_map, pom_map = group_by_dst.create_loc_map(dst_file)
        out_file = os.path.join(self.output_folder, "rms_group.csv")

        group_by_dst.output_rmsgroup_results(mt_map, pom_map, out_file, dst_group)

    def test_plot_rms_results(self):

        rms_file =  os.path.join(self.output_folder, "rms_group.csv")

        group_by_dst.plot_rms_Allresults(rms_file)

    def test_plot_dst_rmse(self):

        dst_rmse_file = os.path.join(self.output_folder, "dst_rmse.csv")

        group_by_dst.plot_dst_rmse(dst_rmse_file, self.output_folder)







         
