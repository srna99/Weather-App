from tkinter import *
from PIL import ImageTk, Image
import Controller

root = Tk()
root.title("Weather App")
root.geometry("325x500")
root.config(bg="gray")

img = ImageTk.PhotoImage(Image.open(Controller.img_path))

loc_label = Label(text=Controller.location, font=("Arial", 20), fg="white", bg="gray")
weather_icon = Label(image=img, bg="gray")
temp_label = Label(text=f"{Controller.temp}", font=("Arial", 70), fg="white", bg="gray")

loc_label.grid(row=1)
weather_icon.grid(row=2)
temp_label.grid(row=3)

root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)
root.rowconfigure(3, weight=0)
root.rowconfigure(4, weight=2)
root.columnconfigure(0, weight=1)

root.mainloop()
