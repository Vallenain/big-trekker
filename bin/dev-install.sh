#!/usr/bin/env bash

set -e

echo "==== Configuring dependencies for development ===="
echo "======= Server installation (PIP) ======"

rm -rf .venv
virtualenv --clear .venv
source .venv/bin/activate
sudo pip install -r requirements-dev.txt
rm -rf .python-libs
linkenv .venv/lib/python2.7/site-packages .python-libs

echo "======= Assets installation (BOWER) ======"
#bower install

echo "======= Development libs install (NPM) ======"
sudo npm i --env=dev

echo "======= Prepararing application in DEV MODE ======"
sudo npm run build:dev
