import requests

# CALL FLIGHT API
querystring = {"origin":"DEN","destination":"HNL","date":"2023-02-17","currency":"USD","countryCode":"US","market":"en-US"}
headers = {
	"X-RapidAPI-Key": open('.key','r').readlines()[4].strip(),
	"X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
}
response = requests.get(url="https://skyscanner50.p.rapidapi.com/api/v1/searchFlights", headers=headers, params=querystring)
flights = response.json()['data']
for flight in flights:
    print('got flight:',flight['price']['amount'])