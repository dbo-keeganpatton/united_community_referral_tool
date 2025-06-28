import streamlit as st

pg = st.navigation([st.Page("./pages/map.py"), st.Page("./pages/referral_list.py")])


pg.run()
