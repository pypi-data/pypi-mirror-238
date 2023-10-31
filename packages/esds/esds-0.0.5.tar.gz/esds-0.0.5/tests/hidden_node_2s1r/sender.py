#!/usr/bin/env python

def execute(api):
    code=api.send("wlan0","Hello World!",1,1)
    api.log("Sender "+str(code))
