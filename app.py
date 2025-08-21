import gspread
import streamlit as st
import pandas as pd
from oauth2client.service_account import ServiceAccountCredentials


# Upload JSON key file for Google Sheets API
json_key_file = st.file_uploader("Upload JSON key file for Google Sheets API", type=["json"])
sheet_urls = st.text_area("Enter Google Sheets URLs (one per line)", height=200 )

if json_key_file and sheet_urls:
    scope = ["https://spreadsheets.google.com/feeds",
             "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_dict(json_key_file.read(), scope)
    client = gspread.authorize(creds)
    
    

    