import streamlit as st
from api.gsheet_functions import GoogleSheets 

title_col1, title_col2 = st.columns(spec=[5,1], gap=None)
with title_col1:
    st.title("Metro United Way")
    st.subheader("Dashboard")
with title_col2:
    st.image(image='./static/muw_logo.png', width=100)

with st.sidebar:
    st.button("Log Out", on_click=st.logout)

st.set_page_config(
    layout="wide",
    page_title="Dashboard",
    page_icon="📊"
)

conn = GoogleSheets()

# I really can't believe this works haha
# yes.. sql queries against a spreadsheet
client_count = conn.Visualize_Data(
    """
    SELECT 
    COUNT(DISTINCT concat(student_first_name, '-', student_last_name)) AS Clients 
    FROM df
    """
)

open_referral_count = conn.Visualize_Data(
    """
    SELECT 
    IFNULL(
       CAST(
          SUM(CASE WHEN status='Open' THEN 1 END) 
          AS INT64
       ), 0
    ) AS open_refs 
    FROM df
    """
)

closed_referral_count = conn.Visualize_Data(
   """
   SELECT 
   IFNULL(
      CAST(
         SUM(CASE WHEN status='Closed' THEN 1 END) 
         AS INT64
       )
       ,0
   ) AS closed_refs 
   from df
   """
)

referral_bar_chart_data = conn.Visualize_Data(
    """
    SELECT 
    status,
    count(*) AS referrals
    FROM df
    GROUP BY status
    ORDER BY referrals DESC
    """
)



col1, col2, col3, col4 = st.columns(4)
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

with col4:
    st.metric(
        label="Avg Days to Close",
        value=10,
        border=True
    )

st.divider()

t1, t2 = st.columns(2)

with t1:
    st.bar_chart(
        data=referral_bar_chart_data,
        x="status",
        y="referrals",
        x_label="",
        y_label=""
    )

with t2:
    st.bar_chart(
        data=referral_bar_chart_data,
        x="status",
        y="referrals",
        x_label="",
        y_label=""
    )

