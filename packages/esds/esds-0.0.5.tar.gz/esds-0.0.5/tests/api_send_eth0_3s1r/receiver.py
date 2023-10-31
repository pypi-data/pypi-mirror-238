#!/usr/bin/env python
from esds import RCode

def receive(node, n):
    for i in range(0,n):
        code, data=node.receive("eth0")
        msg="Received: "+data if code == RCode.SUCCESS else "Receive failed code="+str(code)
        node.log(msg)

def execute(api):
    # Receive the first 3 send that should end at 3s
    receive(api,3)
    # Receive the first 3 send that should end at 7s
    receive(api,3)
    # Receive the first 3 send that should end at 12s
    receive(api,3)
    # Receive the first 3 send that should end at 18s
    receive(api,3)
    # Should ends at 23s
    receive(api,1)
