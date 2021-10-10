import requests
import json
from datetime import datetime

import sensor

id = 1
time = datetime.now(tz=None).strftime("%Y-%m-%d %H:%M")
lat = 53
long = 13
val = sensor.get_current_decibels()
var = {"identity": id, "timestamp": time, "location": {"latitude": lat, "longitude": long},
        "value": val}
headers = {'Content-type': 'application/json'}
r = requests.post("http://127.0.0.1:5000/sensordata", json.dumps(var), headers=headers)

#print(var)
#print(r.text)