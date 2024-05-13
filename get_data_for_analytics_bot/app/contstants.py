import datetime as dt
from pathlib import Path


BASE_DIR = Path(__file__).parent
DATETIME_FORMAT = '%Y-%m-%d_%H-%M-%S'
results_dir = BASE_DIR / 'results'
results_dir.mkdir(exist_ok=True)
now = dt.datetime.now()
now_formatted = now.strftime(DATETIME_FORMAT)
file_name = f'{now_formatted}.csv'
file_path = results_dir/file_name
