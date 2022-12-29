# idea:
# 1. use google to search for accounts
# 2. filter out relevant URL's
# 3. store those in a CSV
# 3. do some kind of validation with scraping tools (in other scripts)


from csv import DictReader, writer
from collections import namedtuple
import itertools
import os
from sys import argv
from googlesearch import search
from random import randint
from time import sleep
from uuid import uuid4

from facebook_scraper import get_profile

in_csv = argv[1]
output = argv[2]
wrong_words = ['/groups/', '/public/', '/videos/', '/p/', '/pub/dir/']
platforms = ["linkedin", "facebook", "twitter", "instagram"]


class Politician:
    def __init__(self, name, ID, place, party):
        self.name = name
        self.ID = ID
        self.place = place
        self.party = party
        self.social_media_identifiers = []
        self.urls = []


def get_politicians_info() -> set:
    """Parse the CSV from wikidata and store essential information in a set"""
    with open(in_csv) as input_file:
        reader = DictReader(input_file)
        all_politicians = []
        for row in reader:
            politician = Politician(row["volledige naam"], row['QID'], row["gemeente"], row["fractie"])
            if politician.ID == '':
                politician.ID = str(uuid4())
            all_politicians.append(politician)
        unique_politicians = set(all_politicians)
        return unique_politicians


def find_politician_profiles(set: Politician):
    """Find social media accounts via google with info from the politicians set"""    
    for platform in platforms:
        for index, politician in enumerate(politicians):
            politician.urls.clear()
            politician.social_media_identifiers.clear()
            print(f"#{index+1} {politician.name}")

            # create the google query from our collection of politicians
            query = f"{politician.name} {politician.place} {platform}".replace(' ', '+')
            pause = randint(0,5) # random pause to have more human-like behaviour
            finds = search(query, num=3, stop=3, lang="nl", pause=pause) 
            finds = filter(lambda url: url.find(platform) >= 0, finds) 
            for find in finds:
                identifier = get_account(find)
                if identifier is not None and not identifier.lower() in politician.social_media_identifiers:
                    politician.social_media_identifiers.append(identifier)
                    politician.urls.append(find)

        write_csv(platform, politicians)
        print(f"\nfinished with {platform}\n".upper())


def get_account(url):
    for word in wrong_words:
        if word in url:
            return
    if '/people/' in url or 'linkedin' in url:
        identifier = url.split('/')[4]
        if 'linkedin' in url and 'posts' in url:
            identifier = identifier.split('_')[0]
    else: 
        # works for Twitter and Facebook
        identifier = url.split('/')[3]

    # Facebook ugly url's
    if '?id=' in identifier:
        identifier = int("".join(char for char in identifier if char.isdigit()))

    # Facebook urgly url's
    if '?' in identifier:
        identifier = identifier.split('?')[0]

    return identifier


def write_csv(platform, politicians):
    lines = [["ID", "name", "location", "party", "social_media_identifier", "url"]]
    path = f'{output}/{platform}.csv'
    
    for politician in politicians:
        id = politician.ID
        name = politician.name
        location = politician.place
        party = politician.party
        for (identifier, url) in zip(politician.social_media_identifiers, politician.urls):
            if identifier and url:
                lines.append([id, name, location, party, identifier, url])

    with open(path, 'w') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerows(lines)


politicians = get_politicians_info()
find_politician_profiles(politicians)
