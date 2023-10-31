#!/usr/bin/env python

def execute(api):
    api.send("eth0","Hello World!",0,1)
    api.wait(0)
    api.send("eth0","Hello World!",0,1)
    api.wait(1)
    api.send("eth0","Hello World!",0,1)
    api.wait(1)
    api.wait(1)
    api.send("eth0","Hello World!",0,1)
    api.send("eth0","Hello World!",0,1)
