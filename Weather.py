from pyowm import *
import Key

owm = OWM(Key.api_key)

obs = owm.weather_at_place("London")
weather = obs.get_weather()
loc = obs.get_location()

temp = weather.get_temperature("fahrenheit")["temp"]
print(round(temp))
status = weather.get_status()
print(status)
icon_url = weather.get_weather_icon_url()
print(icon_url)
location = loc.get_name()
print(location)
