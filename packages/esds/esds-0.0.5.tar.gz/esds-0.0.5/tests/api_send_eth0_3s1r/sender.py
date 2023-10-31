#!/usr/bin/env python

# Node that bandwidths at setup in a way that 1 byte is send in 1 seconds with no sharing

def execute(api):
    # Should be completed at 3s (bandwidth divided by 3)
    api.send("eth0","Hello World from {}!".format(api.node_id),1,3) # Shoud lasts 3s

    # These send should start at 3s and be completed at 7s
    if api.node_id==0:
        api.send("eth0","Hello World (2bytes) from {}!".format(api.node_id),2,3) # Should lasts 3s + 1s = 4s
    else:
        api.send("eth0","Hello World from {}!".format(api.node_id),1,3) # Should lasts 3s
        api.wait(1) # Sync with node 0 at 7s

    # Those sends should start at 7s and be completed at 12s
    if api.node_id<=1:
        api.send("eth0","Hello World (2bytes) from {}!".format(api.node_id),2,3) # Should last 3s + 2s = 5s
        # Completed at 12s since 3 nodes are sharing the bandwidth up to 10s
        # then the 2 two remaining node send their last byte up to 12s
    else:
        api.send("eth0","Hello World from {}!".format(api.node_id),1,3) # Should last 3s
        # Completed at 10s (3 nodes are sharing the bandwidth)
        api.wait(2)  # Sync with node 0-1 at 12s

    # Should start at 12s
    # Node 0 sends 1 byte, node 1 sends 2 byte and node 2 sends 3
    # These send should end at 18s
    api.send("eth0","Hello World from {}!".format(api.node_id),api.node_id+1,3) # Should lasts 3s, 5s and 6s

    # Finally a single send from node 0
    if api.node_id==0:
        api.wait(3) # Since node 0 send ends at 15s we sync it to 18s
        api.send("eth0","Hello World from {}!".format(api.node_id),5,3) # Should takes 5 seconds (ends at 23s)

        

