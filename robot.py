#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: robot.py.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/11/29 9:32

import os
import uuid
import requests
from webdriver import WebDriver

class Robot(object):
    def __init__(self, id, start_url_prefix, webdriver_file, save_path, redis_key_notice, redis_key_offset, redis_handler, logger):
        self.id = id
        self.webdriver_file = webdriver_file
        self.save_path = save_path
        self.redis_key_notice = redis_key_notice
        self.redis_key_offset = redis_key_offset
        self.redis_handler = redis_handler
        self.logger = logger

        self.start_url = '{0}/{1}/'.format(start_url_prefix, self.id)
        self.last_offset = None
        self.current_offset = None
        self.webdriver = None
        self.albums_urls = []

        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        return

    def get_wait_albums(self):
        xpath_wtt = '//div[@id="wrapper"]/div[@class="left"]/div[@riot-tag="tab"]/ul/li[3]'
        if self.webdriver.wait(xpath_wtt):
            while True:
                self.webdriver.driver.find_element_by_xpath(xpath_wtt).click()
                xpath_ul_wait = '//div[@class="relatedFeed"]/ul/li[1]/div/div[@class="normal rbox "]'
                if self.webdriver.wait(xpath_ul_wait):
                    break
                else:
                    self.logger.error('get ul element failed.')
                    continue

            elemet_ul = self.webdriver.driver.find_element_by_xpath('//div[@class="relatedFeed"]/ul')
            offset_li = 0
            while True:
                elemet_lis = elemet_ul.find_elements_by_xpath('li')

                stop = False
                for elemet_li in elemet_lis[offset_li:]:
                    xpath_a = 'div/div[@class="normal rbox "]/div[@class="rbox-inner"]/div[@class="ugc-box"]/div[@class="ugc-content"]/a'
                    album_href = elemet_li.find_element_by_xpath(xpath_a).get_attribute('href')
                    offset_li += 1
                    self.logger.info('{0} album href is {1}'.format(offset_li, album_href))
                    if album_href.split('www.toutiao.com/a')[-1] != self.last_offset:
                        if offset_li == 1:
                            self.current_offset = album_href.split('www.toutiao.com/a')[-1]
                        self.albums_urls.append(album_href)
                    else:
                        stop = True
                        break

                if not stop:
                    self.webdriver.driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
                else:
                    break
        else:
            self.logger.error('get wtt element failed.')
        return

    def get_single_album(self, url):
        album_driver = WebDriver(self.webdriver_file)
        album_driver.init_webdriver()
        album_driver.driver.get(url)

        xpath_div_image = '//div[@class="bui-box container"]/div[@class="bui-left index-middle"]/div[@class="article-box"]'
        if album_driver.wait(xpath_div_image):
            element_div_image = album_driver.driver.find_element_by_xpath(xpath_div_image)
            element_images = element_div_image.find_elements_by_xpath('img')
            for element_image in element_images:
                #self.logger.info('image href is {0}'.format(element_image.get_attribute('src')))
                local_file = os.path.join(self.save_path, '{0}.jpg'.format(uuid.uuid4()))
                self.download_image(element_image.get_attribute('src'), local_file)
                self.save_redis(local_file)
        else:
            self.logger.error('get album div image failed, url is {0}'.format(url))

        album_driver.close()
        return

    def download_image(self, url, local_file):
        response = requests.get(url)
        with open(local_file, 'wb') as file_handler:
            file_handler.write(response.content)
        return

    def save_redis(self, local_file):
        if self.redis_handler.connect():
            self.redis_handler.redis_conn.sadd(self.redis_key_notice, local_file)
        return

    def get_offset(self):
        last_offset = self.redis_handler.redis_conn.hget(self.redis_key_offset, self.id)
        if last_offset:
            self.last_offset = last_offset.decode()
        return

    def set_offset(self):
        if self.current_offset:
            self.redis_handler.redis_conn.hset(self.redis_key_offset, self.id, self.current_offset)
        return

    def process(self):
        self.webdriver = WebDriver(self.webdriver_file)
        self.webdriver.init_webdriver()
        self.webdriver.driver.get(self.start_url)

        self.get_offset()
        self.logger.debug('url is {0}, offset is {1}'.format(self.start_url, self.last_offset))
        self.get_wait_albums()
        for albums_url in self.albums_urls:
            self.get_single_album(albums_url)
        self.set_offset()

        self.webdriver.close()
        return

