# 博客地址：https://blog.csdn.net/as604049322
__author__ = '小小明-代码实体'
__date__ = '2023/11/1'

import os
import platform
import re
import subprocess
import sys
import zipfile

import requests
from selenium.common import WebDriverException
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm


def linux_browser_apps_to_cmd() -> str:
    """获取以下类似的命令的结果:
        google-chrome --version || google-chrome-stable --version
    """
    apps = ("google-chrome", "google-chrome-stable",
            "google-chrome-beta", "google-chrome-dev")
    ignore_errors_cmd_part = " 2>/dev/null" if os.getenv("WDM_LOG_LEVEL") == "0" else ""
    return " || ".join(f"{i} --version{ignore_errors_cmd_part}" for i in apps)


def window_get_browser_version():
    """代码作者：小小明-代码实体 xxmdmst.blog.csdn.net"""
    import winreg
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                             r"SOFTWARE\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        winreg.CloseKey(key)
        return version
    except:
        pass
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
                             r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome")
        version, _ = winreg.QueryValueEx(key, "version")
        winreg.CloseKey(key)
        return version
    except:
        pass


def read_version_from_cmd(cmd):
    with subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                          stdin=subprocess.DEVNULL, shell=True) as stream:
        stdout = stream.communicate()[0].decode()
    return stdout


def get_browser_version_from_os():
    pl = sys.platform
    try:
        if pl == "linux" or pl == "linux2":
            cmd = linux_browser_apps_to_cmd()
            version = read_version_from_cmd(cmd)
        elif pl == "darwin":
            cmd = r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version"
            version = read_version_from_cmd(cmd)
        elif pl == "win32":
            version = window_get_browser_version()
        else:
            return None
        version = re.search(r"\d+\.\d+\.\d+", version)
        return version.group(0) if version else None
    except Exception as e:
        return None


def os_type():
    pl = sys.platform
    architecture = platform.machine().lower()
    if pl == "darwin":
        if architecture == "x86_64":
            architecture = "x64"
        return f"mac-{architecture}"
    pl = re.search("[a-z]+", pl).group(0)
    architecture = 64 if architecture.endswith("64") else 32
    return f"{pl}{architecture}"


def get_chromedriver_url(version):
    chrome_url = "https://googlechromelabs.github.io/chrome-for-testing/known-good-versions-with-downloads.json"
    res = requests.get(chrome_url)
    os_type_str = os_type()
    for obj in reversed(res.json()["versions"]):
        if obj["version"].startswith(version):
            for downloads in obj["downloads"]["chromedriver"]:
                if downloads["platform"] == os_type_str:
                    return obj["version"], downloads["url"]
            break


def show_download_progress(response, _bytes_threshold=100):
    """代码作者：小小明-代码实体 xxmdmst.blog.csdn.net"""
    total = int(response.headers.get("Content-Length", 0))
    if total > _bytes_threshold:
        content = bytearray()
        progress_bar = tqdm(desc="[WDM] - Downloading", total=total,
                            unit_scale=True, unit_divisor=1024, unit="B")
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:
                progress_bar.update(len(chunk))
                content.extend(chunk)
        progress_bar.close()
        response._content = content


def install_new_driver():
    """代码作者：小小明-代码实体 xxmdmst.blog.csdn.net"""
    version = get_browser_version_from_os()
    print(f"谷歌游览器版本：{version}")
    driver_version, url = get_chromedriver_url(version)
    filename = url[url.rfind("/") + 1:]
    filename, ext = os.path.splitext(filename)
    selenium_dir = os.path.join(os.path.expanduser("~"), ".cache", "selenium")
    os.makedirs(selenium_dir, exist_ok=True)
    file = f"{selenium_dir}/{filename}_v{driver_version}{ext}"
    if os.path.exists(file):
        print(file, "已存在，跳过下载~")
    else:
        resp = requests.get(url, stream=True)
        show_download_progress(resp)
        with open(file, 'wb') as f:
            f.write(resp._content)
    suffix = ".exe" if sys.platform == "win32" else ""
    with zipfile.ZipFile(file) as zf:
        for name in zf.namelist():
            if name.endswith("chromedriver" + suffix) and "LICENSE.chromedriver" not in name:
                zf.extract(name, selenium_dir)
                print(name, "已解压到", selenium_dir)
                break
    src = os.path.join(selenium_dir, name)
    dest = os.path.join(selenium_dir, os.path.basename(name))
    if src != dest:
        if os.path.exists(dest):
            os.remove(dest)
        os.rename(src, dest)
        print("已从", src, "移动到", dest)
    return dest


def getChromeBrowser(options=None):
    """代码作者：小小明-代码实体 xxmdmst.blog.csdn.net"""
    suffix = ".exe" if sys.platform == "win32" else ""
    executable_path = "chromedriver" + suffix
    selenium_dir = os.path.join(os.path.expanduser("~"), ".cache", "selenium")
    executable_path = os.path.join(selenium_dir, executable_path)
    service = Service(executable_path=executable_path)
    if not os.path.exists(executable_path) and get_browser_version_from_os() > "115":
        # 如果chromedriver不存在并且版本大于114直接升级，否则可以使用selenium4自动获取driver的功能
        install_new_driver()
        driver = webdriver.Chrome(options=options, service=service)
        return driver
    try:
        driver = webdriver.Chrome(options=options, service=service)
        return driver
    except WebDriverException as e:
        install_new_driver()
        print(e)
    driver = webdriver.Chrome(options=options, service=service)
    return driver

# if __name__ == '__main__':
#     options = webdriver.ChromeOptions()
#     options.add_experimental_option(
#         'excludeSwitches', ['enable-logging', 'enable-automation'])
#     browser = getChromeBrowser(options)
#     browser.get("https://www.baidu.com/")
#     time.sleep(5)
