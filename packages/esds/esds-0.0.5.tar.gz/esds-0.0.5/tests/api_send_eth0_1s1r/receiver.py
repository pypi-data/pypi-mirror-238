#!/usr/bin/env python
from esds import RCode

def execute(api):
    ##### Simple receive
    code, data=api.receive("eth0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    ##### Test if we still receive the data when we are not receiving
    api.wait(2)
    code, data=api.receive("eth0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    ##### Ensure data is not receive when turned off but communication must still be ongoing
    api.turn_off()
    api.wait(1)
    api.turn_on()
    code, data=api.receivet("eth0",1)
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    ##### Ensure communication get aborted on turned off for the sender
    api.wait(28) # Goto t=33s
    api.wait(2)  # Goto t=35s
    api.turn_off()


    
