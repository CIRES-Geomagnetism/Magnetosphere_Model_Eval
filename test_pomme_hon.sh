#!/bin/zsh



exe_path="./pomme_calc"
info_path="Martin_text_files_with_GSM_fields_2/loc_info.txt"
data_path="inputs/pomme_inputs_19972022.txt"
Mmodel_path="Martin_text_files_with_GSM_fields_2/Data_vs_Model_ASC_19970101_20221231_wGSM.txt"
colat="97.897"
lon="345.617"
elev="0.0"
max_lat=90
lat=$(echo "$max_lat - $colat" | bc)

pomme_res_dir="pomme_all_results"
results_file=${pomme_res_dir}"/pomme_ASC.txt"
pomme_tmpfile="pom_tmp.txt"

check_dir(){
    if [ ! -d $pomme_res_dir ]; then
        mkdir $pomme_res_dir
    else
      rm -rf $pomme_res_dir
      mkdir $pomme_res_dir
    fi
}


# check_dir

echo "date X Y Z dst" > $results_file

{
  read
  while IFS=, read -r fYear est ist imf_by em f107 dst
  do
        # build commands and save im temporary file

        $exe_path -a $lat -o $lon -d $fYear -e $elev -E $est -I $ist -B $imf_by -R $f107 -m $em -T C > tmp.txt

        tail -n 1 tmp.txt > $pomme_tmpfile

        while IFS=, read -r fYear alt latitude longtitude decline incline H X Y Z F
        do
          echo "$fYear,$X,$Y,$Z,$dst" >> $results_file

        done < $pomme_tmpfile
  done
} < $data_path

