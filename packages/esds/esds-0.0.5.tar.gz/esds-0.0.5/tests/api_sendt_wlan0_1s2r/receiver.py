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

