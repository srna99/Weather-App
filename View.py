from tkinter import *
from PIL import ImageTk, Image
from Weather import *


class View:
    owm = Weather()
    temp = ""
    degree_unit = "fahrenheit"
    img_path = ""
    location = ""
    humidity = ""
    wind_speed = ""
    pressure = ""

    def __init__(self, root: Tk):
        root.title("Weather App")
        root.geometry("325x500")
        root.config(bg="gray")

        # create frames
        entry_frame = Frame(root, width=300, height=50, padx=20, bg="gray")
        entry_frame.grid_propagate(0)
        temp_frame = Frame(root, bg="gray")
        features_frame = Frame(root, width=300, height=100, bg="gray")

        # layout frames
        entry_frame.grid(row=1)
        temp_frame.grid(row=4)
        features_frame.grid(row=5, ipadx=50, pady=10)

        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        features_frame.columnconfigure(2, weight=1)

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

        # create widgets for features_frame
        humidity_icon = Label(features_frame, bg="gray", height=50, width=50)
        self.display_image("icons/humidity.png", humidity_icon)
        wind_icon = Label(features_frame, bg="gray", height=50, width=50)
        self.display_image("icons/wind.png", wind_icon)
        pressure_icon = Label(features_frame, bg="gray", height=50, width=50)
        self.display_image("icons/pressure.png", pressure_icon)
        self.humidity_label = Label(features_frame, text="23%", font=("Arial", 10), fg="white",
                                    bg="gray")
        self.wind_label = Label(features_frame, text="4 m/s", font=("Arial", 10), fg="white", bg="gray")
        self.pressure_label = Label(features_frame, text="873 hPa", font=("Arial", 10), fg="white",
                                    bg="gray")

        # layout widgets for features_frame
        humidity_icon.grid(row=0, column=0)
        wind_icon.grid(row=0, column=1)
        pressure_icon.grid(row=0, column=2)
        self.humidity_label.grid(row=1, column=0)
        self.wind_label.grid(row=1, column=1)
        self.pressure_label.grid(row=1, column=2)

        # menu
        menu = Menu(root)
        root.config(menu=menu)

        degree_menu = Menu(menu)
        self.degree_option = IntVar()
        menu.add_cascade(label="Degree Unit", menu=degree_menu)
        degree_menu.add_radiobutton(label="Fahrenheit", var=self.degree_option, value=1,
                                    command=self.change_degree_unit)
        degree_menu.add_radiobutton(label="Celsius", var=self.degree_option, value=2,
                                    command=self.change_degree_unit)

        exit_menu = Menu(menu)
        menu.add_cascade(label="Exit", menu=exit_menu)
        exit_menu.add_command(label="Quit", command=root.quit)

        # create widgets for root
        self.loc_label = Label(root, font=("Arial", 20), fg="white", bg="gray")
        self.weather_icon = Label(root, bg="gray", height=173, width=173)

        # layout widgets for root
        self.loc_label.grid(row=2, column=0, columnspan=2)
        self.weather_icon.grid(row=3, column=0, columnspan=2)

        # layout root
        root.rowconfigure(0, weight=1)
        root.rowconfigure(6, weight=1)
        root.columnconfigure(0, weight=1)

        self.update_weather("London")

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)

        if self.owm.location != "Error":
            self.temp = self.owm.get_temperature(self.degree_unit)
            self.img_path = self.owm.get_weather_icon()
            self.location = self.owm.get_location()
            self.humidity = self.owm.get_humidity()
            self.wind_speed = self.owm.get_wind_speed()
            self.pressure = self.owm.get_pressure()

            self.update_gui()
        else:
            self.error_label.grid(row=1, column=0, columnspan=2)

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.temp_label.config(text=self.temp)
        self.humidity_label.config(text=f"{self.humidity}%")
        self.wind_label.config(text=f"{self.wind_speed} m/s")
        self.pressure_label.config(text=f"{self.pressure} hPa")

        self.display_image(self.img_path, self.weather_icon)

    def display_image(self, path: str, widget: Label):
        image = ImageTk.PhotoImage(Image.open(path))
        widget.config(image=image)
        widget.image = image

    def focus_entry(self, event: Event):
        self.entry.config(fg="black", state=NORMAL)
        self.entry.delete(0, END)

    def change_city(self, event: Event):
        self.error_label.grid_forget()
        self.update_weather(self.entry.get())

        self.entry.delete(0, END)
        self.entry.insert(0, "Enter city name")
        self.entry.config(fg="gray", state=DISABLED)

    def change_degree_unit(self):
        if self.degree_option.get() == 1:
            self.degree_unit = "fahrenheit"
        elif self.degree_option.get() == 2:
            self.degree_unit = "celsius"

        self.update_weather(self.location)


window = Tk()
weather_app = View(window)
window.mainloop()
