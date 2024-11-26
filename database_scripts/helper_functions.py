import sqlite3
import csv

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


#import_csv_to_position("job_csv_test.csv","./data/assessment.db")
