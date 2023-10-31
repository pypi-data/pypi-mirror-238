#!/usr/bin/env python

import sys, random, time
from esds import RCode

lr=random.Random(6)

def execute(api):
    uptime=api.args
    endoff=0
    for i in range(0,24):
        startoff=random.randint(0,3600-uptime)
        api.turn_off()
        api.wait(startoff+endoff)
        api.turn_on()
        wakeat=api.read("clock")
        wakeuntil=wakeat+uptime
        # Receive until uptime seconds if elapsed
        while api.read("clock") < wakeuntil:
            code, data=api.receivet("wlan0",wakeuntil-api.read("clock"))
            if code == RCode.SUCCESS:
                api.log("Receive "+data)
        api.log("Was up for {}s".format(api.read("clock")-wakeat))
        endoff=3600*(i+1)-api.read("clock")
    api.turn_off()
    api.wait(endoff)
    api.turn_on()


