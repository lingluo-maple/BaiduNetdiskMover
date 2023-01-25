# 关于

使用 [BaiduPcs-Go](https://github.com/qjfoidnh/BaiduPCS-Go) 下载文件，并移动至 Onedrive 文件自动同步文件夹内

# 使用

您需要安装并配置以下程序
- [BaiduPcs-Go](https://github.com/qjfoidnh/BaiduPCS-Go)
- [Onedrive](https://github.com/abraunegg/onedrive)
- [Python](https://www.python.org)

## 相关配置

### BaiduPcs-Go

您需要提前登录您的百度网盘账号
详细步骤请查看 https://github.com/qjfoidnh/BaiduPCS-Go#%E7%99%BB%E5%BD%95%E7%99%BE%E5%BA%A6%E5%B8%90%E5%8F%B7

### Onedrive

您需要提前安装好 Onedrive 并开启 `--monitor` `--upload-only` `--no-remote-delete` `enable-logging`, 如
```bash
onedrive --monitor --upload-only --no-remote-delete --enable-logging
```
同时检查用户是否有权限写入日志, 默认路径为 `/var/log/onedrive/${user}.onedrive.log
建议使用 `systemctl` 将 Onedrive 注册为服务
详细配置位于 https://github.com/abraunegg/onedrive/blob/master/docs/USAGE.md

### Python

Python 版本要求大于或等于 3.9
使用 `python -V` 来确认Python的版本
如果python版本开头为2，可以尝试改为 `python3 -V`, 同时下文的 python pip 也改为 python3 pip3
然后安装依赖
```bash
pip install loguru
```

### config.example.py

您需要在该文件中填写相关配置