import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up the credentials
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("payscale-analysis-457510-d460e45831c2.json", scope)

# Authenticate and initialize the client
client = gspread.authorize(creds)

# Create the Google Sheet
spreadsheet = client.create("Major Salary Survey")

# Optional: Share with your Gmail to view/edit from Google Sheets UI
spreadsheet.share('lipiv14@gmail.com', perm_type='user', role='writer')

# Select the first worksheet
worksheet = spreadsheet.sheet1

# Read the CSV file into a DataFrame
df = pd.read_csv('payscale_cleaned.csv')

# Add the column names as the first row
worksheet.append_row(df.columns.tolist())

# Convert DataFrame to a list of rows and insert
rows = df.values.tolist()
worksheet.append_rows(rows)

print("✅ Sheet created and data uploaded!")
