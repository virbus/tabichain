import sys
import re

from loguru import logger

def logging_setup():
    format_info =  "<green>{time:YYYY-MM-DD HH:mm:ss.SS}</green> [ <blue>{level: <7}</blue> ] <cyan>{line: <3}</cyan>: <level>{message}</level>"
    format_error = "{time:HH:mm:ss.SS} | {level} | <cyan>{line}</cyan> | <level>{message}</level>"
    file_path = r"logs/"
    logger.remove()
    logger.add(file_path + "logger.log", colorize=False, format=clean_brackets(format_error))
    logger.add(sys.stdout, colorize=True, format=format_info, level="INFO")

def clean_brackets(raw_str):
    clean_text = re.sub(brackets_regex, '', raw_str)
    return clean_text

brackets_regex = re.compile(r'<.*?>')
logging_setup()
