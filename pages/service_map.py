from streamlit.components.v1 import iframe
from api.gsheet_functions import GoogleSheets 
import streamlit as st
import pandas as pd
from datetime import datetime
st.set_page_config(
    layout="wide",
    page_title="Ministry Map",
    page_icon="🗺️"
)



conn = GoogleSheets()
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
        
        # Data Schema Inputs
        student_first_name = st.text_input(label="Student First Name", key="student_first_name")
        student_last_name = st.text_input(label="Student Last Name", key="student_last_name")
        hoh_first_name = st.text_input(label="Head of Houshold First Name", key="hoh_first_name")
        hoh_last_name = st.text_input(label="Head of Household Last Name", key="hoh_last_name")
        hoh_address = st.text_input(label="Head of Household Address", key="hoh_address")
        hoh_zip = st.text_input(label="Head of Household Zip Code", key="hoh_zip")
        hoh_email = st.text_input(label="Head of Household Email", key="hoh_email")
        hoh_cell_number = st.text_input(label="Head of Household Cell", key="hoh_cell_number")
        frsyc_name = st.text_input(label="FRSYC Name", key="frsyc_name")
        school = st.text_input(label="School", key="school")
        ministry = st.text_input(label="Ministry Name", key="ministry")
        description_of_support_needed = st.text_input(label="Description of Support Needed", key="description")
        referral_create_date = str(datetime.now().replace(microsecond=0)) 
        notes = st.text_input(label="Notes", key="notes")


        if st.button(label="submit", key="map_submit_button"):

            if (
                # these fields must be complete for the form submission to work
                # Notes is optional, since that will primarily be used by 
                # ministry volunteers.
                student_first_name and student_last_name and hoh_first_name and 
                hoh_last_name and hoh_address and hoh_zip and
                hoh_email and hoh_cell_number and frsyc_name and 
                school and ministry and description_of_support_needed and 
                referral_create_date
            ):
               
                # All text fields must be filled in for submission to work
                # I am doing a complete DROP AND REPLACE here...
                # this action creates two dataframes, one for the original state 
                # of the data in google sheets and one for the single row that 
                # will be added. These are then concatenated through a standard 
                # pandas method, and the sheet is repopulated with the new data.
                # Yep, this sucks... I'll find a better way at some point.

                pre_insert_data = conn.Going_To_Get_Data()
            
                new_record = pd.DataFrame({
                    "student_first_name"               : [student_first_name], 
                    "student_last_name"                : [student_last_name],
                    "hoh_first_name"                   : [hoh_first_name],
                    "hoh_last_name"                    : [hoh_last_name],
                    "hoh_address"                      : [hoh_address],
                    "hoh_zip"                          : [hoh_zip],
                    "hoh_email"                        : [hoh_email],
                    "hoh_cell_number"                  : [hoh_cell_number],
                    "frsyc_name"                       : [frsyc_name],
                    "school"                           : [school],
                    "ministry"                         : [ministry],
                    "description_of_support_needed"    : [description_of_support_needed],
                    "status"                           : "Open",
                    "referral_create_date"             : [referral_create_date], 
                    "notes"                            : ""
                })

                add_row_to_data = pd.concat([pre_insert_data, new_record], ignore_index=True)
                conn.Update_Data(add_row_to_data)

                st.success("Data Added, Check Referral Page for Updated entry.")
            else:
                st.warning("All fields must be completed to submit")
