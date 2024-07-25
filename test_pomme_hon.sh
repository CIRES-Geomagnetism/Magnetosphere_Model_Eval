#!/bin/zsh



exe_path="./pomme_calc"
info_path="Martin_text_files_with_GSM_fields_2/loc_info.txt"
data_path="inputs/pomme_inputs_19972022.txt"
lat="21.19"
lon="158.0"
elev="0.0"

pomme_res_dir="pomme_results"
results_file=${pomme_res_dir}"/pomme_HON_tmp.txt"

check_dir(){
    if [ ! -d "results/$1" ]; then
        mkdir "results/$1"
    fi
}

{
  read
  while IFS=, read -r fYear est ist imf_by em f107
  do
        # build commands and save im temporary file

        $exe_path -a $lat -o $lon -d $fYear -e $elev -E $est -I $ist -B $imf_by -R $f107 -m $em -T C > tmp.txt

        tail -n 1 tmp.txt >> $results_file


  done
} < $data_path
