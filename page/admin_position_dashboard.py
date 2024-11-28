import streamlit as st
import sqlite3
import pandas as pd

# Funktion, um alle Positionen aus der Datenbank abzurufen
def get_all_positions():
    try:
        conn = sqlite3.connect("./data/assessment.db")
        cursor = conn.cursor()

        # SQL-Abfrage, um alle Positionen zu erhalten
        cursor.execute("""
            SELECT p.id, p.name, p.description, ss.id AS skillset_id, qs.id AS questionset_id
            FROM position p
            LEFT JOIN skillset ss ON p.skillset = ss.id
            LEFT JOIN questionset qs ON p.questionset = qs.id
        """)
        positions = cursor.fetchall()
        print(positions)
        conn.close()
        
        if not positions:
            st.write("Keine Positionen in der Datenbank gefunden.")
            return pd.DataFrame()  # Leeres DataFrame zurückgeben, wenn keine Daten vorhanden sind

        # Konvertiere die Ergebnisse in ein pandas DataFrame
        df = pd.DataFrame(positions, columns=["Position ID", "Position Name", "Description", "Skillset ID", "Questionset ID"])

        # Entferne doppelte Einträge basierend auf der "Position ID"
        df = df.drop_duplicates(subset=["Position ID"])

        return df
        
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Positionen: {e}")
        return pd.DataFrame()  # Rückgabe eines leeren DataFrames bei Fehler

# Funktion, um detaillierte Informationen zu einer Position anzuzeigen
def display_position_details(position_id):
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()

    # Hole Details zu einer Position, z.B. welche Skills und Fragen zugeordnet sind
    cursor.execute("""
        SELECT s.name, ss.grade 
        FROM skill s
        JOIN skillset ss ON s.id = ss.skill
        WHERE ss.id = (SELECT skillset FROM position WHERE id = ?)
    """, (position_id,))
    skills = cursor.fetchall()

    cursor.execute("""
        SELECT q.description
        FROM question q
        JOIN questionset qs ON q.id = qs.question
        WHERE qs.id = (SELECT questionset FROM position WHERE id = ?)
    """, (position_id,))
    questions = cursor.fetchall()

    conn.close()

    # Zeige die Skills und Fragen der Position an
    st.write("### Skills für diese Position:")
    for skill in skills:
        st.write(f"- {skill[0]} (Level: {skill[1]})")
    
    st.write("### Fragen für diese Position:")
    for question in questions:
        st.write(f"- {question[0]}")

# Dashboard für Positionen
def display_dashboard():
    st.title("Positions Dashboard")

    # Hole alle Positionen
    df_positions = get_all_positions()

    # Zeige die Positionen in einer Tabelle
    st.write("### Alle Positionen:")
    st.dataframe(df_positions)

    # Filteroptionen für Positionen
    st.write("### Filter Optionen:")
    position_name_filter = st.text_input("Position Name", "", key="position_name_filter")
    
    # Filtere die Tabelle nach dem Namen der Position (falls eingegeben)
    if position_name_filter:
        df_positions = df_positions[df_positions['Position Name'].str.contains(position_name_filter, case=False)]

    st.write("### Gefilterte Positionen:")
    st.dataframe(df_positions)

    # Auswahl einer Position für Detailansicht
    selected_position_id = st.selectbox("Wählen Sie eine Position aus", df_positions["Position ID"].tolist())

    if selected_position_id:
        display_position_details(selected_position_id)

# Anwendung starten
def main():
    display_dashboard()

main()
