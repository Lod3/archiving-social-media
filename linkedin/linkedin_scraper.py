"""Facebook scrape

This script downloads profile pictures of LinkedIn accounts that are listed in a csv file. 

This tool makes use of an external javascript app, linkedin-profile-scraper 
(https://github.com/nvanderperren/linkedin-profile-scraper). It is essential 
that that app is started before starting this tool.

This script requires requests to be installed in the Python environment.

Usage:
------
python facebook_scrape.py csv output_dir
    csv: str
        path to a csv with at least the columns QID and LinkedIn_ID
    output_dir: str
        path to the directory where all the images should be stored
"""

from csv import DictReader
import os
from random import randint
from sys import argv
from uuid import uuid4
from time import sleep

import requests

csv = argv[1]
folder = argv[2]

filename = 'qid'
linkedin_key = 'LinkedIn_ID'
QID_key = 'QID'
command = "say Help! Something's wrong. Restart the linkedin-profile-scraper app"


def linkedin_scrape(linkedin_id: str, output: str) -> None:
    """A simple function to download the profile picture of a linkedin account.

    This function uses the linkedin username to scrape the profile information in a JSON-object
    via the Requests library. The external linkedin-profile-scraper app is also used 
    (https://github.com/nvanderperren/linkedin-profile-scraper)
    In the JSON-object the key of the profile picture is sought. The profile picture is then downloaden. 
    A uuid is used to create unique filenames.
    
    After each download we let the script sleep for a while in order to avoid a facebook ban. 
    This pause is a random value to make it look more human-like.

    Error handling is used to avoid a crash when we encounter a linkedin account that doesn't exist 
    anymore.

    Parameters
    ----------
    linkedin_id: str
        the username of a linkedin account
    output: str
        the path to the directory where the image should be stored

    """

    # create filename
    uuid = str(uuid4())
    path = output + '/' + uuid + '.jpg'

    # get the json of the person
    # requirement `nmp start @ linkedin-profile-scraper`
    try:  # try to get the json of the linkedin account
        response = requests.get("http://localhost:3000/?url=https://linkedin.com/in/" + linkedin_id)

    except: # let us know if something goes wrong with the linkedin-profile-scraper app
        print("something went wrong.")
        os.system(command)
        sleep(200)

    else:
        # scrape the profile pic url
        image_url = response.json()['userProfile']['photo']
        if image_url.startswith('http'):
            image_data = requests.get(image_url).content
            # download image
            with open(path, "wb") as handler:
                handler.write(image_data)
    
    finally:
        # let it sleep, let it sleep, let it sleep
        # also if an error occurred
        pause = randint(0, 300)
        print("sleeping for " + str(pause) + ' seconds')
        sleep(pause)

def create_folder(folder: str) -> None:
    """A simple function to check if a folder already exists and create it"""
    if not os.path.exists(folder):
        os.mkdir(folder)


def start(metadata: str, output_dir: str) -> None:
    """A function that uses the csv DictReader to look for the right columns
    in the csv and pass on the values to the linkedin_scrape function"""
    print("hello! starting!")
    with open(metadata, 'r') as input_file:
        reader = DictReader(input_file)
        os.chdir(output_dir)
        for row in reader:
            linkedin = row[linkedin_key]
            if not linkedin == '':
                folder = row[QID_key]
                create_folder(folder)
                print("busy with " + row[QID_key])
                linkedin_scrape(linkedin, folder)
                
        input_file.close()

start(csv, folder)