import requests
from django.shortcuts import render

def index(request):
    api_key = "a5ec00ef1b1be1dd0c3ac100ffc0d896"
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + api_key
    
    weather_data = None

   
   
    if request.method == 'POST':
        city = request.POST.get('city')
        response = requests.get(url.format(city)).json()
        
        
        print(response) 

        if response.get('main'):
            weather_data = {
                'city': city,
                'temperature': response['main']['temp'],
                'description': response['weather'][0]['description'],
                'icon': response['weather'][0]['icon'],
            }
        else:

            print(f"Hata Mesajı: {response.get('message')}")

    return render(request, 'weatherapp/index.html', {'weather': weather_data})