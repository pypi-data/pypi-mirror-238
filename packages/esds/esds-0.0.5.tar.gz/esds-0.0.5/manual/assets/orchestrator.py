#!/usr/bin/env python

import esds
import numpy as np

n=2 # 2 nodes
B=np.full((n,n),50*1000) # Bandwith+txperfs 5bps
L=np.full((n,n),0) # Latency 0s

s=esds.Simulator({"wlan0":{"bandwidth":B, "latency":L, "is_wired":False}})

##### Instantiate nodes with their implementation
s.create_node("node",interfaces=["wlan0"],args="sender") # Use node.py for the first node, specify the vailable communication interfaces and use "sender" as argument
s.create_node("node",interfaces=["wlan0"],args="receiver") # Now the second node

##### Run the simulation
s.run(interferences=True)
