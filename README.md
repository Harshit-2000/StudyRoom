# Study Room

Study Room is a chat room webapp using django with login-authentication, CRED operation for user, chatroom and messages. Register and start learning.
<br>
Supports real time group chat using django chanels and websockets.

![Screenshot (66)](https://user-images.githubusercontent.com/70425491/227778755-180e4d5d-1732-4c94-990f-6dafb1a41ab4.png)

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
## Start a redis server 

Start a redis server and change the hosts parameter to your own redis server in the settings.py file.
```
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis://default:redispw@localhost:32768")],
        },
    },
}
```

<b> OR if you are facing issues setting redis server, replace the above lines with the code below </b>

```
CHANNEL_LAYERS = {
     "default": {
         "BACKEND": "channels.layers.InMemoryChannelLayer"
     }
 }
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
