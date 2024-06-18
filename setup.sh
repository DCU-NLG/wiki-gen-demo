#!/bin/bash
apt install p7zip-full p7zip-rar

pip install --upgrade pip
pip install ipywidgets
pip install flask
pip install pandas
pip install numpy
pip install google-api-python-client

git submodule update --init --recursive
