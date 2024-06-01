from kivy.uix.settings import text_type
from kivymd.uix.backdrop.backdrop import MDCard
from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from config import API_KEY
import requests

from config import API_KEY, API_URL
API_URL = "https://api.openweathermap.org/data/2.5/weather?units=metric&lang=uk"

class Weather(MDCard):
    def __init__(self, description,icon,temp,rain,wind ,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ids.desc_text.text = description
        self.ids.temp_text.text = f'{temp}°C'
        self.ids.rain_text.text = f'Ймовірність опадів: {rain*100}%'
        self.ids.wind_text.text = f'Швидкість вітру: {wind}м/c'
        self.ids.weather_icon.source = f"https://openweathermap.org/img/wn/{icon}@2x.png"

class Mainscreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def weather_search(self):
        city = self.ids.city_field.text.strip().lower()
        api_params = {
            'q':city,
            "appid":API_KEY
        }
        
        
        data = requests.get(API_URL, api_params)
        response = data.json()
        print(response)
        description = response['weather'][0]['description']
        icon = response['weather'][0]['icon']
        temp = response['main']['temp']
        if 'rain' in response:
            rain = response['rain']['1h']
        else:
            rain = 0
        wind = response['wind']['speed']
        new_card = Weather(description,icon,temp,rain,wind)
        self.ids.weather_carousel.add_widget(new_card)





class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.screen = Mainscreen("main_screen")
        return self.screen

#gg
MainApp().run()