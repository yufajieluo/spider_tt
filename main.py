#!/usr/bin/python
#-*-coding:utf-8-*-
# vim: tabstop=4 shiftwidth=4 softtabstop=4
# copyright 2019 WShuai, Inc.
# All Rights Reserved.

# @File: main.py
# @Author: WShuai, WShuai, Inc.
# @Time: 2019/11/29 16:20

import os
import sys

from commLog import get_logger
from commRedis import RedisHandler
from commConfig import CommConfig
from robot import Robot

def init():
    # init config
    config_file = './spider_tt.conf'
    comm_config = CommConfig(config_file)
    service_config = comm_config.get_config()

    # init log
    if not os.path.exists(os.path.split(service_config['LOG']['LOG_FILE'])[0]):
        os.makedirs(os.path.split(service_config['LOG']['LOG_FILE'])[0])
    logger = get_logger(service_config['LOG']['LOG_FILE'], service_config['LOG']['LOG_LEVEL'])
    return service_config, logger

if __name__ == '__main__':
    # init
    service_config, logger = init()
    logger.debug('service_config is {0}'.format(service_config))

    redis_handler = RedisHandler(
        service_config['REDIS']['REDIS_HOST'],
        service_config['REDIS']['REDIS_PORT'],
        service_config['REDIS']['REDIS_PASS'],
        service_config['REDIS']['REDIS_DB']
    )
    redis_handler.connect()

    target_users = service_config['SPIDER']['TARGET_USER'].split(',')
    for target_user in target_users:
        robot = Robot(
            target_user,
            service_config['SPIDER']['URL_START_PREFIX'],
            service_config['SPIDER']['WEB_DRIVER_FILE'],
            service_config['SPIDER']['IMAGES_STORE'],
            service_config['REDIS']['REDIS_KEY_NOTICE'],
            service_config['REDIS']['REDIS_KEY_OFFSET'],
            redis_handler,
            logger
        )
        robot.process()

    sys.exit(0)
