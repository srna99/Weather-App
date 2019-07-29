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

        entry_frame = Frame(root, height=40, padx=20, pady=10, bg="gray")
        entry_frame.grid(row=1)

        self.entry = Entry(entry_frame, font=("Arial", 12))
        get_weather_button = Button(entry_frame, text="Search", font=("Arial", 9), bg="dark gray", command=lambda: self.update_weather(self.entry.get()))

        self.entry.pack(padx=5, expand=TRUE, side=LEFT)
        get_weather_button.pack(expand=TRUE, padx=5, side=LEFT)

        self.loc_label = Label(root, font=("Arial", 20), fg="white", bg="gray")
        self.weather_icon = Label(root, bg="gray")
        self.temp_label = Label(root, font=("Arial", 70), fg="white", bg="gray")

        self.update_weather("London")

        self.loc_label.grid(row=2, column=0, columnspan=2)
        self.weather_icon.grid(row=3, column=0, columnspan=2)
        self.temp_label.grid(row=4, column=0, columnspan=2)

        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=0)
        root.rowconfigure(3, weight=0)
        root.rowconfigure(4, weight=0)
        root.rowconfigure(5, weight=2)
        root.columnconfigure(0, weight=1)

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)
        self.temp = self.owm.get_temperature("fahrenheit")
        self.img_path = self.owm.get_weather_icon()
        self.location = self.owm.get_location()

        self.update_gui()

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.temp_label.config(text=self.temp)

        image = ImageTk.PhotoImage(Image.open(self.img_path))
        self.weather_icon.config(image=image)
        self.weather_icon.image = image


window = Tk()
weather_app = View(window)
window.mainloop()
