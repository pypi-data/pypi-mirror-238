#!/usr/bin/env python

def execute(api):
    api.log("wlan0 is {}".format(api.read("ncom_wlan0"))) # Ensure no commmunications at t=0s
    api.wait(624)
    api.log("wlan0 is {}".format(api.read("ncom_wlan0"))) #  Ensure still no commmunications at t=624s
    api.wait(624)
    # Now we are at 624*2=1248 (first sender start a communication)
    api.wait(1) # Let the communication starts (otherwise value will be 0 (see api_read_order_ncom_1s2r))
    api.log("wlan0 is {}".format(api.read("ncom_wlan0"))) # Should print 1
    # Now second sender start a communication
    api.wait(1) # Let the second communication starts
    api.log("wlan0 is {}".format(api.read("ncom_wlan0"))) # Should print 2
