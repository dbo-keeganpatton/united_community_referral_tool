from oauth2client.service_account import ServiceAccountCredentials
from streamlit.components.v1 import iframe
from dotenv import load_dotenv
import streamlit as st
import pandas as pd
import gspread
import json 
import os
load_dotenv()
st.set_page_config(
    layout="wide",
    page_title="Ministry Map",
    page_icon="🗺️"
)



#############################
#        Gsheet Auth        #
#############################
creds_json_str = os.getenv("GOOGLE_SHEETS_CREDS_JSON")
scope = "https://www.googleapis.com/auth/spreadsheets"

if creds_json_str is None:
    raise ValueError("GOOGLE_SHEETS_CREDS_JSON environment variable not set.")

creds_dict = json.loads(creds_json_str)
credentials = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope) 
url = 'https://cfn.maps.arcgis.com/apps/instant/lookup/index.html?appid=ffdde7dd21cd4fcabcdf33e01f95e747'


###############################
#  Title and Logo Alignment   #
###############################
title_col1, title_col2 = st.columns(spec=[5,1], gap=None)
with title_col1:
    st.title("Metro United Way")
    st.subheader("United Community Referral Tool")
with title_col2:
    st.image(image='./static/muw_logo.png', width=100)



with st.container(border=True):
    col1, col2 = st.columns(
        spec=2, 
        gap="medium"
    ) 
    ###############################
    #      ArcGIS Map Embed       #
    ###############################
    with col1:
        with st.container(border=True):
            iframe(
                url, 
                height=600, 
                width=600,
                scrolling=True
            )

    ###############################
    #        Core User CRUD       #
    ###############################
    with col2:
        st.text("Complete Form to log referral details")        
        name = st.text_input(label="Client", key="Client")
        address = st.text_input(label="Client Address", key="Address")
        ministry = st.text_input(label="Ministry Name", key="Ministry")
        

        if st.button(label="submit", key="map_submit_button"):

            if name and address and ministry:
               
                # All text fields must be filled in for submission to work
                # since st-gsheets has no true append method, a complete
                # DROP AND REPLACE must be done, this action creates two dataframes
                # one for the original state of the data in google sheets,
                # and one for the single row that will be added.
                # These are then concatenated through a standard pandas method,
                # and the sheet is repopulated with the new data.
                # Yep, this sucks...

                pre_insert_data = conn.read(worksheet="Sheet1")
                new_record = pd.DataFrame({
                    "Client": [name],
                    "Address": [address],
                    "Ministry": [ministry],
                    "Status": "Open"
                })

                add_row_to_data = pd.concat([pre_insert_data, new_record], ignore_index=True)
                conn.update(worksheet="Sheet1", data=add_row_to_data)


                st.success("Data Added, Check Referral Page for Updated entry.")
            else:
                st.warning("All fields must be completed to submit")
