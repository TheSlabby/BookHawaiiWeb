from django.shortcuts import render, HttpResponseRedirect
from utils import get_db_handle as GetDB
import requests, datetime

# Create your views here.


def home(request):
    db = GetDB()['hawaii']
    city = db.cities.find({'name':'Honolulu'})[0]
    currentWeather = city['weather']['now']
    print(currentWeather['temp_f'])

    return render(request, 'home.html', {'weather' : currentWeather})

def weatherHome(request):
    cities = GetDB()['hawaii'].cities.find()[:15]
    return render(request, 'weatherHome.html', {'cities': cities})

def estimatesHome(request):
    if request.method == 'POST':
        return HttpResponseRedirect('/estimates/' + request.POST['city'].title())
    else:
        return render(request, 'estimatesHome.html')

def estimates(request, city):
    origin = False
    hotelPrice = 150
    if request.method == 'POST':
        origin = request.POST['origin'].upper()
        date = request.POST['departure']
        returnDate = request.POST['arrival']
        hotelPrice = request.POST['hotelPrice']

    db = GetDB()['hawaii']
    if db.cities.count_documents({'name' : city}) > 0:
        print('found city, getting flight information')
        city = db.cities.find({'name' : city})[0]
        dest = city['airport']

        # CALL FLIGHT API
        flights = False
        if origin:
            print('Getting flights...')
            querystring = {"origin":origin,"destination":dest,"date":date,'returnDate':returnDate,"currency":"USD","countryCode":"US","market":"en-US"}
            headers = {
                "X-RapidAPI-Key": "7dc7750061msh5bc05e27aa96c7cp1f0e35jsnb78e0720cfd2",
                "X-RapidAPI-Host": "skyscanner50.p.rapidapi.com"
            }
            response = requests.get("https://skyscanner50.p.rapidapi.com/api/v1/searchFlights", headers=headers, params=querystring)
            flights = response.json()
            if not 'data' in flights:
                flights = "None"
            else:
                flights = flights['data'][:10]
            
            departureDate = datetime.datetime.strptime(date, "%Y-%m-%d")
            arrivalDate = datetime.datetime.strptime(returnDate, "%Y-%m-%d")
            dif = arrivalDate - departureDate
            hotelPrice = dif.days * int(hotelPrice)


        return render(request, 'estimates.html', {'city' : city, 'flights' : flights, 'hotelPrice' : hotelPrice})
    else:
        print('couldnt find city')
        return render(request, 'estimatesNotFound.html')
    