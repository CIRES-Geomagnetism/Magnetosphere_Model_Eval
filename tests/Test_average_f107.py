import unittest
import os
import math

from src import average_f107
from src import create_fyear_inputs


class Test_average_f107(unittest.TestCase):

    def setUp(self):

        self.test_folder = os.path.dirname(__file__)
        self.top_folder = os.path.dirname(self.test_folder)

        self.omni_f107file = os.path.join(self.top_folder, "inputs", "omni2_f107.txt")

        self.output_folder = os.path.join(self.top_folder, "results", "global")
        self.inp_folder = os.path.join(self.top_folder, "Martin_text_files_with_GSM_fields_2")

    def test_get_f107_start_index(self):

        start_time = "19970101 00:30:00"

        index = average_f107.get_f107_start_index(start_time, self.omni_f107file)

        print(index)

        date_to_start = ""

        with open(self.omni_f107file, "r") as file:
            for i, line in enumerate(file):
                if i == index:
                    vals = line.split()

                    date_to_start = f"{vals[0]} {vals[1]} {vals[2]}"

                    break

        self.assertEqual(date_to_start, "1996 327 0")

    def test_get_f107_enddate(self):

        end_time = "20221231 00:30:00"

        year, day = average_f107.get_f107_end_date(end_time)

        self.assertEqual(str(year), "2023")
        self.assertEqual(str(day), "40")

    def test_create_f107_80ave(self):

        out_filename = os.path.join(self.top_folder, "inputs", "f107_19972022.txt")
        start_time = "19970101 00:30:00"
        end_time = "20221231 00:30:00"

        m_file = os.path.join(self.inp_folder, "Data_vs_Model_ASC_19970101_20221231_wGSM.txt")
        dates = create_fyear_inputs.get_time_from_inputs(m_file)
        num_date = math.ceil((len(dates)) / 24)

        print(num_date)

        average_f107.create_f107_80ave(start_time, num_date, self.omni_f107file, out_filename)

    def test_f107_toarray(self):

        out_filename = os.path.join(self.top_folder, "inputs", "f107_19972022.txt")
        arr = average_f107.f107_to_array(out_filename)

        print(len(arr))

        m_file = os.path.join(self.inp_folder, "Data_vs_Model_ASC_19970101_20221231_wGSM.txt")
        dates = create_fyear_inputs.get_time_from_inputs(m_file)

        print(dates[0])

        self.assertEqual(24*len(arr), len(dates))



