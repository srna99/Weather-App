from Weather import *

owm = Weather()
temp = owm.get_temperature("fahrenheit")
img_path = owm.get_weather_icon()
location = owm.get_location()
