# Study Room

Study Room is a chat room webapp using django with login-authentication, CRED operation for user, chatroom and messages. Register and start learning.

Live - http://harshitpundir2000.pythonanywhere.com/

## Setup

Clone the repo on your system using

```bash
git clone https://github.com/Harshit-2000/StudyRoom.git
```

```bash
cd StudyRoom
```

Create a virtual environment

```bash
pip install virtualenv
python -m venv env
```

Activate a virtual env

```bash
.\env\script\activate
```

Installing Requirements

```bash
pip install -r requirements.txt
```

## Add a secret key

Create a file .env and add the below line

```bash
SECRET_KEY = 'a-secret-key'
```
## Migrate Project to the Database

Run the following command
```bash
python manage.py makemigrations
python manage.py migrate
```

## Run Project
```bash
python manage.py runserver
```
