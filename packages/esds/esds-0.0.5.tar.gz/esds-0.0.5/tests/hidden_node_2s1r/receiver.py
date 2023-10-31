#!/usr/bin/env python

def execute(api):
    code,data=api.receive("wlan0")
    api.log("Receiver "+str(code))
    code,data=api.receive("wlan0")
    api.log("Receiver "+str(code))
    
