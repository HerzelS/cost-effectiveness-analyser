import gspread
import streamlit as st
import pandas as pd
import json
from oauth2client.service_account import ServiceAccountCredentials
import modules.ploting as ploting

st.title("📊 Cost-Effectiveness Analyzer (Google Sheets)")

# -------------------------
# 1. Function: Authorize Google Sheets client
# -------------------------
def authorize_gsheets(json_key_file):
    try:
        key_dict = json.load(json_key_file)
        scope = ["https://spreadsheets.google.com/feeds",
                 "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_dict(key_dict, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        st.error(f"❌ Authorization Error: {e}")
        return None

# -------------------------
# 2. Function: Load Google Sheets into DataFrames
# -------------------------
def load_sheets(client, sheet_urls):
    df_list = []
    for i, url in enumerate(sheet_urls):
        try:
            worksheet = client.open_by_url(url).sheet1  # default = first worksheet
            data = pd.DataFrame(worksheet.get_all_records())

            st.write(f"Columns in sheet {i+1}:", data.columns.tolist())
            st.write(f"### Preview of sheet {i+1}", data.head())

            df_list.append(data)
        except Exception as e:
            st.error(f"❌ Error loading sheet {i+1}: {e}")
    return df_list

# -------------------------
# Streamlit App Logic
# -------------------------
# Upload JSON key file
json_key_file = st.file_uploader("Upload JSON key file for Google Sheets API", type=["json"])

# Manual URL input
sheet_urls_input = st.text_area(
    "Enter Google Sheets URLs (one per line, leave blank to use default)", height=200
).splitlines()

# Default sheet URLs
default_sheet_urls = [
    "https://docs.google.com/spreadsheets/d/1d-CAKvSXeEdQqyn9gNo6ZRDYIQRUGqMjKADdszvS5xY/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1d-CAKvSXeEdQqyn9gNo6ZRDYIQRUGqMjKADdszvS5xY?resourcekey=#gid=853958344",
    "https://docs.google.com/spreadsheets/d/1d2SWB7RgKeHat7uv53QwXYjsDOXtlEcDKL5CxI5JPI0/edit?gid=0#gid=0",
    "https://docs.google.com/spreadsheets/d/1rSymM0BmCsEEoiyyiKfjr8Lsf_HTL394dpcvTR5v6L8/edit?gid=0#gid=0"
]

# Use manual or default URLs
sheet_urls = sheet_urls_input if any(sheet_urls_input) else default_sheet_urls

# Run if JSON key uploaded
if json_key_file:
    client = authorize_gsheets(json_key_file)
    if client:
        st.success("✅ Google Sheets API authorized successfully!")
        df_list = load_sheets(client, sheet_urls)

        if df_list:
            st.success(f"Loaded {len(df_list)} sheets into DataFrames.")

            # Example: access the first sheet (project budget)
            overall_budget = df_list[0]
            st.write("### Project Budget (first sheet):")
            st.dataframe(overall_budget.head())

            # Print to terminal (for debugging outside Streamlit)
            print(overall_budget.columns)
            ploting.plot_project_budget(overall_budget)

else:
    st.info("⬆️ Please upload your Google Service Account JSON key file to continue.")