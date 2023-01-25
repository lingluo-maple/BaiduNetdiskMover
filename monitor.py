import os
import re
import time
import html

from pathlib import Path

from loguru import logger

onedriveDirectory = Path("/home/luohua/OneDrive")
logFile = Path("/var/log/onedrive/luohua.onedrive.log")
if not logFile.exists():
    logFile.touch()
def auto_delete():
    logger.info(f"开始自动删除已上传的文件")
    while True:
        content = file.readline().replace("\n", "")
        if not content:
            time.sleep(5)
            continue
        if "modified file" in content:
            continue
        if "invalid name" in content:
            if filename := re.search(r"invalid name .*: (\.\/.*)", content):
                filename = onedriveDirectory / Path(filename.group(1))
                if filename.exists():
                    logger.info(f"Try to rename file {filename}")
                    rename(filename)
        searchResult = re.search(r"Uploading new file (.*) ... done.", content)
        if not searchResult:
            continue

        fileName = searchResult.group(1)
        logger.success(f"File: {fileName} uploaded")
        fileName = onedriveDirectory / fileName
        if Path(fileName).exists():
            os.remove(fileName)
            logger.success(f"File: {fileName} deleted")


def escape(filename: str):
    return html.unescape(
        filename.strip()
        .replace("/", "／")
        .replace("\\", "＼")
        .replace("?", "？")
        .replace("*", "＊")
        .replace('"', "”")
        .replace("<", "《")
        .replace(">", "》")
        .replace(":", "：")
        .replace("|", "｜")
    )


def rename(file: Path):
    # ~ " # % & * : <  > ? / \ { | }
    filename = file.name
    file.rename(Path(file.parent) / Path(escape(filename)))


if __name__ == "__main__":
    file = open(logFile)
    try:
        auto_delete()
    finally:
        file.close()
