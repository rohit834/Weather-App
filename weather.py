from tkinter import *
import tkinter as tk
from tkinter import ttk, messagebox
from opencage.geocoder import OpenCageGeocode
from datetime import datetime
import requests
import pytz
from timezonefinder import TimezoneFinder

root = Tk()
root.title("Weather App")
root.geometry("500x650+300+200")
root.resizable(False, False)

def get_coordinates(city):
    api_key = "637dae5bb49f4988b9b07aba809db751"  # Replace with your OpenCage API key
    geocoder = OpenCageGeocode(api_key)
    
    result = geocoder.geocode(city)
    
    if result and len(result):
        location = result[0]['geometry']
        return location['lat'], location['lng']
    
    return None

def getweather():
    try:
        city = textfield.get()

        coordinates = get_coordinates(city)

        if coordinates is None:
            raise Exception("City not found")

        lat, lng = coordinates

        obj = TimezoneFinder()
        result = obj.timezone_at(lng=lng, lat=lat)
        print(result)

        home = pytz.timezone(result)
        local_time = datetime.now(home)
        current_time = local_time.strftime("%I:%M %p")
        clock.config(text=current_time)
        name.config(text="CURRENT WEATHER")

        # weather
        api = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lng}&appid=602a1ce6b9592384892a0e702e008040"

        json_data = requests.get(api).json()
        print(json_data)
        condition = json_data['weather'][0]['main']
        description = json_data['weather'][0]['description']
        temp = int(json_data['main']['temp'] - 273.15)
        pressure = json_data['main']['pressure']
        humidity = json_data['main']['humidity']
        wind = json_data['wind']['speed']

        t.config(text=f"{temp}°C")  # Update temperature label
        c.config(text=f"{condition} | FEELS LIKE {temp}°C")
        w.config(text=f"{wind} m/s")
        h.config(text=f"{humidity}%")
        d.config(text=f"{description}")
        p.config(text=f"{pressure} hPa")

    except Exception as e:
        print(f"Error during geocoding: {e}")
        messagebox.showerror("Weather APP", "Invalid Entry")

# search box
search_image = PhotoImage(file=r"E:\Weather-App-master\Weather-App-master\search.png")

myimage = Label(image=search_image)
myimage.place(x=10, y=20)

textfield = tk.Entry(root, font=("Arial", 25, "bold"), justify="center", width=17, bg="#404040", border=0, fg="white")
textfield.place(x=80, y=40)
textfield.focus()

search_icon = PhotoImage(file=r"E:\Weather-App-master\Weather-App-master\search_icon.png")
myimage_icon = Button(image=search_icon, borderwidth=0, cursor="hand2", bg="#404040", border=0,
                      activebackground="#404040", command=getweather)
myimage_icon.place(x=390, y=34)

# logo
logo_image = PhotoImage(file=r"E:\Weather-App-master\Weather-App-master\logo.png")
logo = Label(image=logo_image)
logo.place(x=10, y=100)

# button box
frame_image = PhotoImage(file=r"E:\Weather-App-master\Weather-App-master\addbox.png")
frame = Label(image=frame_image)
frame.pack(padx=5, pady=5, side=BOTTOM)

# time
name = Label(root, font=("arial", 15, "bold"))
name.place(x=250, y=150)
clock = Label(root, font=("Helvetica", 20))
clock.place(x=250, y=100)

# label
label1 = Label(root, text="WIND", font=("Helvetica", 10, "bold"), bg="#404040", fg="white")
label1.place(x=40, y=595)

label2 = Label(root, text="HUMID", font=("Helvetica", 10, "bold"), bg="#404040", fg="white")
label2.place(x=140, y=595)

label3 = Label(root, text="INFO", font=("Helvetica", 10, "bold"), bg="#404040", fg="white")
label3.place(x=240, y=595)

label4 = Label(root, text="FORCE", font=("Helvetica", 10, "bold"), bg="#404040", fg="white")
label4.place(x=350, y=595)

t = Label(root, font=("arial", 70, "bold"), fg="red")
t.place(x=10, y=350)
c = Label(root, font=("arial", 15, "bold"))
c.place(x=10, y=450)

w = Label(text="...", font=("arial", 9, "bold"))
w.place(x=81, y=595)
h = Label(text="...", font=("arial", 9, "bold"))
h.place(x=194, y=595)
d = Label(text="...", font=("arial", 9, "bold"))
d.place(x=280, y=595)
p = Label(text="...", font=("arial", 9, "bold"))
p.place(x=400, y=595)

root.mainloop()
