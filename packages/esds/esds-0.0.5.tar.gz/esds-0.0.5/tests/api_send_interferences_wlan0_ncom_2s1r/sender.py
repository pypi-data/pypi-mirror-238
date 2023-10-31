#!/usr/bin/env python

def execute(api):
    if api.node_id==0:
        code=api.send("wlan0","hello",50,None)
    else:
        code=api.send("wlan0","hello",50,None)
    api.log("Sender send code is "+str(code))
    code,data=api.receive("wlan0")
    api.log("Sender receive code is "+str(code))
    