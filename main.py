#!/usr/bin/env python3
import os
import sys
import secrets
import glob
import time
from subprocess import Popen, STDOUT, PIPE

start_time = time.time()
index = 0
magicLink = 'https://www.youtube.com/watch?v='
options = {'randomize': False, 'novideo': False,
           'pickIndex': False, 'playlist': ''}
queries = {'randomize': 'Randomize play order? (Y/n): ',
           'novideo': 'Play without video? (Y/n): '}
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

lists = glob.glob(os.getcwd()+'/playlists/*.txt')

while True:
    for itemnum in range(len(lists)):
        print(itemnum, lists[itemnum].replace(
            f'{os.getcwd()}/playlists/', '').replace('.txt', ''))
    opt = input('Choose playlist num: ')
    if len(opt) == 0:
        continue
    if opt not in [str(x) for x in range(len(lists))]:
        continue
    else:
        options['playlist'] = lists[int(opt)]
        break

while True:
    try:
        songlist = open(options['playlist'], 'r')
        opensonglist = songlist.readlines()
        songs = [x.rstrip() for x in opensonglist if x[0] != '#']

        if options['randomize']:
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

        print(f'Playing index: {index}')
        if 'https://youtu' not in songs[index]:
            print(''.join(songs[index].replace('_', ' ').split(' ')[0, -1]))

        p = Popen([command], shell=True)
        songlist.close()
        p.wait()

        if not options['randomize']:
            if index == len(songs):
                index = 0
            else:
                index += 1
    except KeyboardInterrupt:
        duration = time.time()-start_time
        time_played = {'Week':int(duration/604800), 'Day':int((duration%604800)/86400), 'Hour':int((duration%86400)/3600), 'Minute':int((duration%3600)/60), 'Second':int((duration%60))}
        to_print = ''
        for amount in time_played.keys():
            value = time_played[amount]
            if value > 0:
                to_print += f' {str(value)} '
                to_print += amount
                if value > 1:
                    to_print += 's'

        print(f'Played for:{to_print}')
        sys.exit(0)
