#!/usr/bin/env python

# Load ESDS
import esds

# Use numpy to construct bandwidth and latencies matrix
import numpy as np

##### Scenario
# The simulated scenario comprises 1 that wakes up randomly
# for a duration called "uptime" every hour. The sender try to transmit
# his data during that uptime. Other nodes are receivers that have similar
# random wake up parterns and strive to receive data from the sender.

##### Bandwidth matrix
# Bandwidth value can be 0 for unreachable nodes
# Regarding wireless interfaces the diagonals of the bandwidth and latency matrices are very important.
# They determine the duration of the tranmission for THE SENDER. It allows to have a different tx
# duration per node and per interface. Please cf esds.py for more informations.
n=2 # Number of nodes including the sender
B=np.full((n,n),5) # 5Mbps

##### Latency matrix
# If the latency entries match one with a bandwidth of 0
# then it will be ignore since node is unreachable.
L=np.full((n,n),0) # 0s

##### Create the simulator
# esds.Simulator take at least a dictionnary as a parameter
# This dictionnary contains all the network interfaces (name as a key) of each node
s=esds.Simulator({"wlan0":{"bandwidth":B, "latency":L, "is_wired":False},"eth0":{"bandwidth":B, "latency":L, "is_wired":True}})

##### Instantiate nodes
uptime=180 # 180s uptime
s.create_node("sender",interfaces=["wlan0","eth0"],args=uptime) # Load sender.py for the first node with 5 as argument (first row in B and L)

# Aguments can be passed to nodes via: s.create_node("sender",args="my argument")
for n in range(0,n-1): # Load receiver.py for the remaining nodes
    s.create_node("receiver",interfaces=["wlan0","eth0"],args=uptime)

##### Run the simulation
#s.run(debug=True) # Generate a "esds.debug" file
s.run()
