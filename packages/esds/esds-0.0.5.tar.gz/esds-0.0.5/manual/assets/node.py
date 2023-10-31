def execute(api):
    role=api.args # "sender" or "receiver" cf. platform.yaml
    if role == "sender":
        api.send("wlan0","MY MESSAGE",10,None)
    else:
        api.receive("wlan0")
