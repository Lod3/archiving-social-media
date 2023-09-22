import csv
import os

def create_folder(folder: str) -> None:
    """A simple function to check if a folder already exists and if not create it"""
    if not os.path.exists(folder):
        os.mkdir(folder)

with open("gentse_proffen_twitter.csv" , 'r') as infile:
    reader = csv.reader(infile, delimiter=",")
    header = next(reader)

    for row in reader:
        volledige_naam = row[0]
        QID = row[1]
        twitter_gebruikersnaam = row[2]
        folder = row[1]
        create_folder(folder)
        print(folder)