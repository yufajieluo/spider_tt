#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: webdriver.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/11/29 9:39

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class WebDriver(object):
    def __init__(self, webdriver_file):
        self.driver_file = webdriver_file
        self.driver = None
        self.wait_timeout = 30
        self.wait_interval = 1
        return

    def init_webdriver(self):
        chrome_options = Options()
        # 解决DevToolsActivePort文件不存在的报错
        chrome_options.add_argument('--no-sandbox')
        # 指定浏览器分辨率
        chrome_options.add_argument('window-size=1920x3000')
        # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--disable-gpu')
        # 隐藏滚动条, 应对一些特殊页面
        chrome_options.add_argument('--hide-scrollbars')
        # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
        chrome_options.add_argument('--headless')
        chrome_options.add_argument(f'user-agent=I LOVE TTW')
        # 不加载图片, 提升速度
        chrome_options.add_argument('blink-settings=imagesEnabled=false')
        self.driver = webdriver.Chrome(self.driver_file, chrome_options=chrome_options)
        return

    def wait(self, xpath):
        result = None
        try:
            WebDriverWait(self.driver, 20, 0.5).until(
                EC.presence_of_element_located(
                    (By.XPATH, xpath)
                )
            )
            result = True
        except Exception as e:
            result = False
        return result

    def close(self):
        self.driver.close()
        return
