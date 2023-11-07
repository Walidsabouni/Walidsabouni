import random
from datetime import datetime
import csv


def main():
    bericht = input('Schrijf uw bericht (max 140 karakters): ')
    if len(bericht) > 140:
        raise ValueError('U mag maximaal 140 karakters gebruiken!')
    elif len(bericht) == 0:
        raise ValueError('Uw bericht mag niet leeg zijn!')

    naam = input('Vul uw naam in: ')
    if not naam.strip():
        naam = 'anoniem'

    datum = datetime.now()

    # Kies een willekeurig station uit een lijst van stations
    stations = open('stations.txt', 'r')
    ST_lines = stations.readlines()
    Gekozen_station = random.choice(ST_lines)

    # Sla gegevens op in een CSV-bestand
    with open('data2.csv', 'a', newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerow([bericht, datum, naam, Gekozen_station])


if __name__ == "__main__":
    main()