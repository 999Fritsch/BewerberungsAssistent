import sqlite3
import Extractor_skill_Connection_DB


def create_position(name):
    # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls sie nicht existiert)
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()


    # Überprüfen, ob der Name bereits in der Tabelle existiert
    cursor.execute('SELECT COUNT(*) FROM position WHERE name = ?', (name,))
    if cursor.fetchone()[0] == 0:
        # Wenn der Name noch nicht vorhanden ist, füge ihn ein
        cursor.execute('INSERT INTO position (name) VALUES (?)', (name,))
        conn.commit()
        print(f'Eintrag mit dem Namen "{name}" wurde hinzugefügt.')
    else:
        print(f'Der Name "{name}" existiert bereits in der Tabelle.')

    # Verbindung schließen
    conn.close()

def extract_skills(url):
    # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls sie nicht existiert)
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()    

    job_title, job_profile_text = Extractor_skill_Connection_DB.get_job_offer_text(url)
    skills = Extractor_skill_Connection_DB.extract_skills(job_profile_text)

    cursor.execute("SELECT max(id) FROM skillset")

    if cursor.fetchone()[0] is not None:
        next_skillset_id = cursor.fetchone()[0] + 1
    else:
        next_skillset_id = 0

    for skill in skills:
        cursor.execute("INSERT OR IGNORE INTO skill (name) VALUES (?)", (skill,))
        cursor.execute("SELECT id FROM skill WHERE name = ?", (skill,))
        skill_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO skillset (id,skill) VALUES (?,?)", (next_skillset_id,skill_id))
    
    cursor.execute("INSERT INTO position (name,skillset) VALUES (?,?)", (job_title,next_skillset_id))
    cursor.commit()

extract_skills("https://www.bwi.de/karriere/stellenangebote/job/senior-it-architekt-netzwerk-security-m-w-d-58392")
    