import tkinter as tk
from PIL import ImageTk, Image
from Weather import *


class View:
    temp = ""
    hilo_temp = ""
    weather_status = ""
    degree_unit = "fahrenheit"
    img_path = ""
    location = ""
    humidity = ""
    wind_speed = ""
    pressure = ""

    def update_weather(self, loc: str):
        self.owm.get_weather_at_loc(loc)

        if self.owm.location != "Error":
            self.temp = self.owm.get_temperature(self.degree_unit)
            self.hilo_temp = self.owm.get_hilo_temperature(self.degree_unit)
            self.weather_status = self.owm.get_weather_description()
            self.img_path = self.owm.get_weather_icon()
            self.location = self.owm.get_location()
            self.humidity = self.owm.get_humidity()
            self.wind_speed = self.owm.get_wind_speed(self.degree_unit)
            self.pressure = self.owm.get_pressure()

            self.update_gui()
            self.show_forecast()
        else:
            self.error_label.grid(row=1, column=1, columnspan=2)

    def update_gui(self):
        self.loc_label.config(text=self.location)
        self.weather_label.config(text=self.weather_status)
        self.temp_label.config(text=f"{self.temp}°")
        self.hilo_temp_label.config(text=self.hilo_temp)
        self.humidity_label.config(text=f"{self.humidity}%")
        self.wind_label.config(text=f"{self.wind_speed}")
        self.pressure_label.config(text=f"{self.pressure} hPa")
        self.display_image(self.img_path, self.weather_icon, False)

    def show_forecast(self):
        forecast = self.owm.get_forecast(self.degree_unit)

        self.weekday1_label.config(text=forecast[0][0])
        self.temp1_label.config(text=f"{forecast[0][1]}°")
        self.display_image(forecast[0][2], self.icon1_label, True)

        self.weekday2_label.config(text=forecast[1][0])
        self.temp2_label.config(text=f"{forecast[1][1]}°")
        self.display_image(forecast[1][2], self.icon2_label, True)

        self.weekday3_label.config(text=forecast[2][0])
        self.temp3_label.config(text=f"{forecast[2][1]}°")
        self.display_image(forecast[2][2], self.icon3_label, True)

        self.weekday4_label.config(text=forecast[3][0])
        self.temp4_label.config(text=f"{forecast[3][1]}°")
        self.display_image(forecast[3][2], self.icon4_label, True)

        self.weekday5_label.config(text=forecast[4][0])
        self.temp5_label.config(text=f"{forecast[4][1]}°")
        self.display_image(forecast[4][2], self.icon5_label, True)

    def display_image(self, path: str, widget: tk.Label, resize: bool):
        image = Image.open(path)

        if resize:
            image = image.resize((75, 75), Image.ANTIALIAS)

        img = ImageTk.PhotoImage(image)
        widget.config(image=img)
        widget.image = img

    def focus_entry(self, event):
        self.entry.config(fg="black", state=tk.NORMAL)
        self.entry.delete(0, tk.END)

    def change_city(self, event=None):
        self.error_label.grid_forget()
        self.update_weather(self.entry.get())

        self.entry.delete(0, tk.END)
        self.entry.insert(0, "Enter a city name.")
        self.entry.config(fg="gray", state=tk.DISABLED)

    def change_degree_unit(self):
        if self.degree_option.get() == 1:
            self.degree_unit = "fahrenheit"
        elif self.degree_option.get() == 2:
            self.degree_unit = "celsius"

        self.update_weather(self.location)

    def __init__(self, root: tk.Tk):
        self.owm = Weather()

        font = "Segoe UI Semilight"
        bg_color = "#408ab4"
        text_fg_color = "#c5f0a4"
        accent_color = "#fff8a6"

        root.title("Weather App")
        root.state("zoomed")
        root.config(bg=bg_color)

        # ---- MENU ----

        menu = tk.Menu(root)
        root.config(menu=menu)

        degree_menu = tk.Menu(menu)
        self.degree_option = tk.IntVar()
        menu.add_cascade(label="Degree Unit", menu=degree_menu)
        degree_menu.add_radiobutton(label="Fahrenheit", var=self.degree_option, value=1,
                                    command=self.change_degree_unit)
        degree_menu.add_radiobutton(label="Celsius", var=self.degree_option, value=2,
                                    command=self.change_degree_unit)

        exit_menu = tk.Menu(menu)
        menu.add_cascade(label="Exit", menu=exit_menu)
        exit_menu.add_command(label="Quit", command=root.quit)

        # ---- MAIN FRAMES ----

        weather_frame = tk.Frame(root, bg=bg_color)
        forecast_frame = tk.Frame(root, bg=bg_color)

        weather_frame.grid(row=0, column=1, sticky="nsew")
        forecast_frame.grid(row=0, column=2, ipadx=50, sticky="nsew")

        root.rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1, uniform="side")
        root.columnconfigure(1, weight=2, uniform="main")
        root.columnconfigure(2, weight=2, uniform="main")
        root.columnconfigure(3, weight=1, uniform="side")

        # ---- WEATHER_FRAME ----

        # create frames
        entry_frame = tk.Frame(weather_frame, width=450, height=50, bg=bg_color)
        entry_frame.grid_propagate(0)
        temp_frame = tk.Frame(weather_frame, height=100, width=200, bg=bg_color)
        temp_frame.grid_propagate(0)
        features_frame = tk.Frame(weather_frame, bg=bg_color)

        # layout frames
        entry_frame.grid(row=0, pady=(20, 0))
        temp_frame.grid(row=4)
        features_frame.grid(row=6, ipadx=115, padx=15, pady=(0, 20))

        # create widgets for entry_frame
        self.entry = tk.Entry(entry_frame, font=(font, 12), width=40)
        self.entry.insert(0, "Enter a city name.")
        self.entry.config(fg="gray", state=tk.DISABLED)
        self.entry.bind("<Button-1>", self.focus_entry)
        self.entry.bind("<Return>", self.change_city)
        search_button = tk.Button(entry_frame, text="Search", font=(font, 10),
                                  bg=accent_color, activebackground="#d4cd76",
                                  command=self.change_city)
        self.error_label = tk.Label(entry_frame, text="Invalid city name.",
                                    font=(font, 9), fg="#d54040",
                                    bg=bg_color)

        # layout widgets for entry_frame
        self.entry.grid(row=0, column=1, padx=5)
        search_button.grid(row=0, column=2, padx=5)

        # layout entry_frame
        entry_frame.columnconfigure(0, weight=1)
        entry_frame.columnconfigure(3, weight=1)

        # create widgets for temp_frame
        self.temp_label = tk.Label(temp_frame, font=(font, 65), fg=text_fg_color,
                                   bg=bg_color)

        # layout widgets for temp_frame
        self.temp_label.grid(row=0, column=1)

        # layout temp_frame
        temp_frame.rowconfigure(1, weight=1)
        temp_frame.columnconfigure(0, weight=1)
        temp_frame.columnconfigure(2, weight=1)

        # create widgets for features_frame
        humidity_icon = tk.Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/humidity.png", humidity_icon, False)
        wind_icon = tk.Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/wind.png", wind_icon, False)
        pressure_icon = tk.Label(features_frame, bg=bg_color, height=50, width=50)
        self.display_image("icons/pressure.png", pressure_icon, False)
        self.humidity_label = tk.Label(features_frame, font=(font, 12), fg=accent_color, bg=bg_color)
        self.wind_label = tk.Label(features_frame, font=(font, 12), fg=accent_color,
                                   bg=bg_color)
        self.pressure_label = tk.Label(features_frame, font=(font, 12), fg=accent_color, bg=bg_color)

        # layout widgets for features_frame
        humidity_icon.grid(row=0, column=0)
        wind_icon.grid(row=0, column=1)
        pressure_icon.grid(row=0, column=2)
        self.humidity_label.grid(row=1, column=0)
        self.wind_label.grid(row=1, column=1)
        self.pressure_label.grid(row=1, column=2)

        # layout features_frame
        features_frame.columnconfigure(0, weight=1, uniform="features")
        features_frame.columnconfigure(1, weight=1, uniform="features")
        features_frame.columnconfigure(2, weight=1, uniform="features")

        # create widgets for weather_frame
        self.loc_label = tk.Label(weather_frame, font=(font, 25), fg=text_fg_color,
                                  bg=bg_color)
        self.weather_label = tk.Label(weather_frame, font=(font, 14), fg=accent_color,
                                      bg=bg_color)
        self.weather_icon = tk.Label(weather_frame, bg=bg_color, height=160, width=170)
        self.hilo_temp_label = tk.Label(weather_frame, font=(font, 15), fg=accent_color, bg=bg_color)

        # layout widgets for weather_frame
        self.loc_label.grid(row=1)
        self.weather_label.grid(row=2, pady=(0, 10))
        self.weather_icon.grid(row=3)
        self.hilo_temp_label.grid(row=5, pady=5)

        # layout weather_frame
        weather_frame.rowconfigure(0, weight=1)
        weather_frame.rowconfigure(6, weight=1)
        weather_frame.columnconfigure(0, weight=1)

        # ---- FORECAST_FRAME ----

        # create frames
        day1_frame = tk.Frame(forecast_frame, height=170, width=170, highlightbackground="white",
                              highlightcolor="white", highlightthickness=3, bd=0, bg=bg_color)
        day1_frame.grid_propagate(0)
        day2_frame = tk.Frame(forecast_frame, height=170, width=170, highlightbackground="white",
                              highlightcolor="white", highlightthickness=3, bd=0, bg=bg_color)
        day2_frame.grid_propagate(0)
        day3_frame = tk.Frame(forecast_frame, height=170, width=170, highlightbackground="white",
                              highlightcolor="white", highlightthickness=3, bd=0, bg=bg_color)
        day3_frame.grid_propagate(0)
        day4_frame = tk.Frame(forecast_frame, height=170, width=170, highlightbackground="white",
                              highlightcolor="white", highlightthickness=3, bd=0, bg=bg_color)
        day4_frame.grid_propagate(0)
        day5_frame = tk.Frame(forecast_frame, height=170, width=170, highlightbackground="white",
                              highlightcolor="white", highlightthickness=3, bd=0, bg=bg_color)
        day5_frame.grid_propagate(0)

        # layout frames
        day1_frame.grid(row=1, column=0)
        day2_frame.grid(row=1, column=1)
        day3_frame.grid(row=2, column=0)
        day4_frame.grid(row=2, column=1)
        day5_frame.grid(row=3, column=0, columnspan=2)

        day1_frame.rowconfigure(0, weight=1)
        day1_frame.rowconfigure(1, weight=2)
        day1_frame.rowconfigure(2, weight=1)
        day1_frame.columnconfigure(0, weight=1)
        day2_frame.rowconfigure(0, weight=1)
        day2_frame.rowconfigure(1, weight=2)
        day2_frame.rowconfigure(2, weight=1)
        day2_frame.columnconfigure(0, weight=1)
        day3_frame.rowconfigure(0, weight=1)
        day3_frame.rowconfigure(1, weight=2)
        day3_frame.rowconfigure(2, weight=1)
        day3_frame.columnconfigure(0, weight=1)
        day4_frame.rowconfigure(0, weight=1)
        day4_frame.rowconfigure(1, weight=2)
        day4_frame.rowconfigure(2, weight=1)
        day4_frame.columnconfigure(0, weight=1)
        day5_frame.rowconfigure(0, weight=1)
        day5_frame.rowconfigure(1, weight=2)
        day5_frame.rowconfigure(2, weight=1)
        day5_frame.columnconfigure(0, weight=1)

        # day1 widgets
        self.weekday1_label = tk.Label(day1_frame, font=(font, 18), fg=text_fg_color, bg=bg_color)
        self.icon1_label = tk.Label(day1_frame, bg=bg_color)
        self.temp1_label = tk.Label(day1_frame, font=(font, 22), fg=accent_color, bg=bg_color)

        self.weekday1_label.grid(row=0)
        self.icon1_label.grid(row=1)
        self.temp1_label.grid(row=2)

        # day2 widgets
        self.weekday2_label = tk.Label(day2_frame, text="Monday", font=(font, 18), fg=text_fg_color, bg=bg_color)
        self.icon2_label = tk.Label(day2_frame, text="IMAGE", bg=bg_color)
        self.temp2_label = tk.Label(day2_frame, text="93°", font=(font, 22), fg=accent_color, bg=bg_color)

        self.weekday2_label.grid(row=0)
        self.icon2_label.grid(row=1)
        self.temp2_label.grid(row=2)

        # day3 widgets
        self.weekday3_label = tk.Label(day3_frame, text="Monday", font=(font, 18), fg=text_fg_color, bg=bg_color)
        self.icon3_label = tk.Label(day3_frame, text="IMAGE", bg=bg_color)
        self.temp3_label = tk.Label(day3_frame, text="93°", font=(font, 22), fg=accent_color, bg=bg_color)

        self.weekday3_label.grid(row=0)
        self.icon3_label.grid(row=1)
        self.temp3_label.grid(row=2)

        # day4 widgets
        self.weekday4_label = tk.Label(day4_frame, text="Monday", font=(font, 18), fg=text_fg_color, bg=bg_color)
        self.icon4_label = tk.Label(day4_frame, text="IMAGE", bg=bg_color)
        self.temp4_label = tk.Label(day4_frame, text="93°", font=(font, 22), fg=accent_color, bg=bg_color)

        self.weekday4_label.grid(row=0)
        self.icon4_label.grid(row=1)
        self.temp4_label.grid(row=2)

        # day5 widgets
        self.weekday5_label = tk.Label(day5_frame, text="Monday", font=(font, 18), fg=text_fg_color, bg=bg_color)
        self.icon5_label = tk.Label(day5_frame, text="IMAGE", bg=bg_color)
        self.temp5_label = tk.Label(day5_frame, text="93°", font=(font, 22), fg=accent_color, bg=bg_color)

        self.weekday5_label.grid(row=0)
        self.icon5_label.grid(row=1)
        self.temp5_label.grid(row=2)

        # layout forecast_frame
        forecast_frame.rowconfigure(0, weight=1)
        forecast_frame.rowconfigure(1, weight=1)
        forecast_frame.rowconfigure(2, weight=1)
        forecast_frame.rowconfigure(3, weight=1)
        forecast_frame.rowconfigure(4, weight=1)
        forecast_frame.columnconfigure(0, weight=1, uniform="forecast")
        forecast_frame.columnconfigure(1, weight=1, uniform="forecast")

        # ---- FILL INFO ----
        self.update_weather("London")


window = tk.Tk()
weather_app = View(window)
window.mainloop()
