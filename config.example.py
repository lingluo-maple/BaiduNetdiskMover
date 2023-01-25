from pathlib import Path
from typing import Union, List, Dict, Optional

class Config:
    baiduPcsExec: Union[Path, str] = "BaiduPcs-Go"
    # BaiduPcs 可执行文件路径. (或文件在 $PATH 内)
    storageLimit: Union[int, float] = 5
    # 单位: G, 储存低于限制后停止下载
    delay: float = 30.0
    # 单位: 秒 下载完一个文件后停止的时间
    targetDirectory: Union[Path, str] = "/我的资源/..."
    # 需要下载的文件夹 (百度网盘)
    ondriveDirectory: Union[Path, str] = Path("/home/user/OneDrive")
    # 文件需要下载的地方(绝对路径)
    downloadDirectory: Union[Path, str] = Path("/home/user/Downloads/uid_username")
    # BaiduPcs-Go 保存目录 (与 BaiduPcs-Go config 里的 savedir 不同， 为 ${savedir}/{uid}_{username})
    
    def __init__(self) -> None:
        if not (
            isinstance(self.baiduPcsExec, (Path, str)) and
            isinstance(self.storageLimit, (int, float)) and
            isinstance(self.delay, float) and
            isinstance(self.targetDirectory, (Path, str)) and
            isinstance(self.ondriveDirectory, (Path, str)) and
            isinstance(self.downloadDirectory, (Path, str))
        ):
            raise TypeError("Please check your config file.")