import os
import requests
import zipfile
import pandas as pd

API_URL = "https://api.github.com/repos/DomSamangy/NBA_Shots_04_25/contents"
datadir= "data"

def fetch_file_list():
    r = requests.get(API_URL) 
    r.raise_for_status() 
    return r.json() 

def download_zip(file_info):
    local_path = os.path.join(datadir, file_info["name"])

    if os.path.exists(local_path):
        print(f"{file_info['name']} already downloaded")
        return local_path

    print(f"downloading {file_info['name']}...")
    data = requests.get(file_info["download_url"]).content

    with open(local_path, "wb") as f:
        f.write(data)

    return local_path

def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z: #so that it gets closed automatically
        for name in z.namelist():
            if name.startswith("__MACOSX"):#might find gargabe zips from mac
                continue
            out_path = os.path.join(datadir, name)
            if not os.path.exists(out_path):
                print(f"extracting {name}...")
                z.extract(name, datadir)

def mergecsv():
    tempdf=[]
    for filename in os.listdir(datadir): 
        if filename.endswith(".csv"): 
            filepath=os.path.join(datadir, filename) 
            tempdf.append(pd.read_csv(filepath))    
            print (f"{filename} loaded")
    
    savepath=os.path.join(datadir, "shots_all_seasons.csv")
    df=pd.concat(tempdf, ignore_index=True) #to reset rows index
    df.to_csv(savepath, index=False) #to not create a new index column
    print("all csvs merged successfully")

def main():
    files = fetch_file_list()

    zip_files = [f for f in files if f["name"].endswith(".zip")]

    if not zip_files:
        print("no zip files found in the repo!")
        return

    for f in zip_files:
        if f["name"].endswith(".zip"):
            zipfile=download_zip(f)
            extract_zip(zipfile)
            os.remove(zipfile)
            print("downloaded " + f["name"] + " successfully")
    mergecsv()
    print(" data ready in /data ")

if __name__=="__main__":
    main()  
