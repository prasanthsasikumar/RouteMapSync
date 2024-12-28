import pandas as pd
from google.oauth2.credentials import Credentials
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def update_sheet_values(csv_file_path, spreadsheet_id, range_name, credentials_path):
    """
    Update a Google Sheet with data from a CSV file.
    
    Args:
        csv_file_path (str): Path to the CSV file
        spreadsheet_id (str): The ID of the Google Sheet (from the URL)
        range_name (str): The range to update (e.g., 'Itinerary!A1')
        credentials_path (str): Path to the service account credentials JSON file
    """
    try:
        # Read CSV file
        df = pd.read_csv(csv_file_path)
        
        # Convert DataFrame to values list (including headers)
        values = [df.columns.values.tolist()] + df.values.tolist()
        
        # Set up credentials and service
        credentials = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=['https://www.googleapis.com/auth/spreadsheets']
        )
        
        service = build('sheets', 'v4', credentials=credentials)
        
        # Create the body for the update request
        body = {
            'values': values
        }
        
        # Execute the update request
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Cells updated: {result.get('updatedCells')}")
        return result, service, df
        
    except HttpError as error:
        print(f"An error occurred: {error}")
        return error, None, None

def clear_sheet_formatting(service, spreadsheet_id, sheet_id):
    """
    Clear all formatting in the sheet.

    Args:
        service: Google Sheets API service instance
        spreadsheet_id (str): The ID of the Google Sheet
        sheet_id (int): The ID of the sheet to clear formatting
    """
    try:
        clear_format_request = {
            "requests": [
                {
                    "updateCells": {
                        "range": {
                            "sheetId": sheet_id
                        },
                        "fields": "userEnteredFormat"
                    }
                }
            ]
        }

        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=clear_format_request
        ).execute()

        print("All formatting cleared successfully")
    except HttpError as error:
        print(f"An error occurred while clearing formatting: {error}")

def format_sheet_header(service, spreadsheet_id, sheet_id, num_columns, df):
    """
    Apply formatting to the header row and specific rows in the sheet.

    Args:
        service: Google Sheets API service instance
        spreadsheet_id (str): The ID of the Google Sheet
        sheet_id (int): The ID of the sheet to format
        num_columns (int): Number of columns in the sheet
        df (DataFrame): DataFrame used to calculate row indices
    """
    try:
        format_request = {
            "requests": [
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": 0,
                            "endRowIndex": 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": num_columns
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": "CENTER",
                                "textFormat": {
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat(horizontalAlignment,textFormat)"
                    }
                },
                {
                    "repeatCell": {
                        "range": {
                            "sheetId": sheet_id,
                            "startRowIndex": len(df.index),
                            "endRowIndex": len(df.index) + 1,
                            "startColumnIndex": 0,
                            "endColumnIndex": num_columns
                        },
                        "cell": {
                            "userEnteredFormat": {
                                "horizontalAlignment": "CENTER",
                                "textFormat": {
                                    "bold": True
                                }
                            }
                        },
                        "fields": "userEnteredFormat(horizontalAlignment,textFormat)"
                    }
                }
            ]
        }

        # Execute the formatting request
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body=format_request
        ).execute()

        print("Header formatting applied successfully")
    except HttpError as error:
        print(f"An error occurred during formatting: {error}")

if __name__ == "__main__":
    # Example usage
    CSV_FILE_PATH = 'Route_Details.csv'
    SPREADSHEET_ID = '1NncveTRud-Pg7B6T_GoIQK9zg79URhgLA9nE6Hxq2NA'
    RANGE_NAME = 'Itinerary!A1'
    CREDENTIALS_PATH = 'calcium-aria-388302-9284f6252ea7.json'

    # Update sheet values
    result, service, df = update_sheet_values(CSV_FILE_PATH, SPREADSHEET_ID, RANGE_NAME, CREDENTIALS_PATH)

    if service and df is not None:
        # Get the sheet ID and column count
        sheet_metadata = service.spreadsheets().get(spreadsheetId=SPREADSHEET_ID).execute()
        sheet_id = None
        sheet_name = RANGE_NAME.split('!')[0]
        for sheet in sheet_metadata.get('sheets', ''):
            if sheet['properties']['title'] == sheet_name:
                sheet_id = sheet['properties']['sheetId']
                break

        num_columns = len(df.columns)

        # Clear existing formatting
        clear_sheet_formatting(service, SPREADSHEET_ID, sheet_id)

        # Format the sheet header
        format_sheet_header(service, SPREADSHEET_ID, sheet_id, num_columns, df)
