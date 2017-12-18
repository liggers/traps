import random
import requests
from tinydb import TinyDB, Query
from bs4 import BeautifulSoup
import urllib3
import certifi
from datetime import datetime
from time import strftime, strptime, localtime
import pprint
import re
import unicodedata

subreddit_max_search = 5


def gelbooru_image_search(rating, trap="", *args):
    try:
        tags = f"-asian+-non-asian+rating%3a{rating}+{trap}"
        for i in args:
            if trap == 'trap' and '-trap' in i.lower():
                    return "What are you trying to pull here? The dick only makes it better!"
            else:
                tags += "+" + i

        #pid = random.randint(0, 100) if not args else ""
        url = f"http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}&json=1"
        r = requests.get(url).json()

        return random.choice(r)['file_url']

    except ValueError:
        return "Nice command."


def subreddit_search(subreddit_list):
    headers = {'User-agent': 'traps-bot (by Keisakyu)'}
    url = f"https://www.reddit.com/r/{random.choice(subreddit_list)}.json"
    for i in range(0, subreddit_max_search):
        try:
            r = requests.get(url, headers=headers)
            r = r.json()
            start = random.choice(r['data']['children'])
            post_type = start['data']['is_self']
            replacement = 'amp;'
            if not post_type:
                pic = start['data']['url']
                if replacement in pic:
                    pic = pic.replace(replacement, "")
                return pic
            else:
                continue
        except:
            pass

def get_national_days():
    db = TinyDB('national_days.json')
    db.purge_tables()
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), maxsize=1, timeout=5)
    for month in months:
        url = f'https://nationaldaycalendar.com/{month}/'
        r = http.request('GET', url)
        soup = BeautifulSoup(r.data, 'html.parser')

        days_container = soup.find_all("div", class_="et_pb_blurb_content")
        current_year = strftime("%Y", localtime())
        national_days_for_month = []

        for day_container in days_container:
            day_string = day_container.find("h4").string
            day_string = re.sub(r'(\d)(st|nd|rd|th)', r'\1', day_string)
            day_string = strftime(f"{current_year}-%m-%d", strptime(day_string, "%B %d"))

            national_days = day_container.find_all("a")
            national_days = "\n".join(national_day.text.replace("\n", " ") for national_day in national_days)

            national_days_for_month.append({"date": day_string, "national_days": national_days})

        db.insert_multiple(national_days_for_month)


if __name__ == '__main__':
    get_national_days()
