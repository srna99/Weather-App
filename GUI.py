from tkinter import *
from PIL import Image, ImageTk
import requests
from urllib.request import urlopen
from io import BytesIO
import Weather

root = Tk()
root.title("Weather App")
root.geometry("350x500")

url = Weather.icon_url
u = urlopen(url)
data = u.read()
u.close()

img = Image.open(BytesIO(data))
photo = ImageTk.PhotoImage(img)

# URL = "http://www.universeofsymbolism.com/images/ram-spirit-animal.jpg"
# u = urlopen(URL)
# raw_data = u.read()
# u.close()
#
# im = Image.open(BytesIO(raw_data))
# photo = ImageTk.PhotoImage(im)
#
# label = tk.Label(image=photo)
# label.image = photo
# label.pack()
#
# root.mainloop()


loc_label = Label(text="London", font=("Arial", 20))
weather_icon = Label(image=photo)
weather_icon.image = photo
temp_label = Label(text="80", font=("Arial", 70))

loc_label.grid(row=0)
weather_icon.grid(row=1)
temp_label.grid(row=2)

root.rowconfigure(0, weight=5)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)
root.columnconfigure(0, weight=1)

root.mainloop()
