#!/usr/bin/env python3
import os
import sys
import secrets
import glob
import time
import random
import re
from subprocess import Popen, STDOUT, PIPE


def formatDuration(duration):
    time_played = {'Week': int(duration/604800), 'Day': int((duration % 604800)/86400), 'Hour': int(
        (duration % 86400)/3600), 'Minute': int((duration % 3600)/60), 'Second': int((duration % 60))}
    to_print = ''
    for amount in time_played.keys():
        value = time_played[amount]
        if value > 0:
            to_print += f' {str(value)} '
            to_print += amount
            if value > 1:
                to_print += 's'
    return(to_print)


start_time = time.time()
last_time = time.time()
index = 0
magicLink = 'https://www.youtube.com/watch?v='
options = {'randomize': False, 'pseudorandom': False, 'novideo': False,
           'localAudio': False, 'pickIndex': False, 'playlist': ''}
queries = {'randomize': 'Randomize play order? (Y/n): ',
           'pseudorandom': 'Play in pseudorandom mode? (Y/n): ',
           'novideo': 'Play without video? (Y/n): ',
           'localAudio': 'Play playlist from local Music folder? (Y/n): '}
for i in queries.keys():
    while True:
        opt = input(queries[i]).lower()
        if len(opt) == 0:
            continue
        if opt[0] not in ['y', 'n']:
            continue
        elif opt[0] == 'y':
            options[i] = True
            break
        else:
            options[i] = False
            break

while not options['randomize']:
    opt = input('Choose specific indices? (Y/n): ').lower()
    if len(opt) == 0:
        continue
    if opt[0] not in ['y', 'n']:
        continue
    elif opt[0] == 'y':
        options['pickIndex'] = True
        break
    else:
        options['pickIndex'] = False
        break

lists = glob.glob(os.getcwd()+'/playlists/*')
if options['localAudio']:
    lists = [item for item in lists if '.local' in item]
else:
    lists = [item for item in lists if '.local' not in item]

while True:
    for itemnum in range(len(lists)):
        print(itemnum, lists[itemnum].replace(
            f'{os.getcwd()}/playlists/', '').replace('.txt', '').replace('.bkup', '').replace('.local', ''))
    opt = input('Choose playlist num: ')
    if len(opt) == 0:
        continue
    if opt not in [str(x) for x in range(len(lists))]:
        continue
    else:
        options['playlist'] = lists[int(opt)]
        break

songlist = open(options['playlist'], 'r')
opensonglist = songlist.readlines()
songs = [x.rstrip() for x in opensonglist if x[0] != '#']

if options['pseudorandom']:
    pseudorandom = list(range(len(songs)))

chosen = options["playlist"].replace(os.getcwd()+'/playlists/', '').replace('.txt', '').replace('.bkup', '').replace('.local', '')

while True:
    try:

        if options['pseudorandom']:
            index = random.choice(pseudorandom)
            pseudorandom.remove(index)
        elif options['randomize']:
            index = secrets.randbelow(len(songs))
        elif options['pickIndex']:
            while True:
                try:
                    inp = int(input(f'Pick an index under {len(songs)}: '))
                    if inp >= len(songs):
                        print(f'Please enter a number under {len(songs)}')
                    else:
                        index = inp
                        break
                except ValueError:
                    print(f'Please enter a number under {len(songs)}')

        if 'https://youtu' in songs[index]:
            formatted_link = f'{magicLink}{songs[index].replace("https://youtu.be/", "", 1)}'
        else:
            formatted_link = songs[index]

        command = f'cvlc {formatted_link} --play-and-exit'

        if options['novideo']:
            command += ' --novideo'

        if 'https://youtu' not in songs[index]:
            print(f'Playing index {index}: ' + re.search(
                r'(?:\/)(?!.*\/)(?P<name>.+).{12}\..*$', songs[index]).group("name").replace('_', ' '))
        else:
            print(f'Playing index: {index}')

        p = Popen([command], shell=True)
        songlist.close()
        p.wait()
        time.sleep(2)

        if not options['randomize']:
            if index == len(songs):
                index = 0
            else:
                index += 1

        if len(pseudorandom) == 0:
            pseudorandom = list(range(len(songs)))

        print(
            f'Played playlist "{chosen}" for: {formatDuration(time.time()-start_time)}')

    except KeyboardInterrupt:
        duration = time.time()-start_time
        to_print = formatDuration(duration)
        print(
            f'Played playlist "{chosen}" for: {to_print}')
        sys.exit(0)
