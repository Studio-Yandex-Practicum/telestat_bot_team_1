import os

import gspread
from dotenv import load_dotenv

load_dotenv()

INFO = {
  "type": os.getenv('TYPE'),
  "project_id": os.getenv('PROJECT_ID'),
  "private_key_id": os.getenv('PRIVATE_KEY_ID'),
  "private_key": os.getenv('PRIVATE_KEY'),
  "client_email": os.getenv('CLIENT_EMAIL'),
  "client_id": os.getenv('CLIENT_ID'),
  "auth_uri": os.getenv('AUTH_URI'),
  "token_uri": os.getenv('TOKEN_URI'),
  "auth_provider_x509_cert_url": os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
  "client_x509_cert_url": os.getenv('CLIENT_X509_CERT_URL'),
  "universe_domain": os.getenv('UNIVERSE_DOMAIN')
}


class GoogleSheetsManager:
    def __init__(self, info):
        self.gc = gspread.service_account_from_dict(info)
        self.spreadsheet = self.gc.open('Тест таблица для проекта')

    def get_table_name(self):
        return self.spreadsheet.title

    def get_len_subscribers(self):
        sheet = self.spreadsheet.sheet1
        return len(sheet.get_all_records())


google_sheets_manager = GoogleSheetsManager(INFO)
