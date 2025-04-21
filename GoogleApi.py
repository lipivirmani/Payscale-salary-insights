import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


# Authenticate Google Sheets API
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("payscale-analysis-457510-d460e45831c2.json", scope)
    client = gspread.authorize(creds)
    return client


# Create the Google Sheet and Share
def create_google_sheet(client, sheet_name="Salary Survey"):
    try:
        spreadsheet = client.create(sheet_name)
        spreadsheet.share('lipiv14@gmail.com', perm_type='user', role='writer')
        return spreadsheet
    except Exception as e:
        print(f"Error creating Google Sheet: {e}")
        return None


# Enhanced Analysis
def enhanced_analysis(df):
    df["Spread"] = df["Mid-Career Pay"] - df["Early Career Pay"]
    df["Growth (%)"] = (df["Spread"] / df["Early Career Pay"]) * 100

    top_growth = df[["Major", "Early Career Pay", "Mid-Career Pay", "Spread", "Growth (%)"]].sort_values(by="Spread",
                                                                                                         ascending=False)
    top_growth_summary = top_growth.head(5)

    # Add top 5 growth to a new sheet or summary
    return top_growth_summary


# Upload Data to Google Sheets
def upload_data_to_sheet(spreadsheet, df):
    try:
        worksheet = spreadsheet.sheet1
        worksheet.append_row(df.columns.tolist())  # Column headers

        # Convert DataFrame to list of rows
        rows = df.values.tolist()
        worksheet.append_rows(rows)

        # Optionally, add the enhanced analysis as a summary in another sheet
        summary_sheet = spreadsheet.add_worksheet(title="Top Growth Summary", rows="10", cols="5")
        top_growth_summary = enhanced_analysis(df)
        summary_sheet.append_row(top_growth_summary.columns.tolist())
        summary_rows = top_growth_summary.values.tolist()
        summary_sheet.append_rows(summary_rows)

        print(f"✅ Data from CSV uploaded and enhanced analysis added to Google Sheets!")
    except Exception as e:
        print(f"Error uploading data: {e}")


if __name__ == "__main__":
    client = authenticate_google_sheets()
    if client:
        spreadsheet = create_google_sheet(client)
        if spreadsheet:
            # Read the CSV file into DataFrame
            df = pd.read_csv('payscale_cleaned.csv')

            # Upload original data and enhanced analysis
            upload_data_to_sheet(spreadsheet, df)

