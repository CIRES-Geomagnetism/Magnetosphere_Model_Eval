#!/bin/zsh

#make clean
#make all


time_tag="20150623"

exe_path="./build/pomme_calc"
info_path="Martin_text_files_with_GSM_fields/loc_info.txt"
data_path="inputs/cloud_data_inputs_${time_tag}.txt"
max_lat=90
elev="0.0"
check_dir(){
    if [ ! -d "results/$1" ]; then
        mkdir "results/$1"
    fi
}

{
read
while IFS=, read -r location colat lon
do
    results_file="results/global/${location}/pomme_cloud_results_${time_tag}.txt"
    check_dir $location
    lat=$(echo "$max_lat - $colat" | bc)
 
    echo "date alt lat lon decline incline H X Y Z F" > $results_file

    {
    read
    while IFS=, read -r dates fYear est ist imf_by em f107
    do
      # build commands and save im temporary file
      
      $exe_path -a $lat -o $lon -d $fYear -e $elev -E $est -I $ist -B $imf_by -R $f107 -m $em -T C > tmp.txt
      
      tail -n 1 tmp.txt >> $results_file
                 
    done 
    } < $data_path    
done 
} < $info_path



