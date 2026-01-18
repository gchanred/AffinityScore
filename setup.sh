#!/bin/bash

# Check for Python 3
if command -v python3 &> /dev/null; then
    echo "Python 3 detected."
    python3 install.py
# Fallback to checking 'python'
elif command -v python &> /dev/null; then
    echo "Python detected. Assuming it is a compatible version."
    python install.py
else
    echo "Error: Python is not installed on this system."
    echo "Please download and install Python 3 from https://www.python.org/downloads/"
    exit 1
fi
