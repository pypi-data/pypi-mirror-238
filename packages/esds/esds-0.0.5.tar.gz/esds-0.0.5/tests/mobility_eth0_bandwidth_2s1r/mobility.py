#!/usr/bin/env python

def callback(simulator):
    simulator.log("Network update!")
    new_bw_eth0=simulator.netmat["eth0"]["bandwidth"]*2
    simulator.update_network({"eth0":{"bandwidth":new_bw_eth0, "latency":simulator.netmat["eth0"]["latency"], "is_wired":True}})

