import unittest
import os

from src import group_by_dst

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

         
