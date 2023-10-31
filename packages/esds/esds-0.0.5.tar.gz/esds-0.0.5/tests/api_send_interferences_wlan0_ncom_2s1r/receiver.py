#!/usr/bin/env python

def execute(api):
    code,data=api.receive("wlan0")
    api.log("Receiver receive code 1 is " + str(code))
    code,data=api.receive("wlan0")
    api.log("Receiver receive code 2 is " + str(code))
    

