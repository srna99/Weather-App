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

        # create frames
        entry_frame = Frame(root, width=300, height=50, padx=20, bg="gray")
        entry_frame.grid_propagate(0)
        temp_frame = Frame(root, bg="gray")

        # layout frames
        entry_frame.grid(row=1)
        temp_frame.grid(row=4)

        # create widgets for entry_frame
        self.entry = Entry(entry_frame, font=("Arial", 12))
        self.entry.insert(0, "Enter a city name.")
        self.entry.config(fg="gray", state=DISABLED)
        self.entry.bind("<Button-1>", self.focus_entry)
        self.entry.bind("<Return>", self.change_city)
        get_weather_button = Button(entry_frame, text="Search", font=("Arial", 9), bg="dark gray",
                                    command=self.change_city)
        self.error_label = Label(entry_frame, text="Invalid city name.", font=("Arial", 9), fg="#c80815",
                                 bg="gray")

        # layout widgets for entry_frame
        self.entry.grid(row=0, column=0, padx=5)
        get_weather_button.grid(row=0, column=1, padx=5)

        # create widgets for temp_frame
        self.temp_label = Label(temp_frame, font=("Arial", 70), fg="white", bg="gray")
        degrees_label = Label(temp_frame, text="°", font=("Arial", 40), fg="white", bg="gray")

        # layout widgets for temp_frame
        self.temp_label.grid(row=0, rowspan=2, column=0)
        degrees_label.grid(row=0, column=1)

        # create widgets for root
        self.loc_label = Label(root, font=("Arial", 20), fg="white", bg="gray")
        self.weather_icon = Label(root, bg="gray", height=173, width=173)

        # layout widgets for root
        self.loc_label.grid(row=2, column=0, columnspan=2)
        self.weather_icon.grid(row=3, column=0, columnspan=2)

        # layout root
        root.rowconfigure(0, weight=1)
        root.rowconfigure(5, weight=2)
        root.columnconfigure(0, weight=1)

        self.update_weather("London")

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)

        if self.owm.location != "Error":
            self.temp = self.owm.get_temperature("fahrenheit")
            self.img_path = self.owm.get_weather_icon()
            self.location = self.owm.get_location()

            self.update_gui()
        else:
            self.error_label.grid(row=1, column=0, columnspan=2)

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.temp_label.config(text=self.temp)

        image = ImageTk.PhotoImage(Image.open(self.img_path))
        self.weather_icon.config(image=image)
        self.weather_icon.image = image

    def focus_entry(self, event):
        self.entry.config(fg="black", state=NORMAL)
        self.entry.delete(0, END)

    def change_city(self, event):
        self.error_label.grid_forget()
        self.update_weather(self.entry.get())

        self.entry.delete(0, END)
        self.entry.insert(0, "Enter city name")
        self.entry.config(fg="gray", state=DISABLED)


window = Tk()
weather_app = View(window)
window.mainloop()
