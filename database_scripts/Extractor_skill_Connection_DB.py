#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import sqlite3
from bs4 import BeautifulSoup
import warnings
import spacy
from spacy.training.example import Example
import json
import random
import re

# Unterdrücke warnings
warnings.filterwarnings("ignore", category=UserWarning, module="spacy")
warnings.filterwarnings("ignore", category=FutureWarning, module="tensorflow")


# Funktion um Inhalte von Jobprfilen direkt auf der HTMl zu crawlen 
def get_job_offer_text(url):
    response = requests.get(url)
    html_content = response.text
    
    # Nutze BeautifulSoup um HTML zu parsen 
    soup = BeautifulSoup(html_content, "html.parser")
    
    # Crawle nach Jobtitel

    job_title = soup.find("div", class_="h1")
    if job_title:
        job_title_text = job_title.get_text(strip=True)
    else:
        job_title_text = ""

    # Crwale nach Profil Inhalten
    job_profile_div = soup.find("div", class_="jobBox jobProfile")
    if job_profile_div:
        job_profile = job_profile_div.get_text(separator="\n", strip=True)
    else:
        job_profile = ""
    
    return job_title_text, job_profile

# URL fur den Crawler
#job_offer_url = "https://www.bwi.de/karriere/stellenangebote/job/senior-it-systemingenieur-military-it-services-m-w-d-58317"

# Jobprfil Inhalt von der URL
#job_title, job_profile_text = get_job_offer_text(job_offer_url)

def clean_text(text):
    
    return text
# Liste von bekannten Skills (DB community)
skills_list = [
    "Active Directory", "Firewall", "Storage", "Backup", "Windows Server 2016", 
    "Netzwerk Topologie", "Powershell", "C#", "Automatisierung", "Scriptsprachen", "Programmiersprachen",
    "Python", "Java", "JavaScript", "AWS", "Azure", "Linux", "Django", "Flask"
]

# Funktion zur Extraktion von Skills
def extract_skills(job_profile_text):
    # Bereinigen des Textes
    cleaned_skilltext = clean_text(job_profile_text)

    # Liste der gefundenen Skills
    found_skills = []

    # Durchsuche den bereinigten Text nach Skills

    for skill in skills_list:

        # Anpassung der Expression zum Filtern auf Keywörter innerhalb Klammern
        pattern = r'[\(\[]?' + re.escape(skill) + r'[\)\]]?'
        if re.search(pattern, cleaned_skilltext, re.IGNORECASE):
            found_skills.append(skill)
    
    return found_skills


# Skills extrahieren
#extracted_skills = extract_skills(job_profile_text)

# Ausgabe der extrahierten Skills
#print("Extrahierte Skills:", extracted_skills)
#print ("Der Job-Titel ist:", job_title)


# Funktion für die Erstellung einer DB
def create_database():
    connection = sqlite3.connect()
    co = connection.curser()


    co.execute ()

    connection.commit()
    connection.close()

# Funktion zum Pflegen der DB
def insert_skills_into_db(job_title, skills):
    connection = sqlite3.connect('skills.db')
    co = connection.cursor()

    # Skills in die Datenbank pflegen 

    for skill in skills:
    
        co.execute(())
   

    connection.commit()
    connection.close()


# Erstelle DB falls fehlend

#create_database ()

# Pflege Daten in die Skill-DB
#insert_skills_into_db(job_title, extracted_skills)


