import streamlit as st
from api.gsheet_functions import GeezSheets 


st.title("Dashboard")

st.set_page_config(
    layout="wide",
    page_title="Dashboard",
    page_icon="📊"
)

conn = GeezSheets()

# I really can't believe this works haha
# yes.. sql queries against a spreadsheet
client_count = conn.query_google_sheet_with_sql(
    """
    SELECT 
    COUNT(DISTINCT concat('first_name', '-', 'last name')) AS Clients 
    FROM df
    """
)

open_referral_count = conn.query_google_sheet_with_sql(
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

closed_referral_count = conn.query_google_sheet_with_sql(
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

referral_bar_chart_data = conn.query_google_sheet_with_sql(
    """
    SELECT 
    status, 
    CAST(COUNT(*) AS INT64) AS Referrals 
    FROM df 
    GROUP BY 1 
    ORDER BY 2
    """
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
    x="status",
    y="Referrals",
    x_label="",
    y_label=""
)



