import os
import time
import traceback
from enum import Enum

import requests
from lxml import etree
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


COMMON_HEADER = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Cache-Control": "max-age=0",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-User": "?1",
    "Upgrade-Insecure-Requests": "1",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "Windows",
}


class REQUEST_METHOD(Enum):
    GET = 1
    POST = 2


def send_request(src, headers=None, encoding='utf-8', method: REQUEST_METHOD = REQUEST_METHOD.GET):
    """
    发送请求, 如果顺利得到response并没有爆出任何错误,同时状态码为200, 则正常返回, 否则给出失败提示,
    需要调用者自行决定是否进行成功提示, 该函数不提供
    """
    if headers is None:
        headers = COMMON_HEADER
    response = None
    try:
        if method == REQUEST_METHOD.GET:
            response = requests.get(src, headers=headers)
        elif method == REQUEST_METHOD.POST:
            response = requests.post(src, headers=headers)
        if not hasattr(response, 'status_code'):
            raise RuntimeError()
        if not (response.status_code == 200 or response.status_code == 206):
            raise RuntimeError()
    except Exception as e:
        if hasattr(response, 'status_code'):
            print(f"请求失败{e},code:{response.status_code}")
        else:
            print(f"请求失败{e}")
        traceback.print_exc()
        return None
    response.encoding = encoding
    return response


class FileType(Enum):
    HTML = 1,
    XML = 2,


def text2special_file(text, file_type: FileType = FileType.HTML):
    if file_type == FileType.HTML:
        try:
            tree = etree.HTML(text)
        except Exception as e:
            print('text->html失败')
            return None
        return tree


def write_to_html(data, file_name):
    if not os.path.exists(os.path.dirname(file_name)):
        os.makedirs(os.path.dirname(file_name), exist_ok=True)
    with open(file_name, 'w', encoding='utf-8') as f:
        f.write(data)


def handle_xpath(html_text: str, xpath: str):
    try:
        tree = etree.HTML(html_text)
        datas = tree.xpath(xpath)
        # datas = tree.cssselect(xpath)
        if len(datas) == 0 or len(datas[-1]) == 0:
            print("datas:", datas)
            raise RuntimeError()
        return datas
    except Exception as e:
        print('xpath处理失败')
        traceback.print_exc()
        return None


def handle_xpath_sub(tree: etree.ElementTree, xpath):
    try:
        datas = tree.xpath(xpath)
        if len(datas) == 0 or len(datas[-1]) == 0:
            raise RuntimeError()
        return datas
    except Exception as e:
        print('xpath处理失败')
        return None


def do_a_click_to_a_driver(driver: webdriver.Chrome, button_location_xpath):
    """
    传入一个button的地址, 做到点击它的效果, 并返回页面源码
    """
    button = driver.find_element(By.XPATH, button_location_xpath)
    button.click()
    driver.implicitly_wait(1)
    time.sleep(1)
    # 获取网页源码
    html = driver.page_source
    return html, driver


def get_source_page_from_url(url: str, debug_chrome:bool=False):
    if debug_chrome:
        options = Options()
        options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
        driver = webdriver.Chrome(options=options)
    else:
        driver = webdriver.Chrome()
    driver.get(url)
    driver.implicitly_wait(2)
    time.sleep(2)
    html = driver.page_source
    return html, driver


def get_source_page_from_url_have_driver(url: str, driver: webdriver.Chrome):
    driver.get(url)
    driver.implicitly_wait(1)
    time.sleep(1)
    html = driver.page_source
    return html, driver