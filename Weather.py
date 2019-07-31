from pyowm import *
from pyowm.exceptions import api_response_error, api_call_error

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
        try:
            self.location = location
            self.obs = self.owm.weather_at_place(self.location)
            self.weather = self.obs.get_weather()
            self.loc = self.obs.get_location()
        except (api_response_error.NotFoundError, api_call_error.APICallError):
            self.location = "Error"

    def get_temperature(self, degrees: str) -> str:
        return str(round(self.weather.get_temperature(degrees)["temp"]))

    def get_humidity(self) -> str:
        return str(self.weather.get_humidity())

    def get_wind_speed(self, degrees: str) -> str:
        if degrees == "fahrenheit":
            mph = self.weather.get_wind()["speed"] * (3600/1609.344)
            return f"{str(round(mph, 1))} mph"

        return f"{str(self.weather.get_wind()['speed'])} m/s"

    def get_pressure(self) -> str:
        return str(round(self.weather.get_pressure()["press"]))

    def get_location(self) -> str:
        return self.loc.get_name()

    def get_weather_icon(self) -> str:
        status = self.weather.get_status().lower()

        if status == "clear" or status == "clouds" or status == "drizzle" or status == "rain" or status == "snow" or status == "thunderstorm":
            return f"icons/{status}.png"
        else:
            return "icons/mist.png"

