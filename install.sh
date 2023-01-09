#!/bin/bash

# Run as super user

#== Ubuntu/Debian ==#
apt update -y
apt install software-properties-common
add-apt-repository --yes --update ppa:deadsnakes/ppa
apt update -y
apt install pip -y
apt install node -y


# Install 
pip install -r ./backend/requirements.txt

# Install

sudo apt install -y npm
sudo npm install --prefix ./frontend