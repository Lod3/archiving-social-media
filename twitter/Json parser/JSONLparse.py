#import python modules
import json
import os
import pandas as pd

#vraag JSONL bestandsnaam
#fname = input("Enter the jsonl file name (without extension):")
#parse het JSONL bestand

dflist = []
f = open(os.path.expanduser(f"/mnt/c/Users/Clovis/Documents/Meemoo/pilootproject-gezichtsherkenning/Twitter scrape/gentseproffen.jsonl"), "r") #open het bestand
for line in f: #lees elke lijn in het bestand
    twlist = [] #zet alles in een lijst
    y = json.loads(line) #y is de lijn      
    twlist.append(y["profile_image_url"])
    print(y["profile_image_url"])
    twlist.append(y["screen_name"])
    print(y["screen_name"])


