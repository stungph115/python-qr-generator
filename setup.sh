#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null
then
    echo "Python could not be found. Please install Python before running this script."
    exit
fi

# Install pip if not installed
if ! command -v pip3 &> /dev/null
then
    echo "pip could not be found. Installing pip..."
    sudo apt-get install python3-pip -y
fi

# Install tkinter if not installed
if ! python3 -c "import tkinter" &> /dev/null
then
    echo "tkinter could not be found. Installing tkinter..."
    sudo apt-get install python3-tk -y
fi

# Install required packages
echo "Installing required packages..."
pip3 install -r requirements.txt

echo "Setup completed. You can now run the script using 'python3 qr-gen.py'."
