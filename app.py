import gspread
import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials

st.title("📊 Cost-Effectiveness Analyzer (Google Sheets)")

# Upload JSON key file
json_key_file = st.file_uploader("Upload JSON key file for Google Sheets API", type=["json"])

# Optional: user can input URLs manually
sheet_urls_input = st.text_area(
    "Enter Google Sheets URLs (one per line, leave blank to use default)", height=200
).splitlines()

# Predefined list of sheet URLs (used if text_area is empty)
default_sheet_urls = [
    "https://docs.google.com/spreadsheets/d/1d-CAKvSXeEdQqyn9gNo6ZRDYIQRUGqMjKADdszvS5xY/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1d-CAKvSXeEdQqyn9gNo6ZRDYIQRUGqMjKADdszvS5xY?resourcekey=#gid=853958344",
    "https://docs.google.com/spreadsheets/d/1d2SWB7RgKeHat7uv53QwXYjsDOXtlEcDKL5CxI5JPI0/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1rSymM0BmCsEEoiyyiKfjr8Lsf_HTL394dpcvTR5v6L8/edit?gid=0#gid=0"
]

# Use manual URLs if provided, else default
sheet_urls = sheet_urls_input if any(sheet_urls_input) else default_sheet_urls

if json_key_file:
    try:
        # Parse JSON from uploaded file
        key_dict = json.load(json_key_file)
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
        client = gspread.authorize(creds)
        st.success("✅ Google Sheets API authorized successfully!")

        df_list = []

        for i, url in enumerate(sheet_urls):
            worksheet = client.open_by_url(url).sheet1  # default = first worksheet
            data = pd.DataFrame(worksheet.get_all_records())

            st.write(f"Columns in sheet {i+1}:", data.columns.tolist())
            st.write(f"### Preview of sheet {i+1}", data.head())

            df_list.append(data)

        # ✅ Each sheet's DataFrame is now in df_list
        st.success(f"Loaded {len(df_list)} sheets into DataFrames.")

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Please upload your Google Service Account JSON key file to continue.")
