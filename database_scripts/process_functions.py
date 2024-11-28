import sqlite3
from database_scripts import Extractor_skill_Connection_DB as ext


def create_position(name):
    """
    Fügt eine neue Position in die SQLite-Datenbank ein, falls der Name noch nicht existiert.

    Args:
        name (str): Der Name der Position, die hinzugefügt werden soll.

    Raises:
        sqlite3.Error: Wenn ein Fehler bei der Verbindung zur Datenbank oder bei der Ausführung der SQL-Befehle auftritt.

    Example:
        create_position("Software Engineer")
    """
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
    """
    Extracts skills from a job offer URL and stores them in an SQLite database.
    This function connects to an SQLite database, extracts job title and skills from the given URL,
    and inserts the skills into the database. It also associates the skills with a skillset and 
    inserts the job position with the associated skillset.
    Args:
        url (str): The URL of the job offer.
    Returns:
        int: The ID of the inserted job position, or None if the insertion failed.
    """
    # Verbindung zur SQLite-Datenbank herstellen (oder erstellen, falls sie nicht existiert)
    conn = sqlite3.connect("./data/assessment.db")
    cursor = conn.cursor()    

    job_title, job_profile_text = ext.get_job_offer_text(url)
    skills = ext.extract_skills(job_profile_text)

    print(skills)

    cursor.execute("SELECT max(id) FROM skillset")
    current_skillset_id = cursor.fetchone()[0]
    if current_skillset_id is not None:
        next_skillset_id = current_skillset_id + 1
    else:
        next_skillset_id = 1

    

    for skill in skills:
        cursor.execute("INSERT OR IGNORE INTO skill (name) VALUES (?)", (skill,))
        conn.commit()
        cursor.execute("SELECT id FROM skill WHERE name = ?", (skill,))
        skill_id = cursor.fetchone()[0]
        cursor.execute("INSERT INTO skillset (id,skill) VALUES (?,?)", (next_skillset_id,skill_id))
        conn.commit()
    
    cursor.execute("INSERT INTO position (name,skillset) VALUES (?,?)" "RETURNING id", (job_title,next_skillset_id))
    row = cursor.fetchone()
    (inserted_id, ) = row if row else None
    conn.commit()

    return inserted_id

#extract_skills("https://www.bwi.de/karriere/stellenangebote/job/senior-it-systemingenieur-military-it-services-m-w-d-58317")
#extract_skills("https://www.bwi.de/karriere/stellenangebote/job/senior-it-architekt-ddi-dns-dhcp-und-ip-adressmanagement-m-w-d-58398")
    