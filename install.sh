#!/bin/bash

# Run as super user

#== Ubuntu/Debian ==#
apt update -y
apt install software-properties-common
add-apt-repository --yes --update ppa:deadsnakes/ppa
apt update -y
apt install pip -y
apt install npm -y
apt install node -y


# Install
cd backend
pip install -r ./backend/requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py runserver

# Install
cd ../../frontend
sudo apt install -y npm
npm run dev


