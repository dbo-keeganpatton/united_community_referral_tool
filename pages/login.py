import streamlit as st

st.header("This app is private.")
st.subheader("Please log in.")
st.button("Log in with Google", on_click=st.login)

