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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Mainscreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    def weather_search(self):
        city = self.ids.city_field.text.strip().lower()
        api_params = {
            'q':city,
            "appid":API_KEY
        }
        inf = requests.get(API_URL,api_params)
        response = inf.json()
        print(response)
        deck_weather = response['weather'][0]['deck_weather']
        self.ids.weather_card.ids.label.text = deck_weather

class MainApp(MDApp):
    def build(self):
        Builder.load_file('style.kv')
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Yellow"
        self.screen = Mainscreen("main_screen")
        return self.screen

#gg
MainApp().run()