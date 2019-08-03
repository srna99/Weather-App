from pyowm import OWM
from pyowm.exceptions import api_response_error, api_call_error
from pytz import timezone
from calendar import day_abbr
import Key


class Weather:
    obs = None
    weather = None
    loc = None
    forecaster = None
    location = ""

    def __init__(self):
        self.owm = OWM(Key.api_key)

    def get_weather_at_loc(self, location: str):
        try:
            self.location = location
            self.obs = self.owm.weather_at_place(self.location)
            self.weather = self.obs.get_weather()
            self.loc = self.obs.get_location()
            self.forecaster = self.owm.three_hours_forecast(self.location)
        except (api_response_error.NotFoundError, api_call_error.APICallError):
            self.location = "Error"

    def get_forecast(self, degrees: str) -> [(str, str, str)]:
        forecast = self.forecaster.get_forecast()
        fc = []

        for w in forecast:
            time = w.get_reference_time("date").astimezone(timezone("US/Eastern"))
            day = day_abbr[time.weekday()]

            if "11:00" in str(time):
                self.weather = w
                temp = self.get_temperature(degrees)
                img_path = self.get_weather_icon()

                fc.append((day, temp, img_path))

        return fc

    def get_temperature(self, degrees: str) -> str:
        return str(round(self.weather.get_temperature(degrees)["temp"]))

    def get_hilo_temperature(self, degrees: str) -> str:
        return f"{round(self.weather.get_temperature(degrees)['temp_max'])}°/ {round(self.weather.get_temperature(degrees)['temp_min'])}°"

    def get_humidity(self) -> str:
        return str(self.weather.get_humidity())

    def get_wind_speed(self, degrees: str) -> str:
        if degrees == "fahrenheit":
            mph = self.weather.get_wind()["speed"] * (3600 / 1609.344)
            return f"{str(round(mph, 1))} mph"

        return f"{str(self.weather.get_wind()['speed'])} m/s"

    def get_pressure(self) -> str:
        return str(round(self.weather.get_pressure()["press"]))

    def get_location(self) -> str:
        return f"{self.loc.get_name()}, {self.loc.get_country()}"

    def get_weather_icon(self) -> str:
        status = self.weather.get_status().lower()

        if status == "clear" or status == "clouds" or status == "drizzle" or status == "rain" or status == "snow" or status == "thunderstorm":
            return f"icons/{status}.png"
        else:
            return "icons/mist.png"

    def get_weather_description(self) -> str:
        return self.weather.get_detailed_status().capitalize()
