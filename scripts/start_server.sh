#!/bin/bash

cd /home/ec2-user/tofino/
source ./venv/bin/activate
export FLASK_APP main.py
python -m flask run --host=0.0.0.0
