import tkinter as tk
import psycopg2
import requests

'''faciliteiten uit de database ophalen'''
def get_station_facilities(station_name):
    conn = psycopg2.connect(
        host="51.145.236.173",
        database="stationszuil",
        user="postgres",
        password="W@leed123"
    )
    cursor = conn.cursor()
    query = "SELECT ov_bike, elevator, toilet, park_and_ride FROM station_service WHERE station_city = %s"
    cursor.execute(query, (station_name,))

    facilities = cursor.fetchone()
    conn.close()
    return facilities

def open_berichten_venster():
    geselecteerd_station = station_keuze.get()
    station_kiezen_venster.destroy()

    faciliteiten = get_station_facilities(geselecteerd_station)

    '''
    Maak een nieuw venster aan voor het weergeven van berichten met betrekking tot het geselecteerde station.
    '''
    berichten_venster = tk.Tk()
    berichten_venster.title(f"Station: {geselecteerd_station}")
    berichten_venster.configure(bg="#ffcf36")

    '''
    Maak een frame voor het welkomstbericht en de afbeelding
    '''
    welkomstbericht_frame = tk.Frame(berichten_venster, bg="#ffcf36")
    welkomstbericht_frame.pack(pady=5)

    '''
    Welkomstbericht
    '''
    welkomstbericht = tk.Label(welkomstbericht_frame, text=f"Welkom op : { geselecteerd_station}!", bg="#ffcf36", fg="#003082", font=("Helvetica", 18, "bold"))
    welkomstbericht.pack(side="left", padx=5)

    '''
    Voeg de afbeelding 'NS_logo.png' toe aan de rechterkant van het welkomstbericht
    '''
    ns_logo_image = tk.PhotoImage(file="NS_logo.png")
    ns_logo_image = ns_logo_image.subsample(15, 15)
    ns_logo_label = tk.Label(welkomstbericht_frame, image=ns_logo_image, bg="#ffcf36")
    ns_logo_label.photo = ns_logo_image
    ns_logo_label.pack(side="right")

    '''
    Voeg de titel 'Berichten' toe, kleiner en onder het welkomstbericht en naar links uitgelijnd
    '''
    titel_label = tk.Label(berichten_venster, text="Berichten", bg="#ffcf36", fg="#003082", font=("Helvetica", 11, "bold"))
    titel_label.pack(pady=5, anchor="w")

    '''
    Maak verbinding met de PostgreSQL-database met psycopg2
    '''
    conn = psycopg2.connect(
        host="51.145.236.173",
        database="stationszuil",
        user="postgres",
        password="W@leed123"
    )

    cursor = conn.cursor()

    '''
    Voer een query uit op de database om de meest recente berichten op te halen die goeggekeurd zijn door de NS moderators
    '''
    query = f"SELECT datum_en_tijd, bericht_tekst, naam_reiziger FROM bericht WHERE goedgekeurd = 'true' ORDER BY datum_en_tijd DESC LIMIT 5"
    cursor.execute(query)
    berichten = cursor.fetchall()

    conn.close()

    '''
    Toon de opgehaalde berichten in het berichtvenster
    '''
    for bericht in berichten:
        datum_en_tijd, tekst, naam = bericht
        datum_en_tijd = datum_en_tijd.strftime("%d-%m-%Y %H:%M")

        bericht_frame = tk.Frame(berichten_venster, bg="#D0E1FF")
        bericht_frame.pack(pady=10, padx=10, fill="both", expand=True)

        bericht_label = tk.Label(bericht_frame,
                                 text=f"{datum_en_tijd} - {naam}",
                                 bg="#D0E1FF", fg="#003082",
                                 font=("Helvetica", 12, "bold"))
        bericht_label.pack(anchor="w")

        bericht_label = tk.Label(bericht_frame, text=tekst, bg="#D0E1FF", fg="#003082")
        bericht_label.pack(anchor="w")

    '''
    Voer een aanroep uit naar de weer-API met de geselecteerde stad
    '''
    weerdata = get_weerbericht(geselecteerd_station)

    '''
    Toon het weerbericht onderaan het berichtvenster
    '''
    weer_label = tk.Label(berichten_venster,
                          text=f"Weerbericht\n{weerdata}",
                          bg="#ffcf36",
                          fg="#003082",
                          font=("Helvetica", 12, "bold"))
    weer_label.pack(pady=10)

    '''
    Voeg de afbeeldingen voor faciliteiten toe op basis van beschikbaarheid
    '''
    faciliteiten_frame = tk.Frame(berichten_venster, bg="#ffcf36")
    faciliteiten_frame.pack(pady=10)

    faciliteiten_label = tk.Label(faciliteiten_frame,
                                  text="Faciliteiten",
                                  bg="#ffcf36",
                                  fg="#003082",
                                  font=("Helvetica", 12, "bold"))
    faciliteiten_label.pack()

    if faciliteiten[0]:
        global img_fiets
        img_fiets = tk.PhotoImage(file="img_ovfiets.png")
        img_fiets = img_fiets.subsample(3, 3)
        fiets_label = tk.Label(faciliteiten_frame, image=img_fiets, bg="#ffcf36")
        fiets_label.photo = img_fiets
        fiets_label.pack(side="left", padx=5)

    if faciliteiten[2]:
        global img_toilet
        img_toilet = tk.PhotoImage(file="img_toilet.png")
        img_toilet = img_toilet.subsample(3, 3)
        toilet_label = tk.Label(faciliteiten_frame, image=img_toilet, bg="#ffcf36")
        toilet_label.photo = img_toilet
        toilet_label.pack(side="left", padx=5)

    if faciliteiten[3]:
        global img_pr
        img_pr = tk.PhotoImage(file="img_pr.png")
        img_pr = img_pr.subsample(3, 3)
        pr_label = tk.Label(faciliteiten_frame, image=img_pr, bg="#ffcf36")
        pr_label.photo = img_pr
        pr_label.pack(side="left", padx=5)

    if len(faciliteiten) > 4 and faciliteiten[4]:
        global img_lift
        img_lift = tk.PhotoImage(file="img_lift.png")
        img_lift = img_lift.subsample(3, 3)
        lift_label = tk.Label(faciliteiten_frame, image=img_lift, bg="#ffcf36")
        lift_label.photo = img_lift
        lift_label.pack(side="left", padx=5)

    berichten_venster.mainloop()


def get_weerbericht(stad):

    api_key = "e8986097586d00553665b3f82ef1e38f"
    base_url = f'https://api.openweathermap.org/data/2.5/weather?q={stad},nl&APPID={api_key}'
    response = requests.get(base_url)
    data = response.json()

    if response.status_code == 200:
        temperatuur = data["main"]["temp"]
        beschrijving = data["weather"][0]["description"]
        return f"{temperatuur}°C, {beschrijving}"
    else:
        return "Weerbericht niet beschikbaar"


'''
API-sleutel voor OpenWeatherMap
'''
api_key = "e8986097586d00553665b3f82ef1e38f"

'''Maak het hoofdvenster voor het selecteren van het station'''
station_kiezen_venster = tk.Tk()
station_kiezen_venster.title("Stationhalscherm")
station_kiezen_venster.configure(bg="#ffcf36")
'''
nieuwe afbeelding voor het venster voor stationselectie menu.
'''

photo = tk.PhotoImage(file="NS_logo.png")
photo = photo.subsample(10, 10)
image_label = tk.Label(station_kiezen_venster, image=photo, bg="#ffcf36")
image_label.photo = photo
image_label.pack()

label_kies_station = tk.Label(station_kiezen_venster,
                              text="Kies een station:",
                              font=("Helvetica", 12, "bold"),
                              bg="#ffcf36", fg="#003082")
label_kies_station.pack(pady=10)
'''
Label voor het selecteren van het station.
'''
stations = ["Arnhem", "Almere", "Amersfoort"]
station_keuze = tk.StringVar()
station_keuze.set(stations[0])
'''
Maak een dropdown-menu voor het selecteren van het station.
'''
station_keuzelijst = tk.OptionMenu(station_kiezen_venster, station_keuze, *stations)
station_keuzelijst.pack(pady=10)
'''
Knop om het berichtvenster te openen.
'''
berichten_knop = tk.Button(station_kiezen_venster,
                            text="berichten",
                            command=open_berichten_venster,
                            bg="#003082", fg="#ffcf36")
berichten_knop.pack(pady=10)

station_kiezen_venster.mainloop()
