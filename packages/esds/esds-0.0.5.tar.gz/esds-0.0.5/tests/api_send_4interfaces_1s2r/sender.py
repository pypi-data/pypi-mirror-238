#!/usr/bin/env python

def execute(api):
    # Wireless
    api.send("wlan0","Hello World!",1,1)
    api.send("wlan1","Hello World!",1,1)
    # Wired
    api.send("eth0","Hello World!",1,1)
    api.send("eth0","Hello World!",1,2)
    api.send("eth1","Hello World!",1,1)
    api.send("eth1","Hello World!",1,2)

