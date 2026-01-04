import os
import requests
import zipfile
import pandas as pd

# restituisce la lista dei file della repo che mi serve
API_URL = "https://api.github.com/repos/DomSamangy/NBA_Shots_04_25/contents"
cartelladati= "data" #devi crearla se non esiste

#controlla se la cartella esista e nel caso la crea
def ensure_data_dir():
    os.makedirs(cartelladati, exist_ok=True)

#mi da la lista dei file nella repos di riferimento
def fetch_file_list():
    r = requests.get(API_URL) #qui chiede i file
    r.raise_for_status() #gestisce errori
    return r.json() #ritorna il dizionario di dizionari, per ogni chiave è un file


def download_zip(file_info):
    local_path = os.path.join(cartelladati, file_info["name"])

    # se esiste già, non riscaricare
    if os.path.exists(local_path):
        print(f"Già presente: {file_info['name']}")
        return local_path

    print(f"Scarico {file_info['name']}...")
    data = requests.get(file_info["download_url"]).content

    with open(local_path, "wb") as f:
        f.write(data)

    return local_path

def extract_zip(zip_path):
    with zipfile.ZipFile(zip_path, "r") as z:
        for name in z.namelist():
            if name.startswith("__MACOSX"):
                continue
            out_path = os.path.join(cartelladati, name)
            # Evita di estrarre più volte
            if not os.path.exists(out_path):
                print(f"sto estraendo {name}...")
                z.extract(name, cartelladati)

def mergecsv():
    tempdf=[]
    for filename in os.listdir(cartelladati): 
        if filename.endswith(".csv"): 
            filepath=os.path.join(cartelladati, filename) 
            tempdf.append(pd.read_csv(filepath))    
            print (f"{filename} caricato")
    
    df=pd.concat(tempdf, ignore_index=True)
    df.to_csv("shots_all_seasons.csv", index=False) 


def main():
    ensure_data_dir()
    files = fetch_file_list()

    # Filtra solo gli ZIP
    zip_files = [f for f in files if f["name"].endswith(".zip")]

    if not zip_files:
        print("Nessun file ZIP trovato nella repo!")
        return

    for f in zip_files:
        if f["name"].endswith(".zip"):
            zipfile=download_zip(f)
            extract_zip(zipfile)
            os.remove(zipfile)
            print("scaricato " + f["name"] + " con successo")
    print(" dati pronti in /data ")
    mergecsv()

main()
