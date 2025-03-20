#!/bin/bash

#make clean
#make all



exe_path="./pomme_calc"
info_path="Martin_text_files_with_GSM_fields_2/loc_info.txt"
data_path="inputs/pomme_inputs_19972022.txt"


pomme_res_dir="pomme_results"

pomme_tmpfile="pom_tmp.txt"
max_lat=90
elev="0.0"

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
read -r REPLY
while IFS=, read -r location colat lon
do
    echo "$location"
    results_file="$pomme_res_dir/pomme_$location.txt"

    lat=$(echo "$max_lat - $colat" | bc)

    echo "date X Y Z dst" > $results_file

    {
    read -r REPLY
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
done
} < $info_path


