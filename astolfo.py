import discord
import random, os
import requests
from discord.ext.commands import Bot
from discord.voice_client import VoiceClient
from opus_loader import load_opus_lib
import functions
import re
import json
import pprint
import operator

from TwitterAPI import TwitterAPI
token = os.environ['discord_token']

tw_api = TwitterAPI(os.environ['tw_consumer_key'],
                    os.environ['tw_consumer_secret'],
                    os.environ['tw_access_token'],
                    os.environ['tw_access_token_secret'])
'''
token = config.token

tw_api = TwitterAPI(config.tw_consumer_key,
                    config.tw_consumer_secret,
                    config.tw_access_token,
                    config.tw_access_token_secret)
'''
traps_bot = Bot(command_prefix="?")
pp = pprint.PrettyPrinter()

@traps_bot.event
async def on_ready():
    print('Logged in as')
    print(traps_bot.user.name)
    print(traps_bot.user.id)
    print('------')
    load_opus_lib()
    await traps_bot.change_presence(game=discord.Game(name='Feminine Penises | ?commands'))


@traps_bot.command(pass_context=True)
async def joined_at(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    return await traps_bot.say('{0} joined at {0.joined_at}'.format(member))


@traps_bot.command(pass_context=True)
async def commands(ctx):
    member = ctx.message.channel
    em = discord.Embed(title='Commands', colour=0xFFC9E5)
    em.set_footer(text='The dick only makes it better!')
    em.add_field(name='Text', value='?backwards [text]\n?spam [text] [#]\n?vertical [text]\n?story [text]\n?retardo [text]')
    em.add_field(name='Gay', value='?safe\n?nsfw\n?doujin\n?privatefap\n?gay\n?notgay\n?gaypics')
    em.add_field(name='Reddit', value='?memes\n?animemes\n?clips\n?food\n?subreddit')
    em.add_field(name='Twitter', value='?tw_dl [tweet_url]\n')
    em.add_field(name='Misc', value='?chu\n?nafe\n?nafesfw')
    await traps_bot.send_message(member, embed=em)


@traps_bot.command()
async def notgay():
    gay_list = [
        "The dick only makes it better!",
        "It's not gay if it's cute",
        "It's a feminine dick"
    ]
    return await traps_bot.say(str(gay_list[random.randint(0, len(gay_list)-1)]))

@traps_bot.command()
async def gay():
    gay_list = [
        "Where's the dick?",
        "Look at that \"cute girl\""]
    return await traps_bot.say(random.choice(gay_list))


@traps_bot.command()
async def gaypics():
    path = "/app/files/gay_pics/"
    pic = random.choice(os.listdir(path))
    return await traps_bot.upload(path + pic)


@traps_bot.command()
async def chu():
    path = "/app/files/chu/"
    pic = random.choice(os.listdir(path))
    return await traps_bot.upload(path + pic)


@traps_bot.command()
async def spam(*args):
    text = ''
    for i in args[:-1]:
        text += i + ' '

    try:
        num = int(args[-1])
    except TypeError:
        return await traps_bot.say("Put a number at the end of your spam")

    row = (text * num )
    if num < 11:
        for i in range(0,num):
            await traps_bot.say(row)
    else:
        return await traps_bot.say("Nice try.")


@traps_bot.command()
async def vertical(*args):
    text = ''
    for i in args:
        text += i + ' '
    if len(text) > 50:
        return await traps_bot.say("Yea, no.")
    else:
        vertical_list = list(text)
        del vertical_list[0]
        final = text
        for i in vertical_list:
            final = final + "\n" + i
        return await traps_bot.say(final)


@traps_bot.command()
async def backwards(*args):
    final = ''
    for i in args:
        final += i + ' '
    return await traps_bot.say(final[::-1])


@traps_bot.command()
async def doujin():
    with open("/app/files/doujins.txt") as doujins:
        line = next(doujins)
        for num, aline in enumerate(doujins):
            if random.randrange(num + 2):
                continue
            line = aline
        return await traps_bot.say(line)


@traps_bot.command()
async def publicfap():
    with open("/app/files/doujins.txt") as doujins:
        line = next(doujins)
        for num, aline in enumerate(doujins):
            if random.randrange(num + 2):
                continue
            line = aline
        return await traps_bot.say(line)


@traps_bot.command(pass_context=True)
async def privatefap(ctx,):
    member = ctx.message.author
    with open("/app/files/doujins.txt") as doujins:
        line = next(doujins)
        for num, aline in enumerate(doujins):
            if random.randrange(num + 2):
                continue
            line = aline
        return await traps_bot.send_message(member, content=line)


@traps_bot.command()
async def story(*args):
    if not args:
        return await traps_bot.say('Create a story using 1 word per line. I will give you 10 seconds in between lines')
    else:
        args[0].split()
        final = args[0] + ' '
        limit = 100
        for i in range(limit):
            # multiple = i % 5
            # if multiple == 0:
                # await traps_bot.say("`"+str(limit - i)+ " lines remaining...`")
            msg = await traps_bot.wait_for_message(timeout=10)
            if msg:
                line = str(msg.content)
                first_arg = ''
                for char in line:
                    if char is ' ':
                        break
                    else:
                        first_arg += char
                final += first_arg + ' '
                continue
            else:
                break
        return await traps_bot.say(final)


@traps_bot.command()
async def subreddit(subreddit = None):
    if subreddit is None:
        return await traps_bot.say('Give me a subreddit!')
    headers = {'User-agent': 'traps-bot (by Keisakyu)'}
    url = "https://www.reddit.com/r/" + subreddit + ".json"
    for i in range(0, functions.subreddit_max_search):
        try:
            r = requests.get(url, headers=headers)
            r = r.json()
            if 'error' in r:
                if r['error'] == '404':
                    return await traps_bot.say("Something doesn't look right.")
            if not r['data']['children']:
                return await traps_bot.say('Looks pretty empty.')
            start = random.choice(r['data']['children'])
            first_suggestion = r['data']['children'][0]

            if 't5' in first_suggestion['kind']:
                return await traps_bot.say('Is this what you meant?\n' + "https://reddit.com" + first_suggestion ['data']['url'])
            else:
                posttype = start['data']['is_self']
                replacement = 'amp;'
                if not posttype:
                    pic = start['data']['url']
                    if replacement in pic:
                        pic = pic.replace(replacement, "")
                    return await traps_bot.say("Source:\n<https://www.reddit.com"+start['data']['permalink'] + ">\n\n" + pic)
                else:
                    continue
        except (KeyError, IndexError):
            return await traps_bot.say("Something doesn't look right.")


@traps_bot.command()
async def retardo(*args):
    total_text = ""
    retardo_string = ""
    for text in args:
        total_text += text.replace(" ", "")

    for index, char in enumerate(total_text):
        if index % 2 == 0:
            retardo_string += char.lower() + " "
        else:
            retardo_string += char.upper() + " "

    return await traps_bot.say(retardo_string)


@traps_bot.command(pass_context=True)
async def join(ctx,):
    author = ctx.message.author
    voice_con = traps_bot.join_voice_channel(author.voice.voice_channel)
    await voice_con


@traps_bot.command(pass_context=True)
async def leave(ctx,):
    author = ctx.message.author
    server = ctx.message.server
    voice_channel_name = author.voice.voice_channel
    voice_channel = discord.utils.get(ctx.message.server.channels, name=str(author.voice.voice_channel))
    print("voice channel: " + str(author.voice.voice_channel))
    print(traps_bot.is_voice_connected(server))
    await discord.utils.get(traps_bot.voice_clients, server=server).disconnect()


@traps_bot.command()
async def tw_dl(tw_url):
    tweet_id = re.findall('/\d+', tw_url)
    if len(tweet_id) != 1:
        return traps_bot.say("Try ?tw_dl [tweet_url]")
    tweet_id = tweet_id[0].replace("/", "")

    r = tw_api.request(f'statuses/show/:{tweet_id}')
    tweet_dict = json.loads(r.text)
    pp.pprint(tweet_dict)

    media_to_parse = []
    if 'media' in tweet_dict['entities']:
        media_to_parse.extend(tweet_dict['entities']['media'])

        if 'extended_entities' in tweet_dict:
            media_to_parse.extend(tweet_dict['extended_entities']['media'])

        media_to_parse.sort(key=operator.itemgetter('type'), reverse=True)
    else:
        return await traps_bot.say('No media was found in that tweet')

    media_list = []
    videos = []
    for media in media_to_parse:
        if 'video_info' in media:
            video_variants = media['video_info']['variants']
            for video_variant in video_variants:
                if 'bitrate' in video_variant:
                    videos.append(video_variant)

            # Grab highest bit rate video
            videos.sort(key=operator.itemgetter('bitrate'), reverse=True)
            media_list.append(videos[0]['url'])
            break
        else:
            media_list.append(media['media_url'])

    all_media = "\n".join(map(str, media_list))
    return await traps_bot.say(all_media)


@traps_bot.command()
async def safe(*args):
    return await traps_bot.say(functions.gelbooru_image_search("safe",  "trap", *args))


@traps_bot.command()
async def nsfw(*args):
    return await traps_bot.say(functions.gelbooru_image_search("explicit",  "trap", *args))


@traps_bot.command()
async def nafe(*args):
    return await traps_bot.say(functions.gelbooru_image_search("safe",   *args))


@traps_bot.command()
async def nafesfw(*args):
    return await traps_bot.say(functions.gelbooru_image_search( "explicit",   *args))


@traps_bot.command()
async def memes():
    return await traps_bot.say(functions.subreddit_search(['dankmemes', 'me_irl']))


@traps_bot.command()
async def animemes():
    return await traps_bot.say(functions.subreddit_search(['animemes', 'anime_irl']))


@traps_bot.command()
async def food():
    return await traps_bot.say(functions.subreddit_search(['shittyfoodporn']))


@traps_bot.command()
async def clips():
    return await traps_bot.say(functions.subreddit_search(['livestreamfail']))




traps_bot.run(token)
