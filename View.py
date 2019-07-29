from tkinter import *
from PIL import ImageTk, Image
from Weather import *


class View:
    owm = Weather()
    temp = ""
    img_path = ""
    location = ""

    def __init__(self, root: Tk):
        root.title("Weather App")
        root.geometry("325x500")
        root.config(bg="gray")

        self.loc_label = Label(font=("Arial", 20), fg="white", bg="gray")
        self.weather_icon = Label(bg="gray")
        self.temp_label = Label(font=("Arial", 70), fg="white", bg="gray")

        self.update_gui()

        self.loc_label.grid(row=1)
        self.weather_icon.grid(row=2)
        self.temp_label.grid(row=3)

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=0)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=0)
        root.rowconfigure(4, weight=2)
        root.columnconfigure(0, weight=1)

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)
        self.temp = self.owm.get_temperature("fahrenheit")
        self.img_path = self.owm.get_weather_icon()
        self.location = self.owm.get_location()

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.temp_label.config(text=self.temp)

        image = ImageTk.PhotoImage(Image.open(self.img_path))
        self.weather_icon.config(image=image)


window = Tk()
weather_app = View(window)
window.mainloop()
