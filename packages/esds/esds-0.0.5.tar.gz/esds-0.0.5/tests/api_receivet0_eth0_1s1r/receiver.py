#!/usr/bin/env python
from esds import RCode

def receivet(node,timeout):
    ##### Simple receive
    code, data=node.receivet("eth0",timeout)
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    node.log(msg)

def execute(api):
    # Should not works since communication start at t=0s
    receivet(api,0)
    api.wait(1)
    # Now communication started
    receivet(api,0) # Should work (no timeout error)
