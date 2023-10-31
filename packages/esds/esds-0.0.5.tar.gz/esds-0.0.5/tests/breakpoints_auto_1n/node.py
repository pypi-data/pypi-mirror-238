#!/usr/bin/env python

def execute(api):
    if api.node_id == 0:
        api.send("eth0","Hello",5,1)
    else:
        api.receive("eth0")
        
