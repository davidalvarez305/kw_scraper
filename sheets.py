from __future__ import print_function
import os
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import auth


def write_values(spreadsheet_id, range, values):
    try:
        credentials = auth.get_auth()
        service = build('sheets', 'v4', credentials=credentials)

        # Call the Sheets API
        sheet = service.spreadsheets()

        data = []
        for row in values:
            data.append(row.values())

        body = {
            "values": data
        }

        sheet.values().update(
            spreadsheetId=spreadsheet_id, range=range,
            valueInputOption="USER_ENTERED", body=body).execute()
    except HttpError as err:
        print(err)


def get_values(spreadsheet_id, range):
    try:
        credentials = auth.get_auth()
        service = build('sheets', 'v4', credentials=credentials)

        sheet = service.spreadsheets()

        result = sheet.values().get(spreadsheetId=spreadsheet_id,
                                    range=range).execute()
        values = result.get('values', [])

        if not values:
            return []
        
        data = []
        
        # Shape data matrix into list of dictionaries for easier working data structure
        data_headers = values[0]
        for row in values[1:]:
            val = {}
            for index, col in enumerate(row):
                val[data_headers[index]] = col
            
            data.append(val)

        return data
    except HttpError as err:
        print(err)
