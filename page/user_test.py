# Imports
import streamlit as st
import sqlite3
import uuid

# Funktion um Fragen aus der Datenbank zu holen
def get_questions(job_id):
    # DB-Verbindung
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()

    # SQL-Abfrage, um die Fragen für die Position zu holen
    cursor.execute("""
        SELECT q.id, q.description
        FROM position p
        JOIN questionset qs ON p.questionset = qs.id
        JOIN question q ON qs.question = q.id
        WHERE p.id = ?
    """, (job_id,))
    
    
    questions = cursor.fetchall()
    
    return questions


# Funktion um die Antworten zu speichern
def save_answers(job_id, answers):
    # DB-Verbindung
    connection = sqlite3.connect("./data/assessment.db")
    cursor = connection.cursor()

    # Antworten speichern
    for question_id, answer in answers:
        cursor.execute("""
            INSERT INTO answer (description, question)
            VALUES (?, ?)
        """, (answer, question_id))
    
    connection.commit()


# Thank-You Page
def thank_you_page():
    st.write ("Vielen Dank für die Beantwortung der Fragen!")
    st.write ("Alle Antworten wurden erfolgreich gespeichert und wir melden uns schnellstmöglich bei Ihnen mit der Ergebnissen aus dem Fragenkatalog.")
    
    
# Hauptseite in Streamlit
def question_answer_page(job_id):
    # Lade Fragen aus der Datenbank
    questions = get_questions(job_id)
    
    if not questions:
        st.write("Es wurden keine Fragen gefunden.")
        return

    
    # Überprüfen, ob der Benutzer bereits Antworten abgegeben hat
    if 'answered' in st.session_state and st.session_state['answered']:
        st.session_state['show_thank_you'] = True
        return  # Stoppe die Verarbeitung, wenn bereits geantwortet wurde
    answers = []  # Hier speichern wir die Antworten
    
    
    with st.form("question_form"):
        # Frage durch Frage anzeigen
        for question_id, question_text in questions:
            response = st.text_input(f"Frage: {question_text}", key=str(question_id))
            answers.append((question_id, response))
        
        submit_button = st.form_submit_button("Antworten absenden")
    

    
    # Wenn der Submit-Button geklickt wurde
    if submit_button:
        if all(answer[1] for answer in answers):  # Prüfe, ob alle Fragen beantwortet wurden
            # Speichere die Antworten in der Datenbank
            save_answers(job_id, answers)
            # Markiere, dass der Benutzer bereits geantwortet hat
            st.session_state['answered'] = True
            st.session_state['show_thank_you'] = True
           # st.experimental_rerun()
          

        else:
            st.error("Bitte beantworten Sie alle Fragen.")



# Beispielhafte Anwendung

def main():
    # In einer echten Anwendung könnte der Job ID von einer vorherigen Seite kommen
    job_id = 4
    
    if job_id:
        # Zeige die Frage-Antwort-Seite für die gegebene Job-ID
        if 'show_thank_you' in st.session_state and st.session_state ['show_thank_you']:
            thank_you_page()
        else:                
            question_answer_page(job_id)


# Anwendung starten

main()
