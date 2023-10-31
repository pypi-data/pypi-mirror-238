#!/usr/bin/env python

def execute(api):
    wait=api.node_id
    api.log("Before wait for "+str(wait)+"s")
    api.wait(wait) # Since 3 nodes max(wait)==2
    api.log("First wait end")
    
    # Ensure that wait end return back when simulation ends
    api.wait_end()
    api.log("Terminated")
