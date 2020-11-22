#!/bin/bash

cd /home/ec2-user/tofino/
source venv/bin/activate
supervisord -c supervisord.conf
