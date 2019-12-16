#!/usr/bin/env python3
import os
import sys
import secrets
from subprocess import Popen, STDOUT, PIPE

index = 0

while True:
    opt = input('Randomize play order? (Y/n): ').lower()
    if opt in ['yes', 'y']:
        randomize = True
        break
    elif opt in ['', ' ', '  ']:
        continue 
    else: 
        randomize = False
        break

while True:
    opt = input('Play without video? (Y/n): ').lower()
    if opt in ['yes', 'y']:
        novideo = True
        break
    elif opt in ['', ' ', '  ']:
        continue
    else:
        novideo = False
        break

while True:
    try:
        songlist = open('songlist.txt', 'r')
        opensonglist = songlist.readlines()
        songs = [x.rstrip() for x in opensonglist]

        if randomize:
            index = secrets.randbelow(len(songs))

        string = f'cvlc {songs[index]} --play-and-exit'

        if novideo:
            string += ' --novideo'

        print(f'Playing index: {index+1}')
        p = Popen([string], shell=True)
        songlist.close()
        p.wait()

        if not randomize:
            if index == len(songs):
                index = 0
            else: index += 1

    except KeyboardInterrupt:
        sys.exit(0)