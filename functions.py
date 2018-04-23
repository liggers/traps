import random
import requests
from tinydb import TinyDB
from bs4 import BeautifulSoup
import urllib3
import certifi
from time import strftime, strptime, localtime
import re
from json.decoder import JSONDecodeError

subreddit_max_search = 5


def gelbooru_image_search(rating, trap="", *args):
    args = [x.lower() for x in args]
    base_url = "https://danbooru.donmai.us"
    if trap == 'trap' and '-trap' in args:
        return "What are you trying to pull here? The dick only makes it better!"

    try:
        tags = f"tags={trap}+{'+'.join(args)}"
        rating = f"rating%3A{rating}"

        url = f"{base_url}/posts.json?{tags}+{rating}"
        r = requests.get(url)
        r = r.json()

        if 'success' in r:
            return r['message']

        return f"{random.choice(r)['large_file_url']}" if r else "Nothing to see here"

    except JSONDecodeError:
        fucked = r.text
        return fucked

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
