import os

from dotenv import load_dotenv
from google.oauth2.service_account import Credentials
from googleapiclient import discovery
import asyncio
from parser import parsing


SCOPES = [
         'https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive',
]

load_dotenv()
EMAIL_USER = os.environ['EMAIL']

INFO = {
    'type':  os.environ['TYPE'],
    'project_id':  os.environ['PROJECT_ID'],
    'private_key_id':  os.environ['PRIVATE_KEY_ID'],
    'private_key':  os.environ['PRIVATE_KEY'].replace(r'\n', '\n'),
    'client_email':  os.environ['CLIENT_EMAIL'],
    'client_id':  os.environ['CLIENT_ID'],
    'auth_uri':  os.environ['AUTH_URI'],
    'token_uri':  os.environ['TOKEN_URI'],
    'auth_provider_x509_cert_url':  os.environ['AUTH_PROVIDER_X509_CERT_URL'],
    'client_x509_cert_url':  os.environ['CLIENT_X509_CERT_URL']
}

CREDENTIALS = Credentials.from_service_account_info(
    info=INFO, scopes=SCOPES)

SHEETS_SERVICE = discovery.build('sheets', 'v4', credentials=CREDENTIALS)
DRIVE_SERVICE = discovery.build('drive', 'v3', credentials=CREDENTIALS)


def auth():
    credentials = Credentials.from_service_account_info(
                  info=INFO, scopes=SCOPES)
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service, credentials


def create_spreadsheet(service):
    spreadsheet_body = {
        'properties': {
            'title': 'Аналитика пользователей чата',
            'locale': 'ru_RU'
        },
        'sheets': [{
            'properties': {
                'sheetType': 'GRID',
                'sheetId': 0,
                'title': 'Аналитика чата',
                'gridProperties': {
                    'rowCount': 100,
                    'columnCount': 100
                }
             }
         }]
    }
    request = service.spreadsheets().create(body=spreadsheet_body)
    response = request.execute()
    spreadsheet_id = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
    return spreadsheet_id


def set_user_permissions(spreadsheet_id, credentials):
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': EMAIL_USER}
    drive_service = DRIVE_SERVICE
    drive_service.permissions().create(
        fileId=spreadsheet_id,
        body=permissions_body,
        fields='id'
    ).execute()


def spreadsheet_update_values(service, spreadsheetId):
#    table_values = [
#        ['first_name', 'user.id', 'username', 'joined_date',
#         'phone_number', 'last_online_date'],]

    request_body = {
        'majorDimension': 'ROWS',
        'values': asyncio.run(parsing())
    } 
    request = service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        range='A1:F20',
        valueInputOption='USER_ENTERED',
        body=request_body
    )
    request.execute()
    return 'Документ обновлён'


service, credentials = auth()
spreadsheetId = create_spreadsheet(service)
set_user_permissions(spreadsheetId, credentials)
spreadsheet_update_values(service, spreadsheetId)
