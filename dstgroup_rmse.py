import os

from src import group_by_dst



def main():

    top_folder = os.path.dirname(__file__)


    output_folder = os.path.join(top_folder, "results")

    files = os.listdir(output_folder)
    res_filename = os.path.join(output_folder, "dst_rmse.csv")

    with open(res_filename, "w") as writter:

        writter.write("location,min_dst,max_dst,MX_RMSE,MY_RMSE,MZ_RMSE,PX_RMSE,PY_RMSE,PZ_RMSE\n")

        for location in files:
            print(location)
            if os.path.isdir(os.path.join(output_folder, location)):
                group_by_dst.write_results_file(output_folder, location, writter)





if __name__=="__main__":
    main()