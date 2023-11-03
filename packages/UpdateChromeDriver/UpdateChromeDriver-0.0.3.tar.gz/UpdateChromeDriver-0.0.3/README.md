升级到最新版：

```shell script
pip install UpdateChromeDriver --index-url https://pypi.org/simple/ -U
```

目前本库仅在Windows上测试通过，Mac不敢确认，欢迎使用Mac的童鞋测试。



核心用法示例：

```python
import time

from UpdateChromeDriver import *

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging', 'enable-automation'])
browser = getChromeBrowser(options)
browser.get("https://www.baidu.com/")
time.sleep(2)
```
所有版本的驱动会下载到 `~\.cache\selenium`，可以按需清理。

下载来源：[https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json](https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json)



**其他功能**

获取当前操作系统的平台：

```python
from UpdateChromeDriver import os_type

print(os_type())
```

获取当前谷歌游览器的版本：

```python
from UpdateChromeDriver import get_browser_version_from_os

print(get_browser_version_from_os())
```

