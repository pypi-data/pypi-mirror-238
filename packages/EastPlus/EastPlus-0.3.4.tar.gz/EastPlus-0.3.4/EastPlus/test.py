import tool
import datetime,time
import json,sseclient,requests,pprint

def get_data_stream(data_queue,uid="8_151111_mx",):
    url = "https://28.futsseapi.eastmoney.com/sse/"+uid+"/"
    print("get_data_stream",url)
    payload = {}
    headers = {
      'Accept': 'text/event-stream',
      'Accept-Language': 'en-GB,en-US;q=0.9,en;q=0.8',
      'Cache-Control': 'no-cache',
      'Connection': 'keep-alive',
      'Origin': 'https://quote.eastmoney.com',
      'Referer': 'https://quote.eastmoney.com/gzqh/151111.html',
      'Sec-Fetch-Dest': 'empty',
      'Sec-Fetch-Mode': 'cors',
      'Sec-Fetch-Site': 'same-site',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
      'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
      'sec-ch-ua-mobile': '?0',
      'sec-ch-ua-platform': '"Windows"'
    }
    response = requests.request("GET", url, headers=headers, data=payload)
    client = sseclient.SSEClient(response)
    start = 0
    for event in client.events():
        print(time.time() - start)
        ct = json.loads(event.data)
        pprint.pprint(ct)
        start = time.time()
        data_queue.put(ct)

def date_user(q):
    print("date_user")
    while True:
        item = q.get()
        print("user",item)


import threading
import queue

q = queue.Queue()

get_data_stream(q)