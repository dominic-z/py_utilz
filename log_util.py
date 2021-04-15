import os
from datetime import datetime

from . import file_util


def __log_time_str():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def info(log_info: str, file_path: str):
    log_content = "[{time}] [INFO] {info}".format(time=__log_time_str(), info=log_info)
    __output(log_content, file_path=file_path)


def warn(log_info: str, file_path: str):
    log_content = "[{time}] [WARN] {info}".format(time=__log_time_str(), info=log_info)
    __output(log_content, file_path=file_path)


def error(log_info: str, file_path: str):
    log_content = "[{time}] [ERROR] {info}".format(time=__log_time_str(), info=log_info)
    __output(log_content, file_path=file_path)


def __output(log_content: str, file_path: str):
    if file_path is None:
        print(log_content)
    else:
        if os.path.exists(file_path):
            if os.path.isdir(file_path):
                raise IsADirectoryError("{} is a dir".format(file_path))
            os.remove(file_path)
        file_util.append_to_file(file_path=file_path, lines=[log_content], check_exist=False)
