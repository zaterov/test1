#! /usr/bin/env python3

from pyStatus.Bar import Bar
from pyStatus.plugins import Time, Battery, CPU, Memory, Ip, Traffic, Filesystem, ESSID, MemPercent, MPD, Load


my_bar = Bar(delay=1)
my_bar.register(Time.Time("%H:%M"))

my_bar.loop()
