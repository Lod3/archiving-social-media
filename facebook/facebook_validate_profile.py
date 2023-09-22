# idea:
# 1. get the data out of the csv
# 2. use get_profile to get the name and the places_lived out of the profile
# 3 check if those are the same as naam and gemeente
# 4. store results in a CSV

from csv import DictReader
import os
from random import randint
from sys import argv
from time import sleep

from dotenv import load_dotenv # library to load local .env files
from facebook_scraper import get_profile

csv = argv[1]
output = argv[2]
load_dotenv()
cookies = os.getenv('COOKIES')

def get_profile_data(profile: str) -> (str, str):
    profile_data = get_profile(profile, cookies=cookies)
    name = profile_data['Name']
    for places in profile_data['Places lived']:
        place = places['text'].split(',')[0]
         
