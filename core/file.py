import os
import warnings
import shutil
import pandas as pd
from datetime import datetime
from core.logger import logger
import openpyxl
from pathlib import Path
warnings.simplefilter(action='ignore', category=FutureWarning)

CODE_HOME = os.getcwd()

def load_file(debug: bool = False, file: str = None, sheet: str = None):
    backup_file(debug=debug, file=file)
    data = read_file(file=file, sheet=sheet)
    if debug and len(data)!=0:
        logger.success(f"Successfully loading accounts from {file}")
    return data

def save_file(_df=[], startcol:int=1, startrow:int=2, file: str = None, sheet: str = None):
    wb = openpyxl.load_workbook(file)
    ws=wb[sheet]
    for row in range(0, _df.shape[0]):
        for col in range(0, _df.shape[1]):
            ws.cell(row = startrow + row, column = startcol + col).value = _df.iat[row, col]
    wb.save(file)

def backup_file(debug: bool = False, file: str = None):
    file_name = Path(file).stem
    backup = f"{CODE_HOME}/backup/{file_name}_{datetime.today().strftime('%Y%m%d%H%M%S')}.xlsx"
    shutil.copy2(file, backup)
    if debug:
        logger.success(f"Successfully created backup file in {file}")

def read_file (file: str = None, sheet: str = None):
    df = pd.read_excel(file, sheet_name=sheet, skiprows=0)
    data = pd.DataFrame(df)
    return data
