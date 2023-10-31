#!/usr/bin/env python
from esds import RCode

def receive(node):
    ##### Simple receive
    code, data=node.receive("wlan0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    node.log(msg)


def execute(api):
    # Should works for all receivers
    receive(api)

    if api.node_id == 1:
        receive(api) # Should works
    else:
        api.turn_off()
        api.wait(1) # Node 2 should not receive anything during 1s
        api.turn_on() 


    if api.node_id == 1:
        receive(api) # Should works
    else:
        api.wait(0.5) # Check if started communication get cancelled on turning off
        api.turn_off() # Node 2 should not receive anything
        api.wait(0.5) # Node 2 should not receive anything during 0.5s
        api.turn_on() 

