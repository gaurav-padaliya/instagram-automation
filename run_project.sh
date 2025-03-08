#!/bin/bash
set -e

echo "Upgrading pip, setuptools, and wheel..."
pip3 install --upgrade pip setuptools wheel

echo "Installing dependencies using only binary wheels..."
pip3 install --no-cache-dir --only-binary=:all: -r requirements.txt

echo "Running main.py..."
python3 main.py


# python3 -m venv venv
# source venv/bin/activate