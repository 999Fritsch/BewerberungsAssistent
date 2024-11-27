# Imports
import streamlit as st 
import sqlite3
import uuid


############################
# Functions
############################
# URL input Form
def url_Form():
    # position url question
    with st.form("position_url"):
   
        st.write("Bitte die URL der Stellenbeschreibung, für welche ein Skillset angelegt werden soll angeben")
        url = st.text_input('url', value="", max_chars=None, key=uuid.uuid4(), placeholder='https://www.bwi.de/karriere...', label_visibility="collapsed")
           
        st.form_submit_button("Weiter")  
        
    return url


# Skill grading form
def skillGrading_Foram(skill_list):
    #Variables
    graded_Skills = []
    
    # Process
    with st.form("skill_grading"):
    
        # define collums
        header = st.columns([1,2,3])
        header[0].subheader('Auswahl')
        header[1].subheader('Skill')
        header[2].subheader('Wertung')
    
        # create dynamic form
        for skill in skill_list:
            row = st.columns([1,2,3])
            responses = []
        
            select = row[0].checkbox('none', value=True, key=uuid.uuid4(), on_change=None, label_visibility="collapsed")
            responses.append(select)
        
            name = row[1].text_input('none', value=skill, key=uuid.uuid4(), placeholder=skill, label_visibility="collapsed")
            responses.append(name)
       
            grading = row[2].segmented_control('none', ['Grundlegend', 'Fortgeschritten', 'Experte'], selection_mode="single", key=uuid.uuid4(), label_visibility="collapsed")
            responses.append(grading)
       
            # remove deselected skills
            if responses[0]:
                graded_Skills.append(responses)
            
        st.form_submit_button("Abgeben")
        
    return graded_Skills


# Skill grading form
def questionFinalizing_Form(question_list):
    #Varaibles
    selected_questions = []
    
    # Process
    with st.form("question_finalizing"):
    
        # define collums
        header = st.columns([1,2])
        header[0].subheader('Auswahl')
        header[1].subheader('Frage')
    
        # create dynamic form
        for question in question_list:
            row = st.columns([1,2])
            responses = []
        
            select = row[0].checkbox('none', value=True, key=uuid.uuid4(), on_change=None, label_visibility="collapsed")
            responses.append(select)
        
            description = row[1].text_input('none', value=question, key=uuid.uuid4(), placeholder="Frage", label_visibility="collapsed")
            responses.append(description)
               
            # remove deselected skills
            if responses[0]:
                selected_questions.append(responses) 
                     
        st.form_submit_button("Abgeben")
        
    return selected_questions
    
############################
# Process
############################

# DB connection
# connection = sqlite3.connect(".data/assessment.db")
# cursor = connection.cursor()


# get URL from user
url = url_Form()
# scrape career portal
# create skill list
skill_list = []

if skill_list:
    skillGrading_Foram(skill_list)

# pass graded skills to db
# get_Questions for skillset

question_list = []

if question_list:
    questionFinalizing_Form(question_list)
# pass selected questions into db, link with corresponding skillset