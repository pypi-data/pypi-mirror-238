#!/usr/bin/env python

def execute(api):
    api.log("Before wait")
    api.wait(2)
    api.log("After wait")
    api.log("Before wait")
    api.wait(3)
    api.log("After wait")
