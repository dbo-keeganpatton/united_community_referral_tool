import streamlit as st
import pandas as pd

st.title("referrals")

data = pd.read_csv("./static/placeholder_data.csv")

st.data_editor(
    # Only the Boolean indicator for Completion of the referral
    # is editable. This is to mitigate potential data loss by
    # multiple users working with the app concurrently.
    data=data, 
    hide_index=True,
    disabled=("client_name", "ministry", "address")
)
