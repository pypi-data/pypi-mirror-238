#!/usr/bin/env python

######################
#     _    ____ ___  #
#    / \  |  _ \_ _| #
#   / _ \ | |_) | |  #
#  / ___ \|  __/| |  #
# /_/   \_\_|  |___| #
#                    #
######################
# api.args                                       # Contains node arguments
# api.send(interface, data,size, dst)            # If interface is "wlan0" dst is not used
# api.sendt(interface, data,size, dst,timeout)   # Similar to api.send() but with timeout
# api.receive(interface)                         # Receive the data by returning the following tuple (code,data) if code is 0 receive succeed
# api.receivet(interface,timeout)                # Similar to api.receive() but with timeout
# api.read(register)                             # Read from the simulator registers (ex: clock)
# api.log(msg)                                   # Print log in the simulation console
# api.wait(duration)                             # Wait for "duration" seconds of simulated time
# api.turn_off(duration)                         # Turn the node off for "duration" seconds (no data can be receive during this time period)

import random

# Note that the following is required to have different instance from thread to thread
lr=random.Random(6)

def execute(api):
    uptime=api.args
    endoff=0
    for i in range(0,24):
        startoff=random.randint(0,3600-uptime)
        api.turn_off()
        api.wait(startoff+endoff)
        api.turn_on()
        wakeat=api.read("clock")
        wakeuntil=wakeat+uptime
        # Send until uptime seconds if elapsed
        while api.read("clock") < wakeuntil:
            api.sendt("wlan0","hello",10,None, wakeuntil-api.read("clock"))
        api.log("Was up for {}s".format(api.read("clock")-wakeat))
        endoff=3600*(i+1)-api.read("clock")
    api.turn_off()
    api.wait(endoff)
    api.turn_on()
        



