import pandas as pd 
import os 

path="data/NBA_2004_2023_Shots.csv"
datadir="data"

def mergecsv():
    tempdf=[]
    for filename in os.listdir(datadir): #qui mi restituisce tutti i filename nella cartella data e li scorre uno ad uno 
        if filename.endswith(".csv"): #il gitignore farebbe casino
            filepath=os.path.join(datadir, filename) #concatena datadir e filename in un path unico
            tempdf.append(pd.read_csv(filepath))    
            print ("{filename} caricato")


    return pd.concat(tempdf)

def preview(): #crea per visualizzare tipo 20 righe di tabella durante il programma
    return 0


shots=mergecsv()

choice=input("Choose an option to continue: ")
match(choice):
    case "visual":
        print("saw that")



