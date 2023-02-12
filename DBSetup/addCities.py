import csv, requests, urllib.parse, datetime
from pymongo import MongoClient

with open('.key','r') as f:
    lines = f.readlines()
    mongoURL = lines[1]
    mongoUSER = lines[2]
    mongoPASS = lines[3]

client = MongoClient(mongoURL, username=mongoUSER, password=mongoPASS)
db = client['hawaii']
cities = db.cities
cities.drop()

dayDictionary = [
    'Monday','Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'
]

# use weather api
def get_weather(city):

    # build url
    URL = "http://api.weatherapi.com/v1/forecast.json"
    URL += '?key=' + WEATHER_API_KEY + '&Q=' + urllib.parse.quote(city) + '&days=7'

    print('using URL:', URL)
    r = requests.get(URL)
    data = r.json()

    days = []
    i = 0
    if 'forecast' in data:
        for day in data['forecast']['forecastday']:
            i += 1
            date = dayDictionary[datetime.datetime.strptime(day['date'], "%Y-%m-%d").weekday()]
            
            print(i, date)
            days.append({
                'date' : date,
                'info' : day['day']
            })

        return {
            'now' : data['current'],
            'forecast': days
        }
    else:
        print('error with', city)


with open('.key','r') as f:
    WEATHER_API_KEY = f.readlines()[0]


# Open the CSV file
with open("DBSetup/cities.csv", "r") as file:
    # Create a CSV reader object
    reader = csv.reader(file)

    # Loop through the rows in the CSV file
    for row in reader:
        valid = True
        # Print each column in the row
        city = row[0]
        population = int(row[1].replace(',',''))
        print(city, 'with population:', population)

        # WEATHER
        print('Adding weather:')
        w = get_weather(city)
        if w:
            document = {
                'name' : city,
                'population' : population,
                'weather': w,
                'airport': 'HNL' #default airport

            }
        else:
            continue
    
        # GET NEAREST AIRPORT
        r = requests.get('https://www.travelmath.com/nearest-airport/' + city)
        s = r.text.find('/airport/')
        airport = r.text[s + 9:s+12]
        if airport == 'E h':
            print('invalid airport, setting to honolulu international')
            airport = 'HNL'
        document['airport'] = airport

        print('inserting document..\n')
        cities.insert_one(document)
            



        

