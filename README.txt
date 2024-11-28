WebUI

# Requierments
pip install streamlit
pip install streamlit_Authenticator

# WebUI starten
streamlit run main.py

# Anmeldung
admin password -> Zugriff auf formular zu Skill erstellung, (Dashboards)
user password -> Zugriff zu dem durchzuführenden Test

# Identifikation des angemeldeten users 
Schlüssel der Bewerbung das nutzers in der YAML Datei unter first name angeben
Das Program liest die ID nach der Anmeldung aus, und legt die Information im Session Speicher ab.

# Weitere hinweise
Anforderungen zur einbindung in den Prozess sind an den entsprechenden Stellen gekennzeichnet
    .Page/user_test.py
    .Page/admin_create_Skillset.py

Der Admin account darf in der YAML  Datei nicht verändert werden. Die Darstellung, der für Admins relevanten seiten, ist sont nicht mehr möglich
weitere Nutzer können nach belieben eingefügt werden

