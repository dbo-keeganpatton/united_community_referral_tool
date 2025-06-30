import streamlit as st
from streamlit_gsheets import GSheetsConnection
st.set_page_config(
    layout="wide",
    page_title="Referrals",
    page_icon="📝"
)



st.title("Client Referral Spreadsheet")
st.write("You can update the 'Open' column to mark when referrals have been completed.")



#######################
# G-Sheets Connection #
#######################
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(
    # st.connection.read() is a passthrough
    # for pd.read_csv(), as such, args for 
    # that method will work here.
    worksheet="Sheet1",
    dtype={
        "Client Name": str,
        "Address": str,
        "Ministry": str,
        "Status": str
    },
    header=0
)



# Since streamlit_gsheets lacks proper Update functionality
# a copy of the current state of the source worksheet must be captured when
# the user opens the page.
# This is then saved as a copy and replaced by the alterd version
# when the user clicks the 'Save Changes button' 
if 'original_data' not in st.session_state:
    st.session_state.original_data = data.copy()

edited_data = st.data_editor(
    # Only the Boolean indicator for Completion of the referral
    # is editable. This is to mitigate potential data loss by
    # multiple users working with the app concurrently.
    data=data, 
    hide_index=True,
    disabled=("Client Name", "Ministry", "Address"),
    key="data_editor",
    
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
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
# to what was seein in the original data table when it was sourced from 
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
            disabled=not data_changed)

    with st.sidebar:
        if st.button("🔄 Refresh Data", use_container_width=True):
            # Refresh data from Google Sheets
            st.session_state.original_data = conn.read(worksheet="Sheet1", header=0)
            st.rerun()

        # Clearly this conditional is just an indicator for the user
        # that their actions have had an effect and that they
        # can process the changes if they so choose.
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
            conn.update(
                worksheet="Sheet1",
                data=edited_data
            )
            
            # Once we update the source data, it is recycled back to our UI.
            st.session_state.original_data = edited_data.copy()

        # emojis... Yay.    
        st.success("✅ Changes saved successfully!")
        st.rerun()
    except Exception as e:
        st.error(f"❌ Error saving changes: {str(e)}")
