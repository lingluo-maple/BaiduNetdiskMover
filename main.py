import re
import os
import time
import subprocess
import shutil

from loguru import logger
from pathlib import Path
from typing import List, Optional, Union

from error import *
from config import Config

config = Config()
todoDir = []
files = []

def run(command: str, path: Optional[str] = None):
    if not path:
        path = ''
    else:
        path = f'"{path}"'
    cmd = f'{config.baiduPcsExec} {command} {path}'.strip()
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf8", shell=True)
    return (result.returncode, result.stdout, result.stderr)

def check_code(code: int, err):
    if code != 0:
        raise ReturnCodeError(f"program return none zero code: {code}. \n{err}")

def check_login() -> bool:
    code, out, err = run("who")
    if code != 0:
        raise ReturnCodeError(f"program return {code} when check login satus. \n{err}")
    if (uid:= re.search(r"uid: (\d+)", out)):
        uid = uid.group(1)
    else:
        raise Exception(f"Failed to find uid")
    if uid == 0:
        raise LoginRequired("You should login baiduPcs before use this script. "
                            r"See https://github.com/qjfoidnh/BaiduPCS-Go#%E7%99%BB%E5%BD%95%E7%99%BE%E5%BA%A6%E5%B8%90%E5%8F%B7")
    else:
        return True

def check_target_exist(file: Union[Path, str]):
    """
        file (Union[Path, str]): File or direcroty.
    """
    code, out, err = run("ls", str(file))
    check_code(code, err)
    if "文件或目录不存在" in out:
        logger.error(f"Failed to ls {file}")
        raise FileOrDirectoryNotFound()
    return out
    
def check_storage_enough() -> bool:
    _, _, free = shutil.disk_usage("/")
    if (free:= round(free/1024/1024/1024, 2)) < config.storageLimit:
        logger.warning(f"Available storage is less than {config.storageLimit} GB.\n Current: {free} GB.")
        time.sleep(60)
        return False
    return True
    
def get_downloaded_list() -> List[str]:
    if not (file:= Path("downloaded.txt")).exists():
        file.touch()
    with open(file, "r") as f:
        return [i for i in f.read().split("\n") if i != ""]
    
def get_file_list(directory: Union[Path, str]):
    """get file list by ls command."""
    out = check_target_exist(directory).split("\n")
    datetime_regex = r"\d+-\d+-\d+ \d+:\d+:\d+"
    dir_regex = re.compile(rf"^ *\d+ *- *{datetime_regex} *(.+)\/ *$")
    file_regex = re.compile(rf"^ *\d+ *\d+\.?\d*[KMGT]?B *{datetime_regex} *(.+?) *$")
    for line in out:
        line = line.strip()
        if (match := re.search(dir_regex, line)):
            todoDir.append(os.path.join(directory, match.group(1)))
        elif (match := re.search(file_regex, line)):
            files.append(os.path.join(directory, match.group(1)))

def main():
    logger.info("Check login status.")
    check_login()
    logger.info("Fetch file list.")
    get_file_list(config.targetDirectory)
    while todoDir:
        directory = todoDir.pop()
        get_file_list(directory)
    downloaded = get_downloaded_list()
    logger.info(f"Try to download {len(files)} file(s). {len(downloaded)} are already downloaded.")
    for file in files:
        if file in downloaded:
            continue
        while not check_storage_enough():
            ...
        download(file)
         
    
def download(file: Union[Path, str]):
    """下载文件并移至 Onedrive 文件夹
    
    Args:
        file (Union[Path, str]): {path}/{filename}
    
    Variable:
        f: 百度网盘上的文件路径 {targetDirectory}/{path}/{filename}.
        filename: 文件名
        src: 文件下载到的路径，无目录结构
        dst: Onedrive路径，含目录结构
    """
    f = os.path.join(config.targetDirectory, file)
    filename = Path(file).name
    logger.info(f"Downloading file: {f}")
    # 将 stdout 输出至终端(进度条)，捕获 stderr
    r = subprocess.run(f'{config.baiduPcsExec} d "{f}"', shell=True, stderr=subprocess.PIPE, encoding="utf8")
    check_code(r.returncode, r.stderr)
    src = Path(config.downloadDirectory) / Path(filename)
    dst = Path(f.replace(str(config.targetDirectory), str(config.ondriveDirectory)))
    os.makedirs(dst.parent, exist_ok=True)
    shutil.move(src, dst)
    logger.success(f"Move {filename} from {src} to {dst}")
    
    
def test():
    assert check_login() == True
    assert check_storage_enough() == True
    get_file_list(config.targetDirectory)
    while todoDir:
        directory = todoDir.pop()
        get_file_list(directory)
    print("\n".join(files))
    
if __name__ == "__main__":
    main()
    # test()