#!/usr/bin/sh

export PYTHONPATH=/home/helio/github/RIDE/utest/:$PYTHONPATH
export PYTHONPATH=/home/helio/github/RIDE/src/:$PYTHONPATH

export PYTHONROOT=/usr/bin

cd /home/helio/github/RIDE/
# pytest -k test_ --ignore-glob=../../../../usr/* --ignore-glob=/usr/lib64/python3.10/site-packages/* --ignore-glob=/home2/helio/.local/* -v  --cov=./src --cov=./utest --cov-report=html:.coverage-reports/htmlcov --cov-report=xml:.coverage-reports/coverage.xml --cov-branch ./utest 

PYTHONROOT=/usr/bin PYTHONPATH=/home/helio/github/RIDE/src/:/home/helio/github/RIDE/utest/:$PYTHONPATH  coverage run -m pytest -k test_ --ignore-glob=../../../../usr/* --ignore-glob=/usr/lib64/python3.10/site-packages/* --ignore-glob=/home2/helio/.local/* -v ./utest

coverage report
coverage xml
coverage html

