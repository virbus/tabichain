import os
import warnings
import shutil
import pandas as pd
from datetime import datetime
from core.logger import logger
import openpyxl
from pathlib import Path
from openpyxl.utils.dataframe import dataframe_to_rows
warnings.simplefilter(action='ignore', category=FutureWarning)

CODE_HOME = os.getcwd()
_BACKED_UP_FILES = set()

def load_file(debug: bool = False, file: str = None, sheet: str = None):
    backup_file(debug=debug, file=file)
    data = read_file(file=file, sheet=sheet)
    if debug and len(data)!=0:
        logger.success(f"Successfully loading accounts from {file}")
    return data

def save_file(_df=[], startcol:int=1, startrow:int=2, file: str = None, sheet: str = None):
    wb = openpyxl.load_workbook(file)
    ws=wb[sheet]
    for r_idx, row in enumerate(dataframe_to_rows(_df, index=False, header=False), start=startrow):
        for c_idx, value in enumerate(row, start=startcol):
            ws.cell(row=r_idx, column=c_idx).value = value
    wb.save(file)

def backup_file(debug: bool = False, file: str = None):
    global _BACKED_UP_FILES
    if file in _BACKED_UP_FILES:
        return
    file_name = Path(file).stem
    backup_dir = f"{CODE_HOME}/backup"
    os.makedirs(backup_dir, exist_ok=True)
    backup = f"{backup_dir}/{file_name}_{datetime.today().strftime('%Y%m%d%H%M%S')}.xlsx"
    shutil.copy2(file, backup)
    if debug:
        logger.success(f"Successfully created backup file in {file}")
    _BACKED_UP_FILES.add(file)

def read_file (file: str = None, sheet: str = None):
    df = pd.read_excel(file, sheet_name=sheet, skiprows=0)
    data = pd.DataFrame(df)
    for col in ["Faucet", "Send"]:
        if col in data.columns:
            data[col] = pd.to_numeric(data[col], errors='coerce').fillna(0).astype(int)
    return data
