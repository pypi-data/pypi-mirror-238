#!/usr/bin/env python
from esds import RCode

def execute(api):
    ##### Simple receive from node 0
    code, data=api.receive("eth0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    
    ##### Simple receive from node 1
    code, data=api.receive("eth0")
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    api.log(msg)
    
