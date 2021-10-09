import requests
import json
from datetime import datetime



id = 1
time = datetime.now(tz=None).strftime("%Y-%m-%d %H:%M")
lat = 53
long = 13
val = sensor.getDB()
var = {"identity": id, "timestamp": time, "location": {"latitude": lat, "longitude": long},
        "value": val}

r = requests.post("http://127.0.0.1:5000/", var)

print(var)
#print(r.text)