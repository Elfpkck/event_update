# -*- coding: utf-8 -*-
import requests
import json

url = "http://127.0.0.1:8000/api/events-id-update/"
data = {"gameId": 1,
"gameName": "gridgoal",
"signal": "queue",
"markets": {},
"data": [
    {"eventId": 'ss'},
    {"eventId": 26551, "startTime": "2016-09-02T06:17:00+0800"},
    {"eventId": 26552, "startTime": "2016-09-02T12:20:00+0300"},
    {"eventId": -5, "startTime": "2016-09-02T12:20:00+0300"},
    {"eventId": 'pp'},
    {"eventId": 8, "startTime": "2016-09-02T12:20:00+00"},
]
}
headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)
print(r.text)