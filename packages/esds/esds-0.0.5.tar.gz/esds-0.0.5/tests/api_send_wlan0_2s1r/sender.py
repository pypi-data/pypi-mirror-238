#!/usr/bin/env python

def execute(api):
    code=api.send("wlan0","Hello World!",1,1)
    api.log("Sender send code "+str(code))
    code, data=api.receive("wlan0")
    api.log("Sender receive code "+str(code))