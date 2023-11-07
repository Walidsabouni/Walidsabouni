import csv
import psycopg2
from datetime import datetime


def main():
    beoordelaar_naam = input('Naam van de moderator: ')
    beoordelaar_email = input('E-mailadres van de moderator: ')
    # Lees gegevens uit het CSV-bestand
    with open('data2.csv', 'r', newline='') as data_file:
        reader = csv.reader(data_file)
        rows = list(reader)  # Lees alle rijen in het geheugen

    new_rows = []  # Hier zullen de gemodereerde berichten worden opgeslagen

    for row in rows:
        if not row:
            continue  # Sla lege rijen over

        if len(row) != 4:
            print("Ongeldige rij in CSV-bestand. Moet 4 waarden bevatten.")
            continue  # Sla ongeldige rijen over

        bericht, datum, naam, station = row
        # Simuleer moderatie (vervang dit met de echte moderatie)
        goedgekeurd = input(f"Moderatie voor bericht : {bericht} {datum}. van {naam} op {station}: (goed/afgekeurd): ").strip().lower()
        # beoordelaar_naam = input('Naam van de moderator: ')
        # beoordelaar_email = input('E-mailadres van de moderator: ')

        if goedgekeurd == "goed":
            goedgekeurd = True
        else:
            goedgekeurd = False

        # Voeg gegevens toe aan de PostgreSQL-database
        add_to_database(bericht, datum, naam, station, goedgekeurd, beoordelaar_naam, beoordelaar_email)

    # Overschrijf het CSV-bestand met de gemodereerde gegevens
    with open('data2.csv', 'w', newline='') as data_file:
        writer = csv.writer(data_file)
        writer.writerows(new_rows)

def add_to_database(bericht, datum, naam, station, goedgekeurd, beoordelaar_naam, beoordelaar_email):
    connection = psycopg2.connect(
        dbname="stationszuil",
        user="postgres",
        password="W@leed123",
        host="51.145.236.173"
    )
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO bericht (bericht_tekst, datum_en_tijd, naam_reiziger, station, goedgekeurd, naam_moderator, \"Emailadres_moderator\", tijd_en_datum_beoordeling) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (bericht, datum, naam, station, goedgekeurd, beoordelaar_naam, beoordelaar_email, datetime.now())
        )
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Fout bij toevoegen aan database: {str(e)}")
    finally:
        connection.close()

    # Leeg het CSV-bestand
    open('data2.csv', 'w').close()

if __name__ == "__main__":
    main()
