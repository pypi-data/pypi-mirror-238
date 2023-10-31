#!/usr/bin/env python

def execute(api):
    api.log("wlan0 is {}".format(api.read("ncom_wlan0"))) # Ensure no commmunications at t=0s
