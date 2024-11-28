import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Dieser Befehl muss der erste Streamlit-Befehl im Skript sein


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
        st.markdown("### Übersicht der Skillsets", unsafe_allow_html=True)
        
        # Hier kannst du die Daten ansprechender darstellen, z.B. mit Plotly oder als eine interaktive Tabelle
        fig = px.bar(df_skillsets, x="Skillset ID", y="Skillset Grade", color="Skill Name",
                     labels={"Skillset ID": "Skillset ID", "Skillset Grade": "Skillset Grade"},
                     title="Skillset Übersicht")
        st.plotly_chart(fig, use_container_width=True)  # Darstellung mit Plotly
        
        st.write("#### Skillsets im Detail")
        st.dataframe(df_skillsets)  # Streamlit bietet eine interaktive Darstellung als Tabelle an
        
        # Optional: Filter hinzufügen
        st.write("### Filter")
        skillset_filter = st.selectbox("Wählen Sie ein Skillset aus", df_skillsets["Skillset ID"].unique())
        
        filtered_df = df_skillsets[df_skillsets["Skillset ID"] == skillset_filter]
        st.write(f"#### Skills im Skillset {skillset_filter}")
        st.dataframe(filtered_df)
    else:
        st.warning("Es wurden keine Skillsets gefunden.")

# Streamlit App: Hauptlogik
def main():
    # Benutze Markdown und Streamlit-Widgets, um das Design zu verbessern
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #f0f4f8;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-weight: bold;
            border-radius: 5px;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        .stMarkdown {
            font-family: 'Roboto', sans-serif;
        }
        .stTitle {
            color: #2C3E50;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    st.title("Skillset Dashboard :bar_chart:")
    
    # Anzeige eines Hero Banners oder einer Willkommensnachricht
    st.markdown(
        """
        <div style="background-color:#4CAF50;padding:10px;color:white;font-size:20px;border-radius:10px;">
        Willkommen beim Skillset Dashboard! Hier können Sie alle Skillsets und zugehörigen Skills einsehen.
        </div>
        """, unsafe_allow_html=True)

    # Zeige Skillsets an
    display_skillsets()

main()
