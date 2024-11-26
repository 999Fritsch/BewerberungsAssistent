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

export_to_csv("./data/assessment.db","SELECT description FROM position WHERE name = 'testposition'", "test2.csv")