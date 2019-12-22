import os
import glob
import pathlib
from subprocess import Popen

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

playlist_name = options['playlist'].replace(f'{os.getcwd()}/playlists/', '').replace('.txt', '').replace('.bkup', '')
for item in songs:
    print(f'Downloading song {songs.index(item)+1} out of {list_length}')
    command = f'youtube-dl -f bestaudio --restrict-filename --download-archive {os.getcwd()}/archive_files/{playlist_name}_archive.txt {magicLink}{item.replace("https://youtu.be/", "", 1)} -o "~/Music/{playlist_name}/%(title)s_%(id)s.%(ext)s"'
    p = Popen([command], shell=True)
    p.wait()
del command

while True:
    option = input(f'Write to: {options["playlist"].replace(".bkup", "")}.bkup? (Y/n): ')
    if option.lower() in ['y', 'yes']:
        command = f'mv {options["playlist"]} {options["playlist"].replace(".bkup", "")}.bkup'
        p = Popen([command], shell=True)
        p.wait()
        break
    else: break

new_list = open(options['playlist'].replace('.bkup', ''), 'w+')
for item in glob.glob(f'{pathlib.Path.home()}/Music/{playlist_name}/*.*'):
    new_list.write(f'file://{item}\n')
new_list.close()