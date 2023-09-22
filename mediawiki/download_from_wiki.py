"""Download from wiki

This script downloads images of Wikimedia Commons of which the filenames are listed in a CSV. 

This script requires wikiget to be installed in the Python environment.

Usage:
------
python download_from_wiki.py csv folder
    csv: str
        path to a csv with at least the columns QID and Facebook_ID
    folder: str
        path to the directory where all the images should be stored
"""

from csv import DictReader
from sys import argv
import os

csv = argv[1]
folder = argv[2]

image_key = 'image'
QID_key = 'QID'
prefix = 'File:'

def wiki_scrape(image):
    command = 'wikiget \"{}\"'.format(image)
    print(command)
    os.system(command)

def create_folder(folder):
    if not os.path.exists(folder):
        os.mkdir(folder)

def start(metadata, output_dir):
    print("hello! starting!")
    with open(metadata, 'r') as input_file:
        reader = DictReader(input_file)
        os.chdir(output_dir)
        for row in reader:
            image = row[image_key]
            if not image == '':
                folder = row[QID_key]
                create_folder(folder)
                os.chdir(folder)
                wiki_scrape(prefix+image)      
                os.chdir('..')
        input_file.close()

start(csv, folder)
