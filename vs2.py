#!/usr/bin/env python
''' sauerbraten launcher
    flow:
            switch sound to headphones
            get last map played from log
            get current map from log
            write aex.cfg
            prompt for map selection
            play game
            prompt:
                    advance selection?
            restore sound to original card
'''
import os
import subprocess
import re
import random

import sauertools

SAUERDIR="/opt/sauerbraten/"
AUTOEXEC = "/home/vic/.sauerbraten/autoexec.cfg"
LOG = "/home/vic/.sauerbraten/sauer.vlog"
maps = sauertools.maps
aex = sauertools.aexfile

TEST = 'yessiree bob!'

D = {'LAST_MAP_PLAYED': "map",
     'RANDOM_MAP': "random",
     'CURRENT_MAP': 'current',
     'MAP_LIST_INDEX': 1,
     }


def bail():
    print("oopsie!")
    quit()


def retrieve_last_map():
    #  print("\n\n*** getting map name from log file ***\n\n")
    name = ""
    with open(LOG, "r") as log:
        #  rx1 = re.compile('read map packages/base/(.*)\.ogz.*')
        before = "read map packages/base/"
        after = "\.ogz.*"
        rxstring = before + "(.*)" + after
        rx = re.compile(rxstring)
        for line in log:
            #print(line[:-1])
            m = rx.match(line)
            if m:
                name = m.groups()[0]
                #  print("name: {} ".format(name))

    # names is a list of tuples, so
    return name if name else "hashi"


def retrieve_index():
    print("\n\n*** getting index from autoexec.cfg ***\n\n")
    idx = -1
    rx = re.compile('#current_index:(\d+)\s*')
    with open(AUTOEXEC, 'r') as x:
        for line in x:
            #  print(line)
            m = rx.match(line)
            if m:
                print(line)
                idx = int(m.groups()[0])
                #  print("current map at index {}: {}".format(idx, maps[idx]))
                #  print("idx: [{}] ".format(idx))
        return idx if idx > -1 else bail()


class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)

    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)

    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)
        #  fix_display_args = ["xrandr" , "--output", "DVI-I-1",  "--mode",  "1920x1080"]
        #x = subprocess.Popen(fix_display_args)


def multiple_replace(text, adict):
    rx = re.compile('|'.join(map(re.escape, adict)))

    def one_xlat(match):
        return adict[match.group(0)]
    return rx.sub(one_xlat, text)


def end_prompt():
    print("\n\n*** entering end_prompt ***\n\n")
    while True:
        current_map = maps[int(D['MAP_LIST_INDEX'])]
        next_map = maps[int(D['MAP_LIST_INDEX']) + 1]
        print("current_map: {}\nmext map: {}".format(current_map, next_map))
        response = raw_input("advance to next?[y/N]")
        if response == 'y':
            print('advancing startup map')
            D['MAP_LIST_INDEX'] = str(int(D['MAP_LIST_INDEX']) + 1)
            return
        else:
            print('keeping current startup map')
            return


def launch():
    print("in launch")
    args = ['./sauerbraten_unix']
    with cd(SAUERDIR):
            with open(LOG, 'w') as out:
                    p = subprocess.Popen(args, stdout=out, stderr=out)
                    p.wait()

if __name__ == "__main__":
    sauertools.switcher()
    D['MAP_LIST_INDEX'] = str(retrieve_index())
    launch()
    sauertools.restore()
    D['LAST_MAP_PLAYED'] = retrieve_last_map()
    D['RANDOM_MAP'] = random.choice(maps)
    D['CURRENT_MAP'] = maps[int(D['MAP_LIST_INDEX'])]
    print(D)
    # intro = input("B-random\nM-last Map\nN-Next up in pogression\n\tconinue? ")
    end_prompt()
    with open(AUTOEXEC, 'w') as f:
        f.write(multiple_replace(aex, D))
