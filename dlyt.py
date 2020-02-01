#!/usr/bin/env python3

import os
import glob
import pathlib
from subprocess import Popen

def deduplicate(some_list):
  return list(dict.fromkeys(some_list))

options = {}
lists = glob.glob(os.getcwd()+'/playlists/*')
magicLink = 'https://www.youtube.com/watch?v='

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
del itemnum
del opt

songlist = open(options['playlist'], 'r')
opensonglist = songlist.readlines()
songs = [x.rstrip() for x in opensonglist if x[0] != '#']
list_length = len(songs)
songlist.close()

master_archive_read = open(f'{os.getcwd()}/archive_files/master_archive.txt', 'r+')
master_archive = [item.rstrip().split() for item in list(master_archive_read.readlines())]
grab_lists = [item.replace(os.getcwd()+'/playlists/', '').replace('.txt', '').replace('.local', '') for item in list(glob.glob(os.getcwd()+'/playlists/*')) if '.local' in item]
to_grab = {name : [] for name in grab_lists}

to_add = []

playlist_name = options['playlist'].replace(f'{os.getcwd()}/playlists/', '').replace('.txt', '').replace('.bkup', '')
for item in songs:
    exists = False
    for song in master_archive:
        if item[-11:] == song[1]:
            print(f'{item} already in archive, skipping and adding later.')
            to_grab[song[0]].append(song[1])
            exists = True
            #Guarantee only one append
            break

    if exists:
        continue
    else: 
        to_add.append(item[-11:])

    print(f'Downloading song {songs.index(item)+1} out of {list_length}')
    command = f'youtube-dl -f bestaudio --restrict-filename --download-archive {os.getcwd()}/archive_files/{playlist_name}_archive.txt {magicLink}{item.replace("https://youtu.be/", "", 1)} -o "~/Music/{playlist_name}/%(title)s_%(id)s.%(ext)s"'
    p = Popen([command], shell=True)
    p.wait()

while True:
    option = input(f'Write to: {options["playlist"].replace(".bkup", "")}.bkup? (Y/n): ')
    if option.lower() in ['y', 'yes']:
        command = f'mv {options["playlist"]} {options["playlist"].replace(".bkup", "")}.bkup'
        p = Popen([command], shell=True)
        p.wait()
        break
    else: break

new_list = open(f'{options["playlist"].replace(".bkup", "").replace(".txt", "")}.local.txt', 'w+')
for item in glob.glob(f'{pathlib.Path.home()}/Music/{playlist_name}/*.*'):
    new_list.write(f'file://{item}\n')

for source in list(to_grab.keys()):
    grab_archive = open(f'{os.getcwd()}/playlists/{source}.local.txt', 'r')
    for link in list(grab_archive.readlines()):
        songs_left = deduplicate(to_grab[source])
        for song in songs_left:
            if song in link:
                new_list.write(link)
                to_grab[source].remove(song)
    grab_archive.close()
new_list.close()

master_archive_read.seek(0, os.SEEK_END)
for item in to_add:
    master_archive_read.write(f'{playlist_name} {item[-11:]}\n')
master_archive_read.close()
