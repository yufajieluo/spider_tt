#!/bin/bash
base_path=$(cd `dirname $0`; pwd)

venv_path=${base_path}"/venv/bin/activate"
source ${venv_path}
python main.py
