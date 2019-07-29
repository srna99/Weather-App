from pyowm import *
import Key


class Weather:
    obs = None
    weather = None
    loc = None

    def __init__(self):
        self.owm = OWM(Key.api_key)
        self.location = "London"
        self.get_weather_at_loc(self.location)

    def get_weather_at_loc(self, location: str):
        self.location = location
        self.obs = self.owm.weather_at_place(self.location)
        self.weather = self.obs.get_weather()
        self.loc = self.obs.get_location()

    def get_temperature(self, degrees: str) -> str:
        return str(round(self.weather.get_temperature(degrees)["temp"]))

    def get_location(self) -> str:
        return self.loc.get_name()

    def get_weather_icon(self) -> str:
        status = self.weather.get_status().lower()
        print(status)
        if status == "clear" or status == "clouds" or status == "drizzle" or status == "rain" or status == "snow" or status == "thunderstorm":
            return f"icons/{status}.png"
        else:
            return "icons/mist.png"

