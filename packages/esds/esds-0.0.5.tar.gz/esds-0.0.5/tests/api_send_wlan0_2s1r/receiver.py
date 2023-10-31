#!/usr/bin/env python

def execute(api):
    code, data=api.receive("wlan0")
    api.log("Receiver code 1 "+str(code))
    code, data=api.receive("wlan0")
    api.log("Receiver code 2 "+str(code))

