import streamlit as st
import sqlite3
import pandas as pd

# Funktion, um Skillsets aus der Datenbank zu holen
def get_skillsets():
    try:
        conn = sqlite3.connect("./data/assessment.db")
        cursor = conn.cursor()

        # SQL-Abfrage, um alle Skillsets mit zugehörigen Skills zu bekommen
        cursor.execute("""
            SELECT ss.id AS skillset_id, ss.grade AS skillset_grade, s.name AS skill_name 
            FROM skillset ss
            JOIN skill s ON ss.skill = s.id
        """)
        
        skillsets = cursor.fetchall()
        conn.close()

        # Wenn keine Daten gefunden wurden
        if not skillsets:
            st.write("Keine Skillsets in der Datenbank gefunden.")
            return pd.DataFrame()  # Rückgabe eines leeren DataFrames

        # Konvertiere die Ergebnisse in ein pandas DataFrame
        df = pd.DataFrame(skillsets, columns=["Skillset ID", "Skillset Grade", "Skill Name"])
        return df
    
    except Exception as e:
        st.error(f"Fehler beim Abrufen der Skillsets: {e}")
        return pd.DataFrame()  # Rückgabe eines leeren DataFrames bei Fehler

# Funktion, um Skillsets anzuzeigen
def display_skillsets():
    # Hole Skillsets
    df_skillsets = get_skillsets()

    # Wenn es Skillsets gibt, zeige sie in einem DataFrame an
    if not df_skillsets.empty:
        st.write("### Übersicht der Skillsets")
        st.dataframe(df_skillsets)  # Zeigt die Tabelle in Streamlit an
        
        # Optional: Filter hinzufügen
        st.write("### Filter")
        skillset_filter = st.selectbox("Wählen Sie ein Skillset aus", df_skillsets["Skillset ID"].unique())
        
        filtered_df = df_skillsets[df_skillsets["Skillset ID"] == skillset_filter]
        st.write(f"### Skills im Skillset {skillset_filter}")
        st.dataframe(filtered_df)
    else:
        st.warning("Es wurden keine Skillsets gefunden.")

# Streamlit App: Hauptlogik
def main():
    st.title("Skillset Dashboard")

    # Zeige nur Skillsets an
    display_skillsets()

main()
