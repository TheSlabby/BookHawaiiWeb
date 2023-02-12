import requests
from pymongo import MongoClient

client = MongoClient('mongodb+srv://bookhawaii.eyhrv.mongodb.net/myFirstDatabase', username='Stair', password='4q0khheB27jVnY8m')
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
    

