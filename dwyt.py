import os
import glob
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


songlist = open(options['playlist'], 'r')
opensonglist = songlist.readlines()
songs = [x.rstrip() for x in opensonglist if x[0] != '#']
songlist.close()

playlist_name = lists[itemnum].replace(f'{os.getcwd()}/playlists/', '').replace('.txt', '').replace('.bkup', '')
for item in songs:
    command = f'youtube-dl -s -f bestaudio --restrict-filename --download-archive {os.getcwd()}/archive_files/{playlist_name}_archive.txt {magicLink}{item.replace("https://youtu.be/", "", 1)} -o "~/Music/{playlist_name}/%(title)s_%(id)s.%(ext)s"'
    print(command)
    p = Popen([command], shell=True)
    p.wait()

command = f'mv {options["playlist"].replace(".bkup", "")} {options["playlist"].replace(".bkup", "")}.bkup'
p = Popen([command], shell=True)
p.wait()

new_list = open(options['playlist'].replace('.bkup', ''), 'w+')
print(glob.glob(f'~/Music/{playlist_name}/*'))
for item in glob.glob(f'~/Music/{playlist_name}/*'):
    print(item)
    new_list.write(f'file://{item}\n')
new_list.close()