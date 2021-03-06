import json
import operator
import os
import pprint
import random
import re
from datetime import datetime
from time import (strftime, gmtime)

import certifi
import discord
import requests
import urllib3
from TwitterAPI import TwitterAPI
from bs4 import BeautifulSoup
from discord.ext.commands import Bot
from fuzzywuzzy import process
# from opus_loader import load_opus_lib
from pytz import timezone
from tinydb import TinyDB, Query
from unidecode import unidecode

import config
import functions
from connect_4 import Connect4
from tictactoe import TicTacToe
from trap_dict import *

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
    print(traps_bot.user)
    print('------')
    #load_opus_lib()
    await traps_bot.change_presence(game=discord.Game(name="?commands"))
    print('dicks')


@traps_bot.event
async def on_message(message):
    if not message.content.startswith("?"):
        gay_list = ['gay', 'fag', 'homo']
        message_formatted = message.content.replace(" ", "").lower()

        for replace_str, replacer in gay_message_dict.items():
            message_formatted = message_formatted.replace(replace_str, replacer)

        message_formatted = re.sub('[][!@#$%^&*(){}\-_=+`~|.,<>/;:\'\"]', '', message_formatted)

        message_formatted_reversed = message_formatted[::-1]
        if any(unidecode(x) in message_formatted for x in gay_list) and message.author.name != bot_name:
            await traps_bot.send_message(message.channel, "Not gay")

        if any(unidecode(x) in message_formatted_reversed for x in gay_list) and message.author.name != bot_name:
            await traps_bot.send_message(message.channel, "yag toN")

    await traps_bot.process_commands(message)


@traps_bot.command(pass_context=True)
async def joined_at(ctx, member: discord.Member = None):
    if member is None:
        member = ctx.message.author

    return await traps_bot.say(f'{member} joined at {member.joined_at}')


@traps_bot.command(pass_context=True)
async def commands(ctx):
    member = ctx.message.channel
    em = discord.Embed(title='Commands', colour=0xFFC9E5)
    em.set_footer(text='The dick only makes it better!')
    for key, command_name in commands_dict.items():
        em.add_field(name=key, value='\n'.join(command_name))

    return await traps_bot.send_message(member, embed=em)


@traps_bot.command(pass_context=True)
async def nationalday(ctx):
    member = ctx.message.channel

    db = TinyDB('national_days.json')
    national_days = Query()

    today_tz = datetime.now(timezone('US/Eastern'))
    today_db = today_tz.strftime("%Y-%m-%d")
    today_title = today_tz.strftime("%B %d")

    em = discord.Embed(colour=0xFFC9E5)
    em.add_field(name=f'{today_title}', value=db.search(national_days.date == today_db)[0]['national_days'])

    return await traps_bot.send_message(member, embed=em)


@traps_bot.command()
async def roll():
    number = random.randint(1, 100)
    roll_text = ''
    for x in str(number):
        roll_text += number_emoji_dict[x]

    if number == 100:
        roll_text += ":confetti_ball: " * 3

    return await traps_bot.say(roll_text)


@traps_bot.command()
async def gay():
    path = "./files/gay_pics/"
    pic = random.choice(os.listdir(path))
    return await traps_bot.upload(path + pic)


@traps_bot.command()
async def chu():
    path = "./files/chu/"
    pic = random.choice(os.listdir(path))
    return await traps_bot.upload(path + pic)


@traps_bot.command()
async def dab():
    pic = os.path.join("./files/gif", "carl_dab.gif")
    return await traps_bot.upload(pic)


@traps_bot.command()
async def spam(*args):
    if not args:
        return await traps_bot.say("Give me some spam and a number!")

    text = ' '.join(args[:-1]) + ' '

    try:
        num = int(args[-1])
    except (TypeError, ValueError):
        return await traps_bot.say("Put a number at the end of your spam!")

    row = (text * num)
    if num < 11:
        for i in range(0, num):
            await traps_bot.say(row)
    else:
        return await traps_bot.say("Nice try.")


@traps_bot.command()
async def vertical(*args):
    if not args:
        return traps_bot.say('Give me something to say vertically!')
    text = ' '.join(args)
    print(text)

    if len(text) > 50:
        return await traps_bot.say("Yea, no.")

    vertical_list = list(text)[1:]
    text += '\n'
    text += '\n'.join(vertical_list)

    return await traps_bot.say(text)


@traps_bot.command()
async def backwards(*args):
    if not args:
        return await traps_bot.say('Give me something to say backwards!')

    text = ' '.join(args)

    return await traps_bot.say(text[::-1])


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
            if not r['data']['children']:
                return await traps_bot.say('Looks pretty empty.')
            start = random.choice(r['data']['children'])
            first_suggestion = r['data']['children'][0]

            if 't5' in first_suggestion['kind']:
                return await traps_bot.say('Is this what you meant?\n'
                                           + "https://reddit.com" + first_suggestion ['data']['url'])
            else:
                posttype = start['data']['is_self']
                replacement = 'amp;'
                if not posttype:
                    pic = start['data']['url']
                    if replacement in pic:
                        pic = pic.replace(replacement, "")
                    return await traps_bot.say("Source:\n<https://www.reddit.com"
                                               + start['data']['permalink'] + ">\n\n" + pic)
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
    if len(tweet_id) != 1:
        return await traps_bot.say("Try ?tw_dl [tweet_url]")
    tweet_id = tweet_id[0].replace("/", "")

    r = tw_api.request(f'statuses/show/:{tweet_id}', params)
    tweet_dict = json.loads(r.text)

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

'''
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
'''

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


@traps_bot.command(pass_context=True)
async def embed_test(ctx,):
    pass


@traps_bot.command(pass_context=True)
async def connect4(ctx, player2_id):
    def check(msg):
        try:
            num = int(msg.content)
            if 1 <= num <= 7:
                return True
        except:
            return False

    column_full_message = None
    player1 = ctx.message.author
    player2 = re.findall(r'\d+', player2_id)[0]
    for x in ctx.message.server.members:
        if int(x.id) == int(player2):
            player2 = x
            break

    c4 = Connect4(player1.name, player2.name)

    previous_board = await traps_bot.say(c4.create_board())
    #await traps_bot.say(player1.avatar_url)
    while True:
        drop_piece_to_column = await traps_bot.wait_for_message(timeout=600, author=discord.utils.get(ctx.message.server.members, name=c4.players_turn), check=check)

        if column_full_message:
            await traps_bot.delete_message(column_full_message)
            column_full_message = None

        await traps_bot.delete_message(drop_piece_to_column)
        success = c4.drop_piece(int(drop_piece_to_column.content))

        if not c4.check_for_win() and not column_full_message:
            c4.switch_players_turn()

        if not success:
            column_full_message = await traps_bot.say('That column is full! Pick another column')
            continue
        else:
            counter = 0
            async for x in traps_bot.logs_from(ctx.message.channel, limit=5):
                if x.id == previous_board.id and counter == 0:
                    await traps_bot.edit_message(previous_board, new_content=c4.create_board())
                else:
                    await traps_bot.delete_message(previous_board)
                    previous_board = await traps_bot.say(c4.create_board())
                if c4.number_of_pieces_played == c4.rows * c4.columns:
                    return await traps_bot.say('Draw!')
                break

        if c4.check_for_win():
            return await traps_bot.say(f'{c4.players_turn} wins! :confetti_ball:')


@traps_bot.command(pass_context=True, aliases=["ttt"])
async def tictactoe(ctx, player2_id):
    def check(msg):
        msg = msg.content
        try:
            assert len(msg) == 2
            assert msg[0].isalpha()
            assert 0 < ord(msg[0].lower()) - 96 <= 3
            num = int(msg[1])
            assert 0 < num <= 3
            return True

        except AssertionError:
            return False

    player1 = ctx.message.author
    player2 = re.findall(r'\d+', player2_id)[0]
    player2 = next(x for x in ctx.message.server.members if int(x.id) == int(player2))

    ttt = TicTacToe(player1.name, player2.name)

    successful_placement = True
    previous_board = None
    messages_to_delete = []
    while True:
        if len(messages_to_delete) >= 8:
            await traps_bot.delete_messages(messages_to_delete)

        if successful_placement:
            msg = f"{ttt.create_board()}{ttt.players_turn} is {ttt.current_players_piece}. Your turn"
            if previous_board:
                previous_board = await traps_bot.edit_message(previous_board, new_content=msg)
            else:
                previous_board = await traps_bot.say(msg + f"\n")

        author = discord.utils.get(ctx.message.server.members, name=ttt.players_turn)
        board_position = await traps_bot.wait_for_message(timeout=600, author=author, check=check)
        successful_placement = ttt.place_piece(board_position.content[1], (ord(board_position.content[0].lower()) - 96))
        messages_to_delete.append(board_position)

        if successful_placement is False:
            messages_to_delete.append(await traps_bot.say(f"`{board_position.content.upper()}` is already taken!"))
            continue

        if len(messages_to_delete) > 1:
            await traps_bot.delete_messages(messages_to_delete)
        else:
            await traps_bot.delete_message(messages_to_delete[0])

        if ttt.num_of_pieces_played >= ttt.rows * ttt.columns:
            return await traps_bot.say(f"{ttt.create_board()}\nDraw!")

        if ttt.turn_count >= 3 and ttt.check_for_win():
            await traps_bot.delete_message(previous_board)
            return await traps_bot.say(ttt.create_board() + f"\n{ttt.players_turn} wins! :confetti_ball:")

        ttt.switch_players_turn()


@traps_bot.command()
async def nhentai(*tags):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), maxsize=1, timeout=5)
    url = search_url = 'https://nhentai.net/'
    if tags:
        search_url += 'search/?q=' + '+'.join(tag.replace("_", "-") for tag in tags)
    r = http.request('GET', search_url)
    soup = BeautifulSoup(r.data, 'html.parser')
    #last_page = soup.find('a', class_='last').get('href').split('page=')[1]

    images = [i.get('href') for i in soup.find_all('a', attrs={'class': 'cover'})]

    try:
        return await traps_bot.say(url + random.choice(images)[1:])
    except IndexError:
        return await traps_bot.say("No hentai found!")


@traps_bot.command()
async def tdoll(*name):
    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where(), maxsize=1, timeout=5)
    base_url = "https://en.gfwiki.com"
    url_index = 'https://en.gfwiki.com/wiki/T-Doll_Index'

    # if name:
    #     search_url += 'search/?q=' + '+'.join(tag.replace("_", "-") for tag in tags)
    r = http.request('GET', url_index)
    soup = BeautifulSoup(r.data, 'html.parser')

    tdolls = [i.contents[0].contents[0].get("href") for i in soup.find_all('div', attrs={'class': 'card-bg-small'})]

    tdoll_choice = base_url + random.choice(tdolls)

    if name:
        prefix = "/wiki/"
        matches = process.extract(prefix + name[0], tdolls)
        # sorted(matches, key=lambda x: x[1])
        best_match = matches[0]
        print(matches)

        if best_match[1] >= 90:
            tdoll_choice = base_url + best_match[0]

        else:
            return await traps_bot.say(f"Did you mean {best_match[0].replace(prefix, '')}?")

    return await traps_bot.say(tdoll_choice)


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
    return await traps_bot.say(functions.gelbooru_image_search("explicit",   *args))


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
