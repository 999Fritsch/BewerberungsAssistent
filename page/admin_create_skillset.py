import streamlit as st
import sqlite3
import uuid
from database_scripts import process_functions as pf

# Title of the app
st.title("Skillset Extractor")

# Default URL
#default_url = "https://www.bwi.de/karriere/stellenangebote/job/senior-it-systemingenieur-military-it-services-m-w-d-58317"

# Input field for the URL with a default value
url = st.text_input("Enter the URL:")

# Check if the URL and ID tuple is already in session state
if 'url_id_tuple' not in st.session_state:
    # Extract the position ID from the URL
    ID = pf.extract_skills(url)
    # Save the URL and ID tuple in session state
    st.session_state.url_id_tuple = (url, ID)
else:
    # Retrieve the ID from session state
    ID = st.session_state.url_id_tuple[1]

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
        st.button("Save Skills", on_click=lambda: pf.update_skillset(ID, st.session_state.skill_grades))
    else:
        st.write("Please enter a valid URL.")
