import streamlit as st

# This is basically just the site index
# following standard best practice for multi-page apps
# created in streamlit, doc below for ref when I forget in 6 months
# https://docs.streamlit.io/develop/concepts/multipage-apps/page-and-navigation

pg = st.navigation(
    [
        st.Page("./pages/map.py"), 
        st.Page("./pages/referral_list.py"),
        st.Page("./pages/dashboard.py")
    ]
)

pg.run()
