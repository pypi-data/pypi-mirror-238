#!/usr/bin/env python

def callback(simulator):
    simulator.log("Network update!")
    new_lat_eth0=simulator.netmat["eth0"]["latency"]+1/2
    simulator.update_network({"eth0":{"bandwidth":simulator.netmat["eth0"]["bandwidth"], "latency":new_lat_eth0, "is_wired":True}})
