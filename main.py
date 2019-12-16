#!/usr/bin/env python3
import os
import sys
from subprocess import Popen, STDOUT, PIPE

index = 0
while True:
    try:
        songlist = open('songlist.txt', 'r')
        opensonglist = songlist.readlines()
        songs = [x.rstrip() for x in opensonglist]
        p = Popen([f'cvlc {songs[index]} --play-and-exit'], shell=True)
        songlist.close()
        p.wait()

        if index == len(songs):
            index = 0
        else: index += 1

    except KeyboardInterrupt:
        sys.exit(0)