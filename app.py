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
    "Enter Google Sheets URLs (one per line, leave blank to use default) if you capturing them manually", height=200
).splitlines()

# Predefined list of sheet URLs (used if text_area is empty)
default_sheet_urls = [
    "https://docs.google.com/spreadsheets/d/1d-CAKvSXeEdQqyn9gNo6ZRDYIQRUGqMjKADdszvS5xY/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1d2SWB7RgKeHat7uv53QwXYjsDOXtlEcDKL5CxI5JPI0/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1rSymM0BmCsEEoiyyiKfjr8Lsf_HTL394dpcvTR5v6L8/edit?gid=0#gid=0"
]

sheet_names = ["cea_budget", "cea_activities", "cea_ndicators"]  # descriptive names

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
        
        # Define columns to select from each sheet
        sheets_info = [
            {"url": sheet_urls[0], "columns": ["Intervention", "Activity", "Date", "Budget","Expenditure"], "name": sheet_names[0]},
            {"url": sheet_urls[1], "columns": ["Intervention", "Activity", "Date", "Venue", "Male", "Female", "Other"], "name": sheet_names[1]},
            {"url": sheet_urls[2], "columns": ["Intervention", "Activity", "Indicator", "Baseline", "Target", "Actual"], "name": sheet_names[2]},
        ]

        df_list = []

        for sheet in sheets_info:
            worksheet = client.open_by_url(sheet["url"]).sheet1
            data = pd.DataFrame(worksheet.get_all_records())
            
            # ✅ Debug: show actual columns in this sheet
            st.write(f"Columns in {sheet['name']} sheet:", data.columns.tolist())
            
            # Select only required columns
            data = data[sheet["columns"]]
            df_list.append(data)

        # Merge all sheets on 'Intervention'
        merged_df = df_list[0]
        for df in df_list[1:]:
            merged_df = merged_df.merge(df, on="Intervention", how="left")

        st.subheader("📂 Merged Data from Google Sheets")
        st.dataframe(merged_df.head())

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("⬆️ Please upload your Google Service Account JSON key file to continue.")