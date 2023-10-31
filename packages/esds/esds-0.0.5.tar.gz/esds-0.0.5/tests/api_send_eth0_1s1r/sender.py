#!/usr/bin/env python

def execute(api):
    api.send("eth0","Hello World!",1,1)
    api.send("eth0","Hello World!",1,1)
    api.wait(1) # Goto t=3s
    api.send("eth0","Hello World!",15,1) # Communication should not be aborted even if receiver turned_off (e.g UDP)
    api.log("End transmission") # Should be printed at t=18s 
    api.send("eth0","Hello World!",15,1) # Now receiver is off (but send should continue)
    api.log("End transmission") # Should be printed at t=33s
    api.send("eth0","Hello World!",15,1,receiver_required=True) # Now receiver is off and send should be interrupted
    api.log("End transmission") # Should be printed at t=35s (receiver turned off at t=35s) 
