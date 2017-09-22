import random
import requests
import xml.etree.ElementTree as ET

subreddit_max_search = 5


def gelbooru_image_search(rating, trap="",  *args):
    try:
        tags = f"-asian+-non-asian+rating%3a{rating}+{trap}"
        for i in args:
            if trap == 'trap' and '-trap' in i.lower():
                    return "What are you trying to pull here? The dick only makes it better!"
            else:
                tags += "+" + i

        if not args:
            pid = random.randint(0, 100)
        else:
            pid = ""

        url = f"http://gelbooru.com/index.php?page=dapi&s=post&q=index&tags={tags}&pid={pid}"
        print(url)
        r = requests.post(url, stream=True)
        r.raw.decode_content = True
        events = ET.iterparse(r.raw)
        pic = []

        for event, elem in events:
            pic.append(elem)
        del pic[-1]
        pic = random.choice(pic)
        pic = pic.attrib
        return pic['file_url']
    except IndexError:
        return "Nice command."

def subreddit_search(subreddit_list):
    headers = {'User-agent': 'traps-bot (by Keisakyu)'}
    url = "https://www.reddit.com/r/" + random.choice(subreddit_list) + ".json"
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
