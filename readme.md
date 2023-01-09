# AgendaSSD

Mushingelete Aramson Felho - Matricule: 000574088
Ayoub Touhami - Matricule: 575007


## How to use install the project

Run the installation script 'install.sh'

`
cd AgendaSSD

sudo chmod +x install.sh

sudo ./install.sh

`

Run the installation script 'install.sh'

## How to run the project

Backend port 8000:

´
cd backend

python3 manage.py migrate

python3 manage.py runserver
 ´

 Frontend (on another terminal) port 5173 :
 
 ´
cd frontend

npm install node 

npm run dev

´ 

## Account Activation

After registration, a mail will be sent to activate the account. Most likely, the mail will be in the spam list. After clicking on the link you will not be redirected, but you will be able to login on the client (port 5173).