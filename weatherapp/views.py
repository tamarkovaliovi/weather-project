import os
import requests
from django.shortcuts import render
from django.contrib import messages

def index(request):
    api_key = os.environ.get('OPENWEATHER_API_KEY')
    if not api_key:
        raise RuntimeError('OPENWEATHER_API_KEY not set in environment')

    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    weather_data = None

    if request.method == 'POST':
        city = request.POST.get('city', '').strip()
        
        if not city:
            messages.error(request, 'Lütfen geçerli bir şehir adı girin.')
            
        elif len(city) > 50:
            messages.error(request, 'Şehir adı çok uzun, lütfen kontrol edin.')
            
        else:
            params = {'q': city, 'units': 'metric', 'appid': api_key}
            
            try:
                response = requests.get(base_url, params=params, timeout=5)
                
                if response.status_code == 200:
                    data = response.json()
                    weather_data = {
                        'city': data.get('name', city),
                        'temperature': data['main']['temp'],
                        'description': data['weather'][0]['description'],
                        'icon': data['weather'][0]['icon'],
                    }
                elif response.status_code == 404:
                    messages.error(request, f'"{city}" adında bir şehir bulunamadı.')
                else:
                    messages.error(request, 'Hava durumu servisinde bir sorun oluştu. Lütfen sonra tekrar deneyin.')
                    print(f"OpenWeather API Error: Status {response.status_code}")
                    
            except requests.exceptions.RequestException as e:
                messages.error(request, 'Hava durumu sunucusuna bağlanılamadı.')
                print(f"Bağlantı hatası: {e}")

    return render(request, 'weatherapp/index.html', {'weather': weather_data})