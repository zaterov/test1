#!/usr/bin/python
# -*- coding: latin-1 -*-
'''
This is my module. Because it is mine.
'''

import sys
import time
import os.path
import linecache
from random import randrange


def get_uptime():
	from datetime import timedelta
	import platform

	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])

		days,  remainderD = divmod(uptime_seconds, 3600 * 24)
		hours, remainderH = divmod(remainderD, 3600)
		minutes, seconds = divmod(remainderH, 60)
		upstring =  '%dd %d:%0.2d:%0.2s' % (days, hours, minutes, seconds)

		hoststring = platform.uname()[1]

		return (upstring, hoststring)

def get_sys_info():
            from subprocess import check_output
            outstr = ""
            top_out = check_output(["top", "-n", "1", "-b"])
            top_lines = top_out.split("\n")
            outstr +=  "\n".join(top_lines[:14])
            outstr += "\n\ncollectl:\n" 
            #lines = top_out.split('\n')
            #outstr = "".join(lines)

            lines = []
            collectl_out = check_output(["collectl", "-c", "3", "--quiet"])
            lines.append("".join(collectl_out))

            #print ' '.join(map(str, )
            for i in range(len(lines)):
                    outstr += str(lines[i]) 

            return outstr 

def filesize_fmt(num):
    """Human friendly file size -  thanks to joctee at SO"""
    from math import log

    unit_list = zip([ 'bytes', 'kB', 'MB', 'GB', 'TB', 'PB', ], [ 0, 0, 1, 2, 2, 2, ])
    if num > 1:
        exponent = min(int(log(num, 1024)), len(unit_list) - 1)
        quotient = float(num) / 1024 ** exponent
        (unit, num_decimals) = unit_list[exponent]
        format_string = '{:.%sf} {}' % num_decimals
        return format_string.format(quotient, unit)
    if num == 0:
        return '0 bytes'
    if num == 1:
        return '1 byte'


strFrom ='victor.oravetz@yahoo.com'
strTo = 'victor.oravetz@yahoo.com'
msgRoot = {'Subject': "System YOO update from WernerIV"}
creds = { 'HOST':'smtp.mail.yahoo.com',
          'PORT': 587,
          'LOGIN':'victor.oravetz@yahoo.com',
          'PASS':'jorma444',
        }

def fyshuffle(items):
        '''canonical Pythonic implementation of 
        the Fisher-Yates algorithm  - originally called
        'sattoloCycle' 
        '''
        i = len(items)
        while i>1:
                i = i - 1
                j = randrange(i) # 0 <= j <= i-1
                items[j], items[i] = items[i], items[j]
        return items

def play_music(music_file, volume=0.8):
    import pygame as pg
    '''
    stream music with mixer.music module in a blocking manner
    this will stream the sound from disk while playing
    '''
    # set up the mixer
    freq = 44100     # audio CD quality
    bitsize = -16    # unsigned 16 bit
    channels = 2     # 1 is mono, 2 is stereo
    buffer = 4096    # number of samples (experiment to get best sound)
    pg.mixer.init(freq, bitsize, channels, buffer)
    # volume value 0.0 to 1.0
    pg.mixer.music.set_volume(volume)
    clock = pg.time.Clock()

    try:
        pg.mixer.music.load(music_file.encode('utf-8'))
        print("Music file {} loaded!".format(music_file.encode('utf-8')))
    except pg.error:
        print("File {} not found! ({})".format(music_file.encode('utf-8'), pg.get_error()))
        return

    pg.mixer.music.play()

    while pg.mixer.music.get_busy():
        # check if playback has finished
        clock.tick(30)

import subprocess, os
from subprocess import Popen, PIPE
import errno

def pipe_to_open(text, l):
    p = Popen('less', stdin=PIPE)
    for index, item in enumerate(l):
        line = text % (index, str(item))
        try:
            p.stdin.write(line)
        except IOError as e:
            if e.errno == errno.EPIPE or e.errno == errno.EINVAL:
                # Stop loop on "Invalid pipe" or "Invalid argument".
                # No sense in continuing with broken pipe.
                break
            else:
                # Raise any other error.
                raise

    p.stdin.close()
    p.wait()


if __name__ == '__main__':
	#print get_uptime()
        #print get_sys_info()
        print get_pic()
