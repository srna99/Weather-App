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
        bg_color = "#408ab4"
        text_fg_color = "#eeeeee"
        accent_color = "#f6ef98"
        error_color = "#d54040"

        root.title("Weather App")
        root.geometry("325x520")
        root.config(bg=bg_color)

        # create frames
        entry_frame = Frame(root, width=325, height=50, padx=45, bg=bg_color)
        entry_frame.grid_propagate(0)
        temp_frame = Frame(root, bg=bg_color)
        features_frame = Frame(root, width=325, bg=bg_color)

        # layout frames
        entry_frame.grid(row=0, pady=(15, 0))
        temp_frame.grid(row=3)
        features_frame.grid(row=4, ipadx=50, padx=20, pady=(0, 20))

        features_frame.columnconfigure(0, weight=1)
        features_frame.columnconfigure(1, weight=1)
        features_frame.columnconfigure(2, weight=1)

        # create widgets for entry_frame
        self.entry = Entry(entry_frame, font=("Segoe UI Semilight", 12))
        self.entry.insert(0, "Enter a city name.")
        self.entry.config(fg="gray", state=DISABLED)
        self.entry.bind("<Button-1>", self.focus_entry)
        self.entry.bind("<Return>", self.change_city)
        search_button = Button(entry_frame, text="Search", font=("Segoe UI Semilight", 10),
                               bg=accent_color, activebackground="#d4cd76", command=self.change_city)
        self.error_label = Label(entry_frame, text="Invalid city name.", font=("Segoe UI Semilight", 9),
                                 fg=error_color, bg=bg_color)

        # layout widgets for entry_frame
        self.entry.grid(row=0, column=0, padx=5)
        search_button.grid(row=0, column=1, padx=5)

        # create widgets for temp_frame
        self.temp_label = Label(temp_frame, font=("Segoe UI Semilight", 65), fg=text_fg_color,
                                bg=bg_color)
        degrees_label = Label(temp_frame, text="°", font=("Segoe UI Semilight", 40), fg=text_fg_color,
                              bg=bg_color)

        # layout widgets for temp_frame
        self.temp_label.grid(row=0, rowspan=2, column=0)
        degrees_label.grid(row=0, column=1)

        # layout for temp_frame
        temp_frame.columnconfigure(0, weight=2)
        temp_frame.columnconfigure(1, weight=1)

        # create widgets for features_frame
        humidity_icon = Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/humidity.png", humidity_icon)
        wind_icon = Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/wind.png", wind_icon)
        pressure_icon = Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/pressure.png", pressure_icon)
        self.humidity_label = Label(features_frame, font=("Segoe UI Semilight", 12), fg=accent_color,
                                    bg=bg_color)
        self.wind_label = Label(features_frame, font=("Segoe UI Semilight", 12), fg=accent_color,
                                bg=bg_color)
        self.pressure_label = Label(features_frame, font=("Segoe UI Semilight", 12), fg=accent_color,
                                    bg=bg_color)

        # layout widgets for features_frame
        humidity_icon.grid(row=0, column=0)
        wind_icon.grid(row=0, column=1)
        pressure_icon.grid(row=0, column=2)
        self.humidity_label.grid(row=1, column=0)
        self.wind_label.grid(row=1, column=1)
        self.pressure_label.grid(row=1, column=2)

        # layout for features_frame
        features_frame.columnconfigure(0, weight=1, uniform="features")
        features_frame.columnconfigure(1, weight=1, uniform="features")
        features_frame.columnconfigure(2, weight=1, uniform="features")

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
        self.loc_label = Label(root, font=("Segoe UI Semilight", 25), fg=accent_color, bg=bg_color)
        self.weather_icon = Label(root, bg=bg_color, height=160, width=170)

        # layout widgets for root
        self.loc_label.grid(row=1, column=0, pady=(0, 10))
        self.weather_icon.grid(row=2, column=0)

        # layout root
        root.rowconfigure(0, weight=1)
        root.rowconfigure(4, weight=1)
        root.columnconfigure(0, weight=1)

        self.update_weather("London")

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)

        if self.owm.location != "Error":
            self.temp = self.owm.get_temperature(self.degree_unit)
            self.img_path = self.owm.get_weather_icon()
            self.location = self.owm.get_location()
            self.humidity = self.owm.get_humidity()
            self.wind_speed = self.owm.get_wind_speed(self.degree_unit)
            self.pressure = self.owm.get_pressure()

            self.update_gui()
        else:
            self.error_label.grid(row=1, column=0, columnspan=2)

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.temp_label.config(text=self.temp)
        self.humidity_label.config(text=f"{self.humidity}%")
        self.wind_label.config(text=f"{self.wind_speed}")
        self.pressure_label.config(text=f"{self.pressure} hPa")
        self.display_image(self.img_path, self.weather_icon)

    def display_image(self, path: str, widget: Label):
        image = ImageTk.PhotoImage(Image.open(path))
        widget.config(image=image)
        widget.image = image

    def focus_entry(self, event):
        self.entry.config(fg="black", state=NORMAL)
        self.entry.delete(0, END)

    def change_city(self, event=None):
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
