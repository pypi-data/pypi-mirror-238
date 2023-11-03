用法示例：

```python
from UpdateChromeDriver.UpdateChromeDriver import *

options = webdriver.ChromeOptions()
options.add_experimental_option(
    'excludeSwitches', ['enable-logging', 'enable-automation'])
browser = getChromeBrowser(options)
browser.get("https://www.baidu.com/")
time.sleep(2)
```
驱动会从下载到~\.cache\selenium
下载来源：https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json

下载最新版：
```shell script
pip install UpdateChromeDriver --index-url https://pypi.org/simple/ -U
```
