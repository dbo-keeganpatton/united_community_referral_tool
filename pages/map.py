import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection
from streamlit.components.v1 import iframe

st.set_page_config(
    layout="wide",
    page_title="Ministry Map Tool",
    page_icon="🗺️"
)


conn = st.connection("gsheets", GSheetsConnection)
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



###############################
#           SideBar           #
###############################
with st.sidebar:

    st.page_link(
        page='./pages/referral_list.py',
        label="Referral List"
    )


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
        
        name = st.text_input(label="Client Name", key="client_name")
        address = st.text_input(label="Client Address", key="client_address")
        ministry = st.text_input(label="Ministry Name", key="ministry_name")
        

        if st.button(label="submit", key="map_submit_button"):

            if name and address and ministry:
                

                pre_insert_data = conn.read(worksheet="Sheet1")
                new_record = pd.DataFrame({
                    "client_name": [name],
                    "address": [address],
                    "ministry": [ministry],
                    "open": [True]
                })

                add_row_to_data = pd.concat([pre_insert_data, new_record], ignore_index=True)
                conn.update(worksheet="Sheet1", data=add_row_to_data)


                st.success("Data Added, Check Referral Page for Updated entry.")
            else:
                st.warning("All fields must be completed to submit")


