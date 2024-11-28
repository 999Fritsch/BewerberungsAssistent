import streamlit as st 
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# load yaml config file
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

# Pre-hashing all plain text passwords once
stauth.Hasher.hash_passwords(config['credentials'])

# create authenticator widget
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# generate login screen
try:
    data = authenticator.login()
except Exception as e:
    st.error(e)

# define Admin Navigation
adm_pages = {
    "Dashboards": [
        st.Page("page/admin_dashboard.py", title="Home"),
        st.Page("page/admin_position_dashboard.py", title="Stellen"),
        st.Page("page/admin_skillset_dashboard.py", title="Skillsets"),
    ],
    "Forms": [
        st.Page("page/admin_create_skillset.py", title="Neues Skillset anlegen"),
    ],
}

# get first name of logged in User
try:
    usrName = st.session_state["name"]
    usrName = usrName.split(" ")
    usrName = usrName[0]
except:
    pass

# actions after login    
if st.session_state['authentication_status']:
    authenticator.logout('logout', 'sidebar')

    # show admin navigation
    if usrName == 'admin':
        pg = st.navigation(adm_pages)
        pg.run() 
    
    # show user navigation   
    else:
        pg = st.navigation([st.Page("page/user_test.py", title='Test')])
        pg.run()  
 
elif st.session_state['authentication_status'] is False:
    st.error('Username/password is incorrect')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter your username and password')
    
    # hide navigation post-logout
    pg = st.navigation([st.Page('page/empty.py')], position='hidden')
    pg.run() 