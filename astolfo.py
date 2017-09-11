import discord
import random, os
import requests
from discord.ext.commands import Bot
from opus_loader import load_opus_lib
import functions
import re
import json
import operator
import pprint
from time import (strftime, gmtime)

from trap_dict import (number_emoji_dict, gay_message_dict)
from TwitterAPI import TwitterAPI

import config

token = config.token
tw_api = TwitterAPI(config.tw_consumer_key,
                    config.tw_consumer_secret,
                    config.tw_access_token,
                    config.tw_access_token_secret)


traps_bot = Bot(command_prefix="?")
bot_name = "Traps Aren't Gay"
player = None
pp = pprint.PrettyPrinter()


@traps_bot.event
async def on_ready():
    print('Logged in as')
    print(traps_bot.user.name)
    print(traps_bot.user.id)
    print('------')
    load_opus_lib()
    await traps_bot.change_presence(game=discord.Game(name="?commands"))
    print('dicks')


@traps_bot.event
async def on_message(message):
    gay_list = ['gay', 'fag', 'homo']
    message_formatted = message.content.replace(" ", "").lower()

    for replace_str, replacer in gay_message_dict.items():
        message_formatted = message_formatted.replace(replace_str, replacer)

    message_formatted = re.sub('[][!@#$%^&*(){}\-_=+`~|.,<>/;:\'\"]', '', message_formatted)

    message_formatted_reversed = message_formatted[::-1]
    if any(x in message_formatted for x in gay_list) and message.author.name != bot_name and not str(message).startswith('?'):
        await traps_bot.send_message(message.channel, "Not gay")

    if any(x in message_formatted_reversed for x in gay_list) and message.author.name != bot_name and not str(message).startswith('?'):
        await traps_bot.send_message(message.channel, "yag toN")

    await traps_bot.process_commands(message)


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
    em.add_field(name='Music', value='?play [url]\n?volume [#]\n?np')
    em.add_field(name='Misc', value='?chu\n?nafe\n?nafesfw\n?roll')
    return await traps_bot.send_message(member, embed=em)


@traps_bot.command()
async def roll():
    number = random.randint(1, 100)
    roll_text = ''
    for x in str(number):
        roll_text += number_emoji_dict[x]

    if number == 100:
        roll_text += ":confetti_ball: :confetti_ball: :confetti_ball:"

    return await traps_bot.say(roll_text)


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
    path = "./files/gay_pics/"
    pic = random.choice(os.listdir(path))
    return await traps_bot.upload(path + pic)


@traps_bot.command()
async def chu():
    path = "./files/chu/"
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
        for i in range(0, num):
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
    with open("./files/doujins.txt") as doujins:
        line = next(doujins)
        for num, aline in enumerate(doujins):
            if random.randrange(num + 2):
                continue
            line = aline
        return await traps_bot.say(line)


@traps_bot.command()
async def publicfap():
    with open("./files/doujins.txt") as doujins:
        line = next(doujins)
        for num, aline in enumerate(doujins):
            if random.randrange(num + 2):
                continue
            line = aline
        return await traps_bot.say(line)


@traps_bot.command(pass_context=True)
async def privatefap(ctx,):
    member = ctx.message.author
    with open("./files/doujins.txt") as doujins:
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
            print(url)
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
    if not args:
        return await traps_bot.say("I suggest giving me a message to retardify")

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
async def join(ctx, *channel_name):
    author = ctx.message.author
    server = ctx.message.server

    channel_name = " ".join(channel_name)

    voice_channel = discord.utils.get(ctx.message.server.channels, name=channel_name, type=discord.ChannelType.voice) if channel_name else author.voice.voice_channel

    if not author.voice.voice_channel and not channel_name:
        return await traps_bot.say("You should join a voice channel first! Or you could specify a channel name")

    if not voice_channel:
        return await traps_bot.say(f"{channel_name} is not a voice channel")

    if traps_bot.is_voice_connected(server):
        await discord.utils.get(traps_bot.voice_clients).disconnect()

    return await traps_bot.join_voice_channel(voice_channel)


@traps_bot.command(pass_context=True)
async def leave(ctx,):
    server = ctx.message.server

    if not traps_bot.is_voice_connected(server):
        return await traps_bot.say("Leave what?")

    return await discord.utils.get(traps_bot.voice_clients).disconnect()


@traps_bot.command()
async def tw_dl(*args):
    if not args:
        return await traps_bot.say("Give me a tweet url")
    tw_url = args[0]
    params = {
        'include_entities': True,
        'include_ext_alt_text': True,
        'tweet_mode': 'extended'
    }

    tweet_id = re.findall('/\d+$', tw_url)
    print(tweet_id)
    if len(tweet_id) != 1:
        return await traps_bot.say("Try ?tw_dl [tweet_url]")
    tweet_id = tweet_id[0].replace("/", "")

    r = tw_api.request(f'statuses/show/:{tweet_id}', params)
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
            if media['media_url'] not in media_list:
                media_list.append(media['media_url'])

    all_media = "\n".join(map(str, media_list))
    return await traps_bot.say(all_media)


@traps_bot.command(pass_context=True)
async def play(ctx, *args):
    if not args:
        return await traps_bot.say("gib url")

    author = ctx.message.author
    server = ctx.message.server

    voice = await traps_bot.join_voice_channel(author.voice.voice_channel) if not traps_bot.is_voice_connected(server) else discord.utils.get(traps_bot.voice_clients)

    global player

    if not player:
        player = await voice.create_ytdl_player(args[0])
        player.volume = 0.05
        player.start()
    return


@traps_bot.command(pass_context=True)
async def volume(ctx, *args):
    server = ctx.message.server

    if not traps_bot.is_voice_connected(server):
        return await traps_bot.say("Put me into a voice channel first!")

    if not args:
        return await traps_bot.say("Enter a volume between 1 - 200")

    try:
        vol = args[0]
        int(vol)
        global player
        if player and 1 <= int(args[0]) <= 200:
            player.volume = int(args[0]) / 100
            volume_string = ''
            if int(vol) == 69:
                volume_string = ':cancer:'
            elif int(vol) == 200:
                volume_string = ':regional_indicator_m: :regional_indicator_a: :regional_indicator_x: '
            else:
                for num in list(str(vol)):
                    volume_string += number_emoji_dict[num]

            return await traps_bot.say(f":speaker: {volume_string}")

        elif not player:
            return await traps_bot.say("Play something first!")

        else:
            return await traps_bot.say("Enter a volume between 1 - 200")

    except (TypeError, ValueError):
        return await traps_bot.say("Enter a valid number")


@traps_bot.command(pass_context=True)
async def np(ctx, *args):
    global player
    if player:
        duration = strftime("%M:%S", gmtime(player.duration))
        return await traps_bot.say(f"Now Playing:```\n{player.title}\n{duration}```")

    else:
        return traps_bot.say("There is nothing playing")


@traps_bot.command(pass_context=True)
async def stop(ctx,):
    global player
    if player:
        player.stop()
        return await traps_bot.say(":musical_note: :gun:")
    else:
        return traps_bot.say("There is nothing playing!")


@traps_bot.command(pass_context=True)
async def pause(ctx,):
    global player
    if player:
        player.pause()
        return await traps_bot.say(":musical_note: :octagonal_sign:")
    else:
        return traps_bot.say("There is nothing playing!")


@traps_bot.command(pass_context=True)
async def resume(ctx,):
    global player
    if player:
        player.resume()
        return await traps_bot.say(":musical_note: :ok:")
    else:
        return traps_bot.say("There is nothing playing!")


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

traps_bot.remove_command('help')
traps_bot.run(token)
