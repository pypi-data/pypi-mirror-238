#!/usr/bin/env python
from esds import RCode

def receivet(node,timeout):
    ##### Simple receive
    code, data=node.receivet("eth0",timeout)
    msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
    node.log(msg)

def execute(api):
    # Should works
    receivet(api,2)
    # Should failed
    receivet(api,0.5) # At t=1.5s
    # Should works (priorities says that communications should occurs before timeout)
    receivet(api,0.5) # At t=2s (timeout+receive should occur)
