from flask import Flask, render_template, request, url_for # render_template html templatelerimizi response olarak dönmemizi sağlıyor 
import requests
import json

app = Flask(__name__) # flask sınıfından nesne oluşturuyoruz


def weather(city):
    apiKey = '2a73a23a41e79f0e197ab13269cf3c80'
    response = requests.get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={apiKey}')
    weatherData = json.loads(response.content) # response olarak gelen datanın contentini json formatına dönüştürüyoruz

    skyDescription = weatherData['weather'][0]['description']
    cityName = weatherData['name']
    skyTypes = ['clear sky', 'few clouds','overcast clouds', 'scattered clouds','light rain', 'broken clouds', 'shower rain', 'rain', 'thunderstorm','snow','mist']
    skyTypesTR = ['Güneşli', 'Az Bulutlu','Çok Bulutlu', 'Alçak Bulutlu', 'hafif yağmur', 'Yer Yer Açık Bulutlu', 'Sağanak Yağmurlu', 'Yağmurlu', 'Gök Gürültülü Fırtına', 'Karlı', 'Puslu']

    for i in range(len(skyTypes)):
        if skyDescription == skyTypes[i]:
            skyDescription = skyTypesTR[i]

    temp = round((weatherData['main']['temp'] - 273.15), 2)
    feels_temp = round((weatherData['main']['feels_like'] - 273.15), 2)
    temp_min = round((weatherData['main']['temp_min'] - 273.15), 2)
    temp_max = round((weatherData['main']['temp_max'] - 273.15), 2)
    humidity = weatherData['main']['humidity'] 

    weatherDictionary = {
        "Şehir": cityName,
        "Gökyüzü": skyDescription,
        "Sıcaklık": temp,
        "Hissedilen Hava Sıcaklığı": feels_temp,
        "Minimum Sıcaklık": temp_min,
        "Maksimum Sıcaklık": temp_max,
        "Nem Oranı": humidity
    }

    return weatherDictionary

@app.route("/", methods=['POST','GET']) # fonksiyonu decoratora bağlıyoruz ve decorator yapısı ile /'a (kök dizine) erişirse fonksiyon çalıştırmasını istiyoruz.
def index(): # / şeklinde bir request gelirse index fonksiyonu çalışacak

    if request.method == 'POST':
        cityİnfo = request.form['data']
        if not cityİnfo:
            return render_template('index.html')

        a = weather(cityİnfo)
        return render_template('result.html', result = a)
    else:
        return render_template('index.html')

if __name__ == "__main__": #__name__ değişkeni ile dosyamız ana program olarak mı çalıştırılmış yoksa modül olarak başka bir sayfaya mı dahil edilerek çalıştırılmış kontrol ediyoruz, eğer flaskdenemesi.py dosyamız direkt olarak terminalden başlatılmışsa bu değişkenimiz __main__ değerini dönderiyor ve bizimde if ile yaptığımız kontrol başarılı bir şekilde devreye giriyor

    app.run(port=8000,debug=True) # localhost daki web sunucumuzu çalıştırıyoruz