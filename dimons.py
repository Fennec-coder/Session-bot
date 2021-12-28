import threading


def todays_check():
    pass


flow_todays_check = threading.Thread(target=todays_check)
flow_todays_check.daemon = True
flow_todays_check.start()
