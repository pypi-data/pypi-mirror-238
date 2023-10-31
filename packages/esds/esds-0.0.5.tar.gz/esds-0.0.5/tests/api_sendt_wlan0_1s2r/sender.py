#!/usr/bin/env python

def execute(api):
    # Should works
    api.sendt("wlan0","Hello World!",1,1,2)
    # Should not work
    api.sendt("wlan0","Hello World!",1,1,0.5)
    
