import os

import pandas as pd
from fpdf import FPDF

from services.spreadsheet_manager import \
    google_sheets_manager


class FormatManager:

    def __init__(self):
        self.folder_path = 'reports'

    def _get_file_path(self, format_file):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)

        filename = f'{google_sheets_manager.get_table_name()}{format_file}'
        return os.path.join(self.folder_path, filename)

    def message(self):
        return (
            f'Группа в телеграм: {google_sheets_manager.get_table_name()}\n'
            f'Количество подписчиков текущее: '
            f'{google_sheets_manager.get_len_subscribers()}'
        )

    def _csv_or_excel(self, format_report):
        df = pd.DataFrame(
            {
                'Группа в телеграм': [google_sheets_manager.get_table_name()],
                'Количество подписчиков текущее': [
                    google_sheets_manager.get_len_subscribers()]
            }
        )
        file_path = self._get_file_path(format_report)
        if format_report == '.csv':
            df.to_csv(file_path, index=False)
        if format_report == '.xlsx':
            df.to_excel(file_path, index=False)
        return file_path

    def _pdf(self, format_report):
        pdf = FPDF()
        pdf.add_page()
        pdf.add_font('DejaVu', '', 'DejaVuSans-Bold.ttf', uni=True)
        pdf.set_font('DejaVu', '', 12)
        pdf.cell(
            200,
            10,
            f'Группа в телеграм: {google_sheets_manager.get_table_name()}',
            0,
            1
        )

        pdf.cell(
            200,
            10,
            (f'Количество подписчиков текущее: '
             f'{google_sheets_manager.get_len_subscribers()}'),
            0,
            1
        )
        file_path = self._get_file_path(format_report)
        pdf.output(file_path)
        return file_path

    def format_selection(self, format_report):
        if format_report == '.pdf':
            return self._pdf(format_report)
        else:
            return self._csv_or_excel(format_report)


format_manager = FormatManager()
