# Imports
import streamlit as st 
import sqlite3 
import uuid

"""
# DB connection
connection = sqlite3.connect(".data/assessment.db")
cursor = connection.cursor()

############################
# Process
############################
def get_questions(applicationID):
    questions = cursor.execute("")
    
    
# evaluate answers
def evaluate_answers(answers):
    score = 0  
    return score
    

# push score to db
def push_answers(applicantID, ql):
    cursor.execute("")
    
""" 
  
def check_Status(applicationID):
    # check if answers already exist
    answer_content = cursor.execute("")
    
    # return bool
    if answer_content:
        return True
    else:
        return False
   

# create Form
def user_Test(ql):
    rp = [] # Variable, für ausagbe der Nutzerantworten
    
    with st.form('user_Test'):
    
        for question in ql:
            st.write(question)
            response = st.text_area("Antwort", key=uuid.uuid4(), help=None, on_change=None, args=None, kwargs=None, placeholder=None, disabled=False, label_visibility="collapsed")
            rp.append(response)
        
        st.form_submit_button('Abgeben')
        
    return rp

    
############################
# Process
############################
# BewerbungsID Auslesen
try:
    applicationID = st.session_state["name"]
    applicationID = usrName.split(" ")
    applicationID = usrName[0]
except:
    pass

# get question catalogue from DB
# ql = get_questions(applicationID):

# check if user already completed the Test
if False: #replace False with check_Status(applicationID)
    st.write('Kein offener Test verfügbar')
    
else:
    ql = ["Welcher Tag ist heute?", "Wie ist dein name?", "wie viel Uhr ist es"] # Placeholder Fragenkatalog
    answers = user_Test(ql)
      
# push questions to DB 
# push_answers(applicationID, answers) 

# run question eval
# evaluate_answers(applicationID)     