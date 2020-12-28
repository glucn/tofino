# tofino

![CI/CD](https://github.com/glucn/tofino/workflows/build/badge.svg?branch=master)

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


AWS EC2
```
sudo yum install python3-devel mysql-devel gcc git -y
git clone https://github.com/glucn/tofino.git
cd tofino
python3 -m venv ./venv
source ./venv/bin/activate
pip install -r requirements.txt
nohup inv run &
```