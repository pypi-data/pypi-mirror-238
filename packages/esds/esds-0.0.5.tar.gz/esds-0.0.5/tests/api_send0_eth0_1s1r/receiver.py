#!/usr/bin/env python
from esds import RCode

def receive(api):
    ##### Simple receive
    code, data=api.receive("eth0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)

def execute(api):
    receive(api)
    # Simulated time t=0s here
    receive(api)
    # Simulated time t=0s here
    receive(api)
    # Simulated time t=1s here
    receive(api)
    # Simulated time t=3s here
    code, data=api.receivet("eth0",0)
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    # Simulated time t=3s here

    
