import streamlit as st
from streamlit_gsheets import GSheetsConnection
st.set_page_config(
    layout="wide",
    page_title="Referral Spreadsheet",
    page_icon="📝"
)

st.title("referrals")

#######################
# G-Sheets Connection #
#######################
conn = st.connection("gsheets", type=GSheetsConnection)
data = conn.read(
    # st.connection.read() is a passthrough
    # for pd.read_csv(), as such, args for 
    # that method will work here.
    worksheet="Sheet1", 
    header=0
)


st.data_editor(
    # Only the Boolean indicator for Completion of the referral
    # is editable. This is to mitigate potential data loss by
    # multiple users working with the app concurrently.
    data=data, 
    hide_index=True,
    disabled=("client_name", "ministry", "address")
)
