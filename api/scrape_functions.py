# This is not used now, this is for later
# If needed
import streamlit as st
import re

text_input = st.text_area("Paste your text below:")

# Define the fields you want to extract
fields = [
    "Name",
    "Phone",
    "Zipcodes Served",
    "Office Address",
    "Food Access",
    "Financial Assistance"
]

def extract_fields(text):
    extracted = {}
    for field in fields:
        # Look for "Field<TAB or SPACE>Value" pattern
        pattern = rf"{re.escape(field)}[ \t]+(.+?)(?=\n\S|$)"
        match = re.search(pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            extracted[field] = match.group(1).strip()
        else:
            extracted[field] = ""
    return extracted

# Only parse if there’s text
if text_input:
    result = extract_fields(text_input)

    st.markdown("### Extracted Information")
    for key, value in result.items():
        st.text_input(label=key, value=value, key=key)


