import random
import requests

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

