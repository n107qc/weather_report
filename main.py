from kivymd.uix.pickers.datepicker.datepicker import date
from kivy.uix.screenmanager import NoTransition
from kivy.uix.settings import text_type
from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from config import API_KEY
import requests

from config import API_KEY, API_URL, FORECAST_URL
API_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&lang=uk"

class Weather(MDCard):
    def __init__(self, date_time, description,icon,temp,rain,wind ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.date_text.text = date_time
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f'{temp}°C'
        self.ids.rain_text.text = f'Ймовірність опадів: {rain*100}%'
        self.ids.wind_text.text = f'Швидкість вітру: {wind}м/c'
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"

class Mainscreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def get_weather_data(self,url,city):
        api_params = {
            'q':city,
            "appid":API_KEY
        }
        
        
        data = requests.get(url, api_params)
        if data.status_code == 200:
            response = data.json()
            return response
        else:
            return None
        
    
    def add_weather_card(self,response):
        description = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temp = response['main']['temp']
        if 'rain' in response:
            if  '1h' in response['rain']:
                rain = response['rain']['1h']
            else:
                rain = response['rain']['3h']
        else:
            rain = 0
        wind = response['wind']['speed']
        if 'dt_txt' in response:
            date_time =  response['dt_txt']
        else:
            date_time = 'Зараз'
        new_card = Weather(date_time,description,icon,temp,rain,wind)
        self.ids.weather_carousel.add_widget(new_card)

    def weather_search(self):
        self.ids.weather_carousel.clear_widgets()
        city = self.ids.city_field.text.strip().lower()
        
        current_weather = self.get_weather_data(API_URL,city)
        forecast = self.get_weather_data(FORECAST_URL,city)
        
        if current_weather:
            self.add_weather_card(current_weather)

        if forecast:
            for period in forecast['list']:
                self.add_weather_card(period)





class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.screen = Mainscreen("main_screen")
        return self.screen

#gg
MainApp().run()