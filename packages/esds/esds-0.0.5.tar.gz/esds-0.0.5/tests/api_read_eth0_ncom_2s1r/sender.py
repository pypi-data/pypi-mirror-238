#!/usr/bin/env python

def execute(api):
    api.wait(1248) # All communications start at t=1248s
    if api.node_id==0:
        api.send("eth0","hello",50,2)
    else:
        api.wait(1) # Second sender start 1s after the first
        api.send("eth0","hello",50,2)
