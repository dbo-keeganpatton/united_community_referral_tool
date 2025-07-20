import streamlit as st
from dotenv import load_dotenv
# This is basically just the site index
# following standard best practice for multi-page apps
# created in streamlit, doc below for ref when I forget in 6 months
# https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation
load_dotenv()


if not st.user.is_logged_in:
    # If the user has not gone through the OAuth flow, 
    # then only present the login template to prompt
    # authentication.
    pg = st.navigation(
        [st.Page("./pages/login.py", title="Login")]
    )
    pg.run()


elif st.user.is_logged_in and st.user.email=="keeganpatton@gmail.com":
    # When the user proceeds through the OAuth flow, check the email returned
    # in the cookie to see if it is part of our accepted list of users.
    # If it is not, then notify the user that they need to contact for 
    # access.
    st.write(f"{st.user.email} has not been verified for access. Please contact your administrator.")
    pg = st.navigation(
        [st.Page("./pages/login.py", title="Login")]
    )
    pg.run()


else:
    # If the user completes Oauth, and they are on the list of accepted users,
    # Grant access to the entire application.
    pg = st.navigation(
        [
            st.Page("./pages/service_map.py", title="Service Map"), 
            st.Page("./pages/referral_list.py", title="Spreadsheet"),
            st.Page("./pages/dashboard.py", title="Dashboard")
        ]
    )
    pg.run()
