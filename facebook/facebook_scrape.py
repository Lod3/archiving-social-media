"""Facebook scrape

This script downloads profile pictures of facebook accounts that are listed in a csv file. 

This tool requires a .env file (see .env.example in the GitHub repository) containing the path to 
a facebook cookies.txt file, which is necessary to scrape facebook.

This script requires dotenv, facebook_scraper and reuests to be installed within the Python
environment you are running this script in.

Usage:
------
python facebook_scrape.py csv output_dir
    csv
        path to a csv with at least the columns QID and Facebook_ID
    output_dir
        path to the directory where all the images should be stored
"""

from csv import DictReader
import os
from random import randint
from sys import argv
from time import sleep
from uuid import uuid4

from dotenv import load_dotenv # library to load local .env files
from facebook_scraper import get_profile # function to scrape profile info of facebook account
import requests  # library to communicate with webresources

csv = argv[1]  # path to the csv with at least a QID of other identifier and a Facebook_ID 
output_dir = argv[2]

load_dotenv()
cookies = os.getenv('COOKIES')  # you'll need a cookie.txt file of a facebook account to scrape data
QID_key = 'QID'
facebook_key = 'Facebook_ID'

def facebook_scrape(facebook_id: str, output: str) -> None:
    """A simple function to download the profile picture of a facebook account (personal and page)

    This function uses the facebook username to scrape the profile information in a JSON-object. 
    The facebook_scraper module is used for that.
    In the JSON-object the key of the profile picture is sought. The URL is captured and the requests
    module is used to download and save the profile picture.
    After each download we let the script sleep for a while in order to avoid a facebook ban. 
    This pause is a random value to make it look more human-like.

    Error handling is used to avoid a crash when we encounter a facebook username that doesn't exist 
    anymore.

    Parameters
    ----------
    facebook_id: str
        the username of a facebook account
    output: str
        the path to the directory where the image should be stored

    """
    #output folder
    uuid = str(uuid4())
    path = output + '/' + uuid + '.jpg'

    try:
        # check if it's possible to scrape the profile info
        json = get_profile(facebook_id, cookies=cookies)

    except:
        # if scraping is not possible, e.g. a deleted account
        print("something went wrong")

    else:
        # if scraping was succesfull
        image_url = json['profile_picture']

        if image_url.startswith('http'):
            image_data = requests.get(image_url).content

            # downlaod image
            with open(path, "wb") as handler:
                handler.write(image_data)
 
    finally:
        # execute always
        # let it sleep, let it sleep, let it sleep
        pause = randint(0, 300)
        print("sleeping for " + str(pause) + ' seconds')
        sleep(pause)
    

def create_folder(folder: str) -> None:
    """A simple function to check if a folder already exists and if not create it"""
    if not os.path.exists(folder):
        os.mkdir(folder)

def start():
    """A function that uses the csv DictReader to look for the right columns and 
    pass on the values to the facebook_scrape function"""
    with open(csv, 'r') as input_file:
        reader = DictReader(input_file)
        os.chdir(output_dir)
        for row in reader:
            facebook = row[facebook_key]
            if not facebook == '':
                folder = row[QID_key]
                create_folder(folder)
                facebook_scrape(facebook, folder)
                
        input_file.close()

start()