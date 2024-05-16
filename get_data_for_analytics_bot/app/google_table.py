import os
# import asyncio
from aiogoogle import Aiogoogle
from aiogoogle.sessions.aiohttp_session import AiohttpSession
from aiogoogle.auth.creds import ServiceAccountCreds
from dotenv import load_dotenv

from app.bot_parser import parsing


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

CREDENTIALS = ServiceAccountCreds(scopes=SCOPES, **INFO)

app = Aiogoogle(service_account_creds=CREDENTIALS,
                session_factory=AiohttpSession)


async def create_spreadsheet() -> str:
    service = await app.discover('sheets', 'v4')
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
    response = await app.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    print('https://docs.google.com/spreadsheets/d/' + spreadsheet_id)
    return spreadsheet_id


async def set_user_permissions(spreadsheet_id: str,
                               ) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': EMAIL_USER}
    service = await app.discover('drive', 'v3')
    await app.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheet_update_values(
        spreadsheet_id: str,
) -> None:
    service = await app.discover('sheets', 'v4')
    update_body = {
        'majorDimension': 'ROWS',
        'values': await parsing()
    }
    await app.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )


async def collect_analytics():
    spreadsheetid = await create_spreadsheet()
    await set_user_permissions(spreadsheetid)
    await spreadsheet_update_values(spreadsheetid)


# asyncio.run(collect_analytics())
