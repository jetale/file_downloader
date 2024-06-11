from io import StringIO

import pandas as pd
import os
import glob
import requests



class DownloadFiles:

    def __init__(self):
        self.input_file_path = "input/Human-Promoter_interactions_SATORI.csv"
        self.srx_file_path = "input/chip_atlas_data.csv"
        self.base_download_link = "https://chip-atlas.dbcls.jp/data/hg19/eachData/bed05/{Experimental_ID}.05.bed"
        self.input_df = pd.read_csv(self.input_file_path)
        self.srx_df = pd.read_csv(self.srx_file_path, delimiter="\t")
        self.create_storage_dirs()
        self.delete_old_files()

    def create_storage_dirs(self):
        """ This function creates directories for storing the downloaded files"""
        storage_dirs = ["dir1", "dir2"]
        for dr in storage_dirs:
            if not os.path.exists(dr):
                os.makedirs(dr)
                print(f"Directory created - {dr}")


    def delete_old_files(self):
        """This function deletes old files before starting download"""
        dirs = ["dir1/*", "dir2/*"]
        for dr in dirs:
            files = glob.glob(dr)
            if files:
                for file in files:
                    os.remove(file)
                    print(f"Removing {file}")

    def delete_temp_files(self, dir_name):
        print(f"Removing temp files from {dir_name}")
        files = glob.glob(dir_name)
        if files:
            for file in files:
                if "temp" in file:
                    os.remove(file)
                    print(f"Removing {file}")



    def download_and_return(self):
        self.delete_old_files()
        for index, row in self.input_df.iterrows():
            tf1 = row["TF1"]
            tf2 = row["TF2"]
            ret_dir1 = self.download_bed_file(tf1, "dir1")
            ret_dir2 = self.download_bed_file(tf2, "dir2")
            yield [ret_dir1, ret_dir2]



    def download_bed_file(self, tf_val, dir_name):
        srx_vals = []
        dfs = []
        out_dir = dir_name + "/combined_data.bed"
        temp_file_path = dir_name + "/temp_"
        print(f"\n\nDownloading files for - {tf_val} in {dir_name}")

        #Find all SRX for given tf_val
        for index, row in self.srx_df.iterrows():
            if row["Track type"] == tf_val:
                srx_vals.append(row["SRX ID"])

        #Download bed files
        print(f"Total {len(srx_vals)} files to be downloaded for {tf_val}")
        for index, val in enumerate(srx_vals):
            print(f"Downloading file {index+1}/{len(srx_vals)} with experiment_id - {val}")
            temp_file_name = temp_file_path + str(index) + "_.bed"
            url = self.base_download_link.format(Experimental_ID=val)
            response = requests.get(url)
            if response.status_code == 200:  
                with open(temp_file_name, 'w') as file:
                    file.write(response.text)
            else:
                print(f"Failed to download {url}")

        #Combine all temp files into one
        print(f"Combining {len(srx_vals)} files for {tf_val} into - {out_dir} \n\n")
        for file_name in os.listdir(dir_name):
            file_path = os.path.join(dir_name, file_name)
            df = pd.read_csv(file_path, sep="\t", header=None)
            df.to_csv(out_dir, sep="\t", header=False, index=False, mode='a')
        
        # Deleting temp files
        self.delete_temp_files(dir_name)

        return out_dir



if __name__ == "__main__":
    # Examples usage
    dwldr = DownloadFiles()
    dwlrd_gen = dwldr.download_and_return()
    vals = next(dwlrd_gen)
    print(vals)