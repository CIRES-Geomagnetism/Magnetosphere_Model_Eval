import os
import src.pomme_preprocess as pomme_preprocess





def main():

    top_folder = os.path.dirname(__file__)
    Mmodel_folder = os.path.join(top_folder, "Martin_text_files_with_GSM_fields_2")
    inp_folder = os.path.join(top_folder, "inputs")


    m_file = os.path.join(Mmodel_folder, "Data_vs_Model_ASC_19970101_20221231_wGSM.txt")
    omni_file = os.path.join(inp_folder, "omni_19972022.txt")
    f107_file = os.path.join(inp_folder, "f107_19972022.txt")
    out_file = os.path.join(inp_folder, "pomme_inputs_19972022.txt")

    pomme_preprocess.create_inpus_file(m_file, omni_file, f107_file, out_file)



if __name__=="__main__":
    main()