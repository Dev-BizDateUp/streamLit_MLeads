import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd

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

# Display the results
for _, row in df.iterrows():
    st.write(f"{row['first_name']} {row['last_name']} has a :{row['POC']}:")
