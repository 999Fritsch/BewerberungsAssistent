import streamlit as st
import sqlite3
import pandas as pd

# DB-Verbindung
# Funktion, um Bewerberdaten abzurufen
def get_applicant_data(position_filter=None, score_min=None, score_max=None):
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()

    position_id = 1  # Beispiel-Position-ID, für die du die Applications abrufen möchtest
    query= """
    SELECT DISTINCT a.id AS application_id, a.applicant, a.score
    FROM position p
    JOIN skillset s ON p.skillset = s.id
    JOIN questionset qs ON p.questionset = qs.id
    JOIN question q ON qs.question = q.id
    JOIN answer an ON q.id = an.question
    JOIN application a ON an.application = a.id
    WHERE p.id = p.id
    """
    

    filters = []
    if position_filter:
        query += " AND p.name = ?"
        filters.append(position_filter)
    #if score_min is not None:
    #    query += " AND a.score >= ?"
    #    filters.append(score_min)
    #if score_max is not None:
    #    query += " AND a.score <= ?"
    #    filters.append(score_max)
    
    cursor.execute(query, tuple(filters))
    results = cursor.fetchall()
    conn.close()

    # Erstelle DataFrame aus den Ergebnissen
    df = pd.DataFrame(results, columns=["Applicant", "Position", "Score"])
    
    return df


# Funktion, um Positionsdaten abzurufen
def get_positions():
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM position")
    positions = [row[0] for row in cursor.fetchall()]
    conn.close()
    return positions

# Funktion, um die Antworten der Bewerber abzurufen
def get_answers(applicant_id):
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()

    query = """
    SELECT q.description, a.score
    FROM answer a
    JOIN question q ON a.question = q.id
    JOIN questionset qs ON a.question = qs.question
    JOIN application ap ON a.application = ap.id
    WHERE ap.id = ?
    """
    
    cursor.execute(query, (int(applicant_id),))
    results = cursor.fetchall()
    conn.close()

    # Erstelle DataFrame aus den Antworten
    df = pd.DataFrame(results, columns=["Question", "Score"])
    return df

# Streamlit-Dashboard zur Anzeige der Bewerber
def display_dashboard():
    st.title("Interaktives Bewerber Dashboard")

    # Dropdown-Menü für Positionen
    positions = get_positions()
    position_filter = st.selectbox("Wählen Sie eine Position", ["Alle"] + positions, index=0)
    
    # Filter für Score
    score_min = st.slider("Min. Score", 0, 100, 0)
    score_max = st.slider("Max. Score", 0, 100, 100)
    
    # Zeige gefilterte Bewerberdaten
    st.write("Gefilterte Bewerber:")
    if position_filter != "Alle":
        df = get_applicant_data(position_filter=position_filter, score_min=score_min, score_max=score_max)
    else:
        df = get_applicant_data(score_min=score_min, score_max=score_max)
    
    if df.empty:
        st.write("Es wurden keine Daten gefunden.")
    else:
        st.dataframe(df)
        st.write("Bitte wählen Sie einen Bewerber aus, um die Antworten zu sehen.")
        
        # Dropdown-Menü für Bewerber
        selected_applicant = st.selectbox("Wählen Sie einen Bewerber", df["Applicant"].unique())

        if selected_applicant:
            # Hole die Antworten des ausgewählten Bewerbers
            applicant_id = df[df["Applicant"] == selected_applicant].index[0] + 1
            answers_df = get_answers(applicant_id)
            if not answers_df.empty:
                st.write(f"Antworten von {selected_applicant}:")
                st.dataframe(answers_df)
            else:
                st.write("Keine Antworten gefunden.")

# Anwendung starten
def main():
    display_dashboard()
    
main()