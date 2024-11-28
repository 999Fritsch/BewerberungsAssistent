import streamlit as st
import sqlite3
import uuid
from database_scripts import process_functions as pf

# Title of the app
st.title("Skillset Extractor")

# Default URL
default_url = "https://www.bwi.de/karriere/stellenangebote/job/senior-it-systemingenieur-military-it-services-m-w-d-58317"

# Input field for the URL with a default value
url = st.text_input("Enter the URL:", value=default_url)

# Extract the position ID from the URL
ID = pf.extract_skills(url)

# Button to trigger skill extraction
if st.button("Extract Skills") or pf.check_position_id_exists(ID):
    if url:
        # Get skills from the database using the extracted ID
        skill_list = pf.get_skills_by_position_id(ID)
        
        # Initialize session state for skill grades
        if 'skill_grades' not in st.session_state:
            st.session_state.skill_grades = {}

        # Display the extracted skills and allow user to choose grading
        st.write("Extracted Skills:")
        grading_options = ["Grundkentnisse", "Fortgeschritten", "Experte"]
        
        for skill in skill_list:
            skill_name = skill[0]
            if skill_name not in st.session_state.skill_grades:
                st.session_state.skill_grades[skill_name] = grading_options[0]
            st.session_state.skill_grades[skill_name] = st.segmented_control(f"Select grade for {skill_name}:", grading_options, key=skill_name, default=st.session_state.skill_grades[skill_name])
        
        # Button to save the graded skills into the database
        if st.button("Save Skills"):
            conn = sqlite3.connect("./data/assessment.db")
            cursor = conn.cursor()
            
            for skill_name, grade in st.session_state.skill_grades.items():
                cursor.execute("SELECT id FROM skill WHERE name = ?", (skill_name,))
                skill_id = cursor.fetchone()[0]
                cursor.execute("INSERT OR REPLACE INTO skillset (id, skill, grade) VALUES (?, ?, ?)", (ID, skill_id, grade))
            
            conn.commit()
            conn.close()
            st.success("Skills and grades have been saved to the database.")
    else:
        st.write("Please enter a valid URL.")
