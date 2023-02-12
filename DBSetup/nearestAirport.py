import requests
from pymongo import MongoClient

with open('.key','r') as f:
    lines = f.readlines()
    mongoURL = lines[1].strip()
    mongoUSER = lines[2].strip()
    mongoPASS = lines[3].strip()
client = MongoClient(mongoURL, username=mongoUSER, password=mongoPASS)
db = client['hawaii']

URL = 'https://www.travelmath.com/nearest-airport/'

for city in db.cities.find():
    r = requests.get(URL + city['name'])
    s = r.text.find('/airport/')
    airport = r.text[s + 9:s+12]
    if airport == 'E h':
        print('invalid airport, setting to honolulu international')
        airport = 'HNL'
    print(city['name'], airport)

    print('replacing...')
    db.cities.delete_one()
    

