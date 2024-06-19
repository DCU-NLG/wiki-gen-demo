#!/bin/bash
apt install p7zip-full p7zip-rar

pip install --upgrade pip
pip install ipywidgets
pip install flask
pip install pandas
pip install numpy
pip install google-api-python-client
pip install SPARQLWrapper

git submodule update --init --recursive
