from api.gsheet_functions import GoogleSheets 
import streamlit as st
st.set_page_config(
    layout="wide",
    page_title="Referrals",
    page_icon="📝"
)


title_col1, title_col2 = st.columns(spec=[5,1], gap=None)
with title_col1:
    st.title("Metro United Way")
    st.subheader("Client Referral Spreadsheet")
with title_col2:
    st.image(image='./static/muw_logo.png', width=100)

st.write("You can update the 'Open' column to mark when referrals have been completed.")

with st.sidebar:
    st.button("Log Out", on_click=st.logout)


#######################
# G-Sheets Connection #
#######################
conn = GoogleSheets()
data = conn.Going_To_Get_Data() 


# a copy of the current state of the source worksheet must be 
# captured when the user opens the page. This is then saved 
# as a copy and replaced by the altered version when the user 
# clicks the 'Save Changes button' 
if 'original_data' not in st.session_state:
    st.session_state.original_data = data.copy()

edited_data = st.data_editor(
    # pass the 'disabled=' arg with a set of col names
    # to set cols that should not be edited from the app.
    data=data, 
    hide_index=True,
    key="data_editor",

    # Set Data Validation here for Drop Downs
    column_config={
        "status": st.column_config.SelectboxColumn(
            "status",
            help="Select status from dropdown",
            width="small",
            options=[
                "Open",
                "Closed",
                "Emailed",
                "Called",
                "Blocked"
            ],
            required=True,
        )
    }
)

# This variable is just used to compare data that currently exists on the page
# to what was seen in the original data table when it was sourced from 
# Google Sheets.
data_changed = not edited_data.equals(st.session_state.original_data) 


#################################
#   CRUD Buttons on Sidebar     #
#################################
with st.container():
    # These buttons are placed in the sidebar because I am 
    # to stupid to figure out how to align them above the data table
    # while still maintaining state accurately.
    with st.sidebar:
        save_button = st.button(
            "💾 Save Changes",
            use_container_width=True,
            disabled=not data_changed
        )

    with st.sidebar:
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Refresh data from Google Sheets
            st.cache_data.clear() 
            st.rerun()


        if data_changed:
            st.warning("⚠️ You have unsaved changes")
        else:
            st.success("✅ Data is up to date")


###############################################
#      Apply Changes to Source Data Logic     #
###############################################
if save_button:
    try:
        with st.spinner("Saving changes to Google Sheets..."):
            # Runs a complete DROP and REPLACE operation essentially on the
            # source workbook.I really hate this..... Like I REALLY hate it.
            conn.Update_Data(edited_data)
            # Once we update the source data, it is recycled back to our UI.
            st.session_state.original_data = edited_data.copy()

        # emojis... Yay.    
        st.success("✅ Changes saved successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error saving changes: {str(e)}")
