#!/usr/bin/env python

def callback(simulator):
    simulator.log("Network update!")
    B=simulator.netmat["wlan0"]["bandwidth"]
    new_lat_wlan0=simulator.netmat["wlan0"]["latency"]+1/2
    simulator.update_network({"wlan0":{"bandwidth":B, "latency":new_lat_wlan0, "is_wired":False}})
