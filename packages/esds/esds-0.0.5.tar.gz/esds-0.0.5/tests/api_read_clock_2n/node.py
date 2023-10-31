#!/usr/bin/env python

def execute(api):
    api.log("Clock is {}s".format(api.read("clock"))) # Ensure clock is 0s for both node
    api.wait(5698.1256)
    api.log("Clock is {}s".format(api.read("clock"))) # Ensure clock is 5698.1256s for both node
    api.log("Clock is {}s".format(api.read("clock"))) # Ensure clock did not change in between for both node
