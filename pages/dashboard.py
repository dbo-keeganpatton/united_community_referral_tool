import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Dashboard")

st.set_page_config(
    layout="wide",
    page_title="Dashboard",
    page_icon="📊"
)

conn = st.connection("gsheets", type=GSheetsConnection)

# I really can't believe this works haha
# yes.. sql queries against a spreadsheet
client_count = conn.query(
    worksheet="Sheet1",
    sql="SELECT COUNT(DISTINCT Client) AS Clients FROM Sheet1"
)

open_referral_count = conn.query(
    worksheet='Sheet1',
    sql="SELECT ifnull(CAST(SUM(CASE WHEN Status='Open' THEN 1 END) AS INT64),0) AS open_refs from Sheet1"
)

closed_referral_count = conn.query(
    worksheet='Sheet1',
    sql="SELECT ifnull(CAST(SUM(CASE WHEN Status='Closed' THEN 1 END) AS INT64),0) AS closed_refs from Sheet1"
)

referral_bar_chart_data = conn.query(
    worksheet='Sheet1',
    sql="SELECT Status, CAST(COUNT(*) AS INT64) AS Referrals FROM Sheet1 GROUP BY 1 ORDER BY 2"
)



col1, col2, col3 = st.columns(3)
with col1:
    st.metric(
        label="Clients",
        value=client_count.iloc[0],
        border=True
    )

with col2:
    st.metric(
        label="Open Referrals",
        value=open_referral_count.iloc[0],
        border=True
    )

with col3:
    st.metric(
        label="Closed Referrals",
        value=closed_referral_count.iloc[0],
        border=True
    )

st.divider()

st.bar_chart(
    data=referral_bar_chart_data,
    x="Status",
    y="Referrals",
    x_label="",
    y_label=""
)



