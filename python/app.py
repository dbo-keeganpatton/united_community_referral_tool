import streamlit as st
from streamlit.components.v1 import iframe

url = 'https://cfn.maps.arcgis.com/apps/instant/lookup/index.html?appid=ffdde7dd21cd4fcabcdf33e01f95e747'
app_id = 'ffdde7dd21cd4fcabcdf33e01f95e747' 


st.write("Hello from Streamlit")

iframe(url, height=500)
