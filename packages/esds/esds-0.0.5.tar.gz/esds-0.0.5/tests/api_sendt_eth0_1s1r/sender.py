#!/usr/bin/env python
from esds import RCode

def sendt(node,timeout):
    code=node.sendt("eth0","Hello World!",1,1,timeout)
    msg="Send worked!" if code == RCode.SUCCESS else "Send failed"
    node.log(msg)

def execute(api):
    # Should work
    sendt(api,2)
    # Should not work
    sendt(api,0.5)
    # Should work
    sendt(api,1)
