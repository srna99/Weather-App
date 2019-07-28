from tkinter import *
from PIL import ImageTk, Image

root = Tk()
root.title("Weather App")
root.geometry("350x500")

path = "icons/clear.png"
img = ImageTk.PhotoImage(Image.open(path))

loc_label = Label(text="London", font=("Arial", 20))
weather_icon = Label(image=img)

temp_label = Label(text="80", font=("Arial", 70))

loc_label.grid(row=0)
weather_icon.grid(row=1)
temp_label.grid(row=2)

root.rowconfigure(0, weight=5)
root.rowconfigure(1, weight=1)
root.rowconfigure(2, weight=5)
root.columnconfigure(0, weight=1)

root.mainloop()
