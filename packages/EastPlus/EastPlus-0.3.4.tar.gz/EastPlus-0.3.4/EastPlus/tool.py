import requests
import json
import pprint
import sseclient
import time
import datetime
def pdata(url,headers,payload,file_name="",mor=0):
    response = requests.request("GET", url, headers=headers, data=payload, stream=True)
    client = sseclient.SSEClient(response)
    start = 0
    for event in client.events():
        print(time.time() - start)
        ct  = json.loads(event.data)
        pprint.pprint(ct)
        start = time.time()
        if ct == {'h':'n'} and mor == 0:
            pass
        elif ct == {'h':'n'}:
            if datetime.datetime.now().hour>7:
                if file_name:
                    fc = open(file_name, "a+")
                    fc.write(str(ct) + "\n")
                    fc.close()
                return "end"
        else:
            mor = 1

        if file_name:
            fc = open(file_name,"a+")
            fc.write(str(ct)+"\n")
            fc.close()

def get_date():
    return datetime.datetime.now().strftime("%Y%m%d")

def hour_check(t_hour):
    if datetime.datetime.now().hour > t_hour:
        return False
    return True
