#!/bin/bash
base_path=$(cd `dirname $0`; pwd)

ps -ef | grep webdriver | grep -v grep | awk '{print $2}' | xargs kill -9 
venv_path=${base_path}"/venv/bin/activate"
source ${venv_path}
python main.py
