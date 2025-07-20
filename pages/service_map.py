from streamlit.components.v1 import iframe
from api.gsheet_functions import GoogleSheets 
import streamlit as st
import pandas as pd
import time
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

with st.sidebar:
    st.button("Log Out", on_click=st.logout)

# This stages the page for a reload flow after the 
# @st.dialog modal decorator has been confirmed for
# referral form submission.
# This value will be updated to non-zero by confirming that data
# will be added to our database. After this action, the
# counter and all session state vars will be reset, triggering
# a full app reload.
if 'form_key' not in st.session_state:
    st.session_state.form_key = 0


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
        student_first_name = st.text_input(label="Student First Name", key=f"student_first_name_{st.session_state.form_key}")
        student_last_name = st.text_input(label="Student Last Name", key=f"student_last_name_{st.session_state.form_key}")
        hoh_first_name = st.text_input(label="Head of Houshold First Name", key=f"hoh_first_name_{st.session_state.form_key}")
        hoh_last_name = st.text_input(label="Head of Household Last Name", key=f"hoh_last_name_{st.session_state.form_key}")
        hoh_address = st.text_input(label="Head of Household Address", key=f"hoh_address_{st.session_state.form_key}")
        hoh_zip = st.text_input(label="Head of Household Zip Code", key=f"hoh_zip_{st.session_state.form_key}")
        hoh_email = st.text_input(label="Head of Household Email", key=f"hoh_email_{st.session_state.form_key}")
        hoh_cell_number = st.text_input(label="Head of Household Cell", key=f"hoh_cell_number_{st.session_state.form_key}")
        frsyc_name = st.text_input(label="FRSYC Name", key=f"frsyc_name_{st.session_state.form_key}")
        school = st.text_input(label="School", key=f"school_{st.session_state.form_key}")
        ministry = st.text_input(label="Ministry Name", key=f"ministry_{st.session_state.form_key}")
        description_of_support_needed = st.text_input(label=f"Description of Support Needed", key=f"description_{st.session_state.form_key}")
        referral_create_date = str(datetime.now().replace(microsecond=0)) 
        notes = st.text_input(label="Notes", key=f"notes_{st.session_state.form_key}")
    
        
        ##################################
        #     Modal Confirmation Flow    #
        ##################################
        @st.dialog("Submit Referral to Database?")
        def submit_referral_confirmation():
            st.write("Are you sure you want to submit this referral?")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Yes, Submit", type="primary"):
                    
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
                        "notes"                            : [notes] if notes else ""
                    })

                    add_row_to_data = pd.concat([pre_insert_data, new_record], ignore_index=True)
                    conn.Update_Data(add_row_to_data)
                    
                    # Once the user selects "confirm" to add their form inputs to 
                    # the app's backend, the app will pause for 1 second before
                    # resetting all session state vars, and triggering
                    # full app reload.
                    st.success("Data Added, Check Referral Page for Updated entry.")
                    time.sleep(1)
                    st.session_state.form_key += 1
                    st.rerun()
            

            with col2:
                if st.button("Cancel"):
                    st.rerun()

        # Main submit button logic
        if st.button(label="Submit", key="map_submit_button", type="primary"):
            if (
                # these fields must be complete for the form submission to work
                student_first_name and student_last_name and hoh_first_name and 
                hoh_last_name and hoh_address and hoh_zip and
                hoh_email and hoh_cell_number and frsyc_name and 
                school and ministry and description_of_support_needed and 
                referral_create_date
            ):
                
                submit_referral_confirmation()
            else:
                st.warning("All fields must be completed to submit")
