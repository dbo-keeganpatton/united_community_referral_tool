import streamlit as st
from dotenv import load_dotenv
# This is basically just the site index
# following standard best practice for multi-page apps
# created in streamlit, doc below for ref when I forget in 6 months
# https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation

load_dotenv()
pg = st.navigation(
    [
        st.Page("./pages/login.py", title="Login"),
        st.Page("./pages/service_map.py", title="Service Map"), 
        st.Page("./pages/referral_list.py", title="Spreadsheet"),
        st.Page("./pages/dashboard.py", title="Dashboard")
    ]
)

pg.run()
