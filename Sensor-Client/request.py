import requests

pload = {'location':'Seestraße 111', 'Lautstaerke':'9', 'Zeitpunkt':'09.10.2021 13:50'}
r = requests.post("http://127.0.0.1:5000/", pload)
print(r.text)