import sqlite3
import csv
import requests
from bs4 import BeautifulSoup
import json

def generate_csv_from_select(statement, outputfile):

    connection = sqlite3.connect("./data/assessment.db")

    cursor = connection.cursor()

    cursor.execute(statement)
    with open(outputfile, "w") as csv_file:
        csv_writer = csv.writer(csv_file, delimiter="\t")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)

def export_to_csv(db_name, query, csv_file_name):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()

        # Execute the query to get the descriptions (or any other data)
        cursor.execute(query)

        # Fetch all results
        rows = cursor.fetchall()

        # Check if any results were returned
        if rows:
            # Open CSV file for writing
            with open(csv_file_name, mode='w', newline='', encoding='utf-8') as csv_file:
                writer = csv.writer(csv_file)

                # Write header (you can adjust the column names as needed)
                writer.writerow(['Description'])  # Modify this as per your column name

                # Write all data rows
                for row in rows:
                    writer.writerow([row[0]])  # Assuming the description is in the first column

            print(f"Data successfully exported to {csv_file_name}")
        else:
            print("No data found for the given query.")

    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    finally:
        # Close the database connection
        if conn:
            conn.close()

# Funktion zum Einfügen von CSV-Daten in die SQLite-Datenbank
def import_csv_to_position(csv_file_name, db_name):
    try:
        # Verbindung zur SQLite-Datenbank herstellen
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()


        # CSV-Datei öffnen und Daten einlesen
        with open(csv_file_name, mode='r', encoding='utf-8') as csv_file:
            reader = csv.reader(csv_file)
            
            # Überspringe die Kopfzeile, falls vorhanden
            next(reader)

            # Füge jede Beschreibung aus der CSV-Datei in die Tabelle ein
            for row in reader:
                description = row[7]
                name = row[1]
                cursor.execute("INSERT INTO position (description, name) VALUES (?,?)", (description,name,))

        # Änderungen speichern
        conn.commit()
        print(f"Daten aus {csv_file_name} wurden erfolgreich in die Datenbank eingefügt.")

    except sqlite3.Error as e:
        print(f"SQLite-Fehler: {e}")
    except Exception as e:
        print(f"Fehler: {e}")
    finally:
        # Verbindung zur Datenbank schließen
        if conn:
            conn.close()

# Funktion zum Abrufen und Extrahieren von Text aus einer Webseite
def get_page_text(url, output_filename):
    try:
        # Sendet eine GET-Anfrage an die URL
        response = requests.get(url)

        # Überprüfen, ob die Anfrage erfolgreich war (Statuscode 200)
        if response.status_code == 200:
            # Die Seite mit BeautifulSoup parsen
            soup = BeautifulSoup(response.text, 'html.parser')

            # Den gesamten Text aus der Seite extrahieren (nur den sichtbaren Text)
            page_text = soup.get_text()
            page_text = extract_subtext(page_text, "Ihr Profil:", "Wir bieten:")
            page_text = page_text.replace("\n"," ")


            # Speichern des extrahierten Textes in eine JSON-Datei
            data = {'url': url, 'text': page_text.strip()}

            # JSON-Daten in eine Datei schreiben
            with open(output_filename, 'w', encoding='utf-8') as json_file:
                json.dump(data, json_file, ensure_ascii=False, indent=4)

            print(f"Der Text von der Seite wurde erfolgreich in '{output_filename}' gespeichert.")
        else:
            print(f"Fehler: Die Anfrage an {url} war nicht erfolgreich (Statuscode: {response.status_code}).")

    except requests.exceptions.RequestException as e:
        print(f"Fehler bei der Anfrage: {e}")
    except Exception as e:
        print(f"Allgemeiner Fehler: {e}")

def extract_subtext(text, start_marker, end_marker):
    # Finde die Position des Startmarkes
    start_pos = text.find(start_marker)
    if start_pos == -1:
        return "Startmarker nicht gefunden"
    
    # Finde die Position des Endmarkes
    end_pos = text.find(end_marker, start_pos)
    if end_pos == -1:
        return "Endmarker nicht gefunden"
    
    # Extrahiere den Subtext zwischen dem Start- und Endmarker
    # Addiere die Länge des Startmarkers, um direkt nach ihm zu beginnen
    subtext = text[start_pos + len(start_marker):end_pos].strip()
    
    return subtext

def save_skills_to_db(job_name, file_path, db_path='data/assessment.db'):
    # Schritt 1: Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()


    # Schritt 3: Datei zeilenweise lesen und Skills in die Datenbank einfügen
    with open(file_path, 'r', encoding='utf-8') as file:
        skillset = []
        for line in file:
            # Entferne Leerzeichen und Zeilenumbrüche
            skill = line.strip()
            if skill:  # Nur nicht-leere Zeilen hinzufügen
                skillset.append(skill)
                cursor.execute('''
                    INSERT OR IGNORE INTO skill (name) VALUES (?)
                ''', (skill,))
                cursor.execute('''
                    SELECT id FROM skill WHERE name = (?)
                ''', (skill,))
                id = cursor.fetchone()
                cursor.execute('''
                    INSERT INTO skillset (id, skill) VALUES (?,?)
                ''', (skill,id))
        

    # Schritt 4: Änderungen speichern und Verbindung schließen
    conn.commit()
    conn.close()

url = "https://www.bwi.de/karriere/stellenangebote/job/lead-solution-architekt-german-mission-network-m-w-d-58389"
output_filename = "Profiltext.json"  # Name der JSON-Datei, in die der Text gespeichert wird

get_page_text(url, output_filename)

#import_csv_to_position("job_csv_test.csv","./data/assessment.db")
