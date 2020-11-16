#!/bin/bash

cd /home/ec2-user/tofino
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt