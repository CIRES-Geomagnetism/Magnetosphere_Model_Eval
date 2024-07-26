#!/bin/zsh



exe_path="./pomme_calc"
info_path="Martin_text_files_with_GSM_fields_2/loc_info.txt"
data_path="inputs/pomme_inputs_50.txt"
Mmodel_path="Martin_text_files_with_GSM_fields_2/Data_vs_Model_HON_19970101_20221231_wGSM.txt"
lat="21.19"
lon="158.0"
elev="0.0"

pomme_res_dir="pomme_results"
results_file=${pomme_res_dir}"/pomme_HON_tmp.txt"
pomme_tmpfile="pom_tmp.txt"

check_dir(){
    if [ ! -d $pomme_res_dir ]; then
        mkdir $pomme_res_dir
    else
      rm -rf $pomme_res_dir
      mkdir $pomme_res_dir
    fi
}


check_dir

{
  read
  while IFS=, read -r fYear est ist imf_by em f107 dst
  do
        # build commands and save im temporary file

        $exe_path -a $lat -o $lon -d $fYear -e $elev -E $est -I $ist -B $imf_by -R $f107 -m $em -T C > tmp.txt

        tail -n 1 tmp.txt > $pomme_tmpfile

        while IFS=, read -r fYear alt lat lon decline incline H X Y Z F
        do
          echo "$fYear,$X,$Y,$Z,$dst" >> $results_file

        done < $pomme_tmpfile
  done
} < $data_path

