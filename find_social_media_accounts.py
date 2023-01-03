# idea:
# 1. use google to search for accounts
# 2. filter out relevant URL's
# 3. store those in a CSV
# 3. do some kind of validation with scraping tools (in other scripts)

from csv import DictReader, writer
from sys import argv
from random import randint
from time import sleep
from uuid import uuid4

from googlesearch import search

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
        self.social_media_accounts = []

    def has_no_account(self, platform):
        for account in self.social_media_accounts:
            if account.platform == platform:
                return False
        return True
    
    def get_platform_accounts(self, platform):
        platform_accounts = []
        for account in self.social_media_accounts:
            if account.platform == platform:
                platform_accounts.append(account)
        return platform_accounts

    def get_platform_usernames(self, platform):
        platform_accounts = []
        for account in self.social_media_accounts:
            if account.platform == platform:
                platform_accounts.append(account.username)
        return platform_accounts

class Social_Media_Account:
    def __init__(self, username, platform, url = ''):
        self.username = username
        self.url = url
        self.platform = platform


def get_politicians_info() -> set:
    """Parse the CSV from wikidata and store essential information in a set"""
    with open(in_csv) as input_file:
        reader = DictReader(input_file)
        all_politicians = []
        for row in reader:
            politician = Politician(row["volledige naam"], row['QID'], row["gemeente"], row["partij"])
            if politician.ID == '':
                politician.ID = str(uuid4())
            politician.social_media_accounts = parse_accounts_from_csv(row)
            all_politicians.append(politician)
        unique_politicians = set(all_politicians)

        return unique_politicians


def parse_accounts_from_csv(values: list) -> list:
    social_media_accounts = []
    if values['twitter'] != '':
        social_media_accounts.append(Social_Media_Account(values['twitter'], 'twitter'))
    if values['facebook'] != '':
        social_media_accounts.append(Social_Media_Account(values['facebook'], 'facebook'))
    if values['linkedin'] != '':
        social_media_accounts.append(Social_Media_Account(values['linkedin'], 'linkedin'))    
    return social_media_accounts


def find_politician_profiles(set: Politician) -> None:
    """Find social media accounts via google with info from the politicians set"""    
    for platform in platforms:
        for index, politician in enumerate(politicians):
            print(f"#{index+1} {politician.name}")

            if politician.has_no_account(platform):            
                # create the google query from our collection of politicians
                query = f"{politician.name} {politician.place} {platform}".replace(' ', '+')
                pause = randint(0,60) # random pause to have more human-like behaviour
                finds = search(query, num=3, stop=3, lang="nl", pause=pause)
                finds = filter(lambda url: url.find(platform) >= 0, finds)
                # bij facebook beter checken voor facebook.com?
                for find in finds:
                    identifier = parse_account_from_url(find)
                    if identifier is not None:
                        account = Social_Media_Account(identifier.lower(), platform, find)
                        if not identifier.lower() in politician.get_platform_usernames(platform):
                            politician.social_media_accounts.append(account)        
        
        write_csv(platform, politicians)
        print(f"\nfinished with {platform}".upper())
        pause = randint(0, 100)
        sleep(pause)
        print(f"now sleeping for{pause} seconds\n")


def parse_account_from_url(url: str) -> str:
    #TODO nog iets doen met de /pages/category/ stuff

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
        identifier = str(int("".join(char for char in identifier if char.isdigit())))
    # Facebook ugly url's
    if '?' in identifier:
        identifier = identifier.split('?')[0]
    return identifier


def write_csv(platform, politicians):
    lines = [["ID", "name", "location", "party", "social_media_identifier", "url"]]
    path = f'{output}/{platform}.csv'
    
    for politician in politicians:
        accounts = politician.get_platform_accounts(platform)
        for account in accounts:
            if account.username and account.url:
                lines.append([politician.ID, politician.name, 
                politician.location, politician.party, account.username, account.url])

    with open(path, 'w') as output_file:
        csv_writer = writer(output_file)
        csv_writer.writerows(lines)


politicians = get_politicians_info()
find_politician_profiles(politicians)
