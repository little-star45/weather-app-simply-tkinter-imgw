from tkinter import *
import requests
import json

root = Tk()

root.geometry("1050x550")

# root.iconbitmap("ikona_bitcoin.ico")

api_stacje = requests.get(f"https://danepubliczne.imgw.pl/api/data/synop")

api2 = json.loads(api_stacje.content)
stacje = []

for i in range(len(api2)):
  stacja = api2[i]["stacja"]
  stacje.append(stacja)


#4 FUNKCJA SZUKAJACA MIEJSCOWOŚCI PO KODZIE POCZTOWYM
def zip_LookUp_fun(event):

  try:
    #my_Label1 = Label(root, text= " ")
    #my_Label1.place(relx = 0.5, rely = 0.5, anchor = CENTER)

    wpisane = zip.get()
    wpisane_polskie = wpisane

    polskie_znaki = ["ó", "ł", "ę", "ą", "ć", "ź", "ż", "ń", "ś"," "]
    niepolskie_znaki = ["o", "l", "e", "a", "c", "z", "z", "n", "s",""]

    miejscownosc = wpisane_polskie.lower()
    j = 0
    nowe_miejscowosc = ""

    for i in range(len(miejscownosc)):
        if miejscownosc[i] in polskie_znaki:
            j = polskie_znaki.index(miejscownosc[i])
            nowe_miejscowosc += niepolskie_znaki[j]
        else:
            nowe_miejscowosc += miejscownosc[i]
            
    wpisane = nowe_miejscowosc

    api_request = requests.get(f"https://danepubliczne.imgw.pl/api/data/synop/station/{wpisane}")

    api = json.loads(api_request.content)

    #stacja = api["stacja"]
    godz = api["godzina_pomiaru"]
    data = api["data_pomiaru"]
    temp = api["temperatura"]
    pr_wiatr = api["predkosc_wiatru"]
    opad = api["suma_opadu"]

    weather_colour = "#00e400"

    root.configure(background=weather_colour)  #ustawianie koloru tła
    my_Label1 = Label(root, text= f" Stacja : {wpisane_polskie.title()}\n Godz: {godz} \n Data: {data} \n Temperatura [stC] :{temp} \n Prędkość wiatru [m/s] : {pr_wiatr} \n Deszcz [mm] : {opad}", font=("Helvetica", 18), bg=weather_colour)
    my_Label1.place(relx=0.5, rely=0.6, anchor=CENTER)

  except:
	    api = "Error..."

#dodanie Entry Box do wpisywania kodu pocztowego i wyszukiwania po tym pogody
my_Label4 = Label(root,text=f"Dostępne miejscowości : \n{stacje[0:12]}\n{stacje[12:24]}\n{stacje[24:36]}\n{stacje[36:48]}\n{stacje[48:62]}")
my_Label4.place(relx=0.5, rely=0.17, anchor=CENTER)

my_Label3 = Label(root, text="Wpisz miejscowość do sprawdzenia pogody:")
my_Label3.place(relx=0.5, rely=0.05, anchor=CENTER)

zip = Entry(root)
zip.place(relx=0.5, rely=0.30, anchor=CENTER)

zip_Button = Button(root, text="Potwierdź", command=lambda:zip_LookUp_fun(True))
zip_Button.place(relx=0.5, rely=0.35, anchor=CENTER)

root.bind('<Return>', zip_LookUp_fun)

root.mainloop()
