#!/usr/bin/env python

def execute(api):
    api.send("eth0","Hello World from {}!".format(api.node_id),1,2)

