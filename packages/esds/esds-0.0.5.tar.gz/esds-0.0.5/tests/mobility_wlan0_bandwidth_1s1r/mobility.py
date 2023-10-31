#!/usr/bin/env python

def callback(simulator):
    simulator.log("Network update!")
    L=simulator.netmat["wlan0"]["latency"]
    new_bw_wlan0=simulator.netmat["wlan0"]["bandwidth"]*2
    simulator.update_network({"wlan0":{"bandwidth":new_bw_wlan0, "latency":L, "is_wired":False}})
