import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
import altair as alt

# Google Sheets API setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials from Streamlit secrets
creds = Credentials.from_service_account_info(
    st.secrets["gcp_service_account"],  # Using the secret key stored in Streamlit secrets
    scopes=scope
)

client = gspread.authorize(creds)
sheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1uN214sOkU7cz53FxtdcNF_H0RfYIn0OZPKi_L8rvOkc/edit?usp=sharing").worksheet("Sheet1")

# Fetch the data
data = sheet.get_all_records()

# Convert the data to a pandas dataframe
df = pd.DataFrame(data)

# Ensure 'POC' and 'Lead Type' columns exist before creating the stacked bar chart
if 'POC' in df.columns and 'Lead Type' in df.columns:
    # Prepare data for stacked bar chart
    chart_data = df.groupby(['POC', 'Lead Type']).size().reset_index(name='Count')
    
    # Create an Altair stacked bar chart
    chart = alt.Chart(chart_data).mark_bar().encode(
        x='POC:N',  # Nominal (categorical) data on the X axis
        y='Count:Q',  # Quantitative data on the Y axis
        color='Lead Type:N'  # Stacked bars by 'Lead Type'
    ).properties(
        width=600,  # Width of the chart
        height=400  # Height of the chart
    ).interactive()  # Allow zooming/panning interaction

    # Render the chart in Streamlit
    st.altair_chart(chart)
else:
    st.error("Required columns 'POC' and 'Lead Type' not found in the dataset")


# Lead vs POC
# Under Progress/DNP vs POC
# sum Overdue
# count vs Lead Type