# Convo

Make sure you have python and redis instaled on your server

## Redis for windows

<https://github.com/tporadowski/redis/releases/download/v5.0.10/Redis-x64-5.0.10.msi>

Install pipenv

```.
pip install pipenv
```

In order to run the project, go to the base directory, where 'requirements.txt' file exists
Run the following commands:

```.
pipenv shell
pip install -r requirements.txt
cd convo
python manage.py makemigrations
python manage.py migrate --run-syncdb
python manage.py runserver
```

(requirements.txt contains all the python dependencies required to run the project)

## Details

The project, convo, consisting of two apps, is actually a chat application capable of handling voice communication and texting simultaneously as per the user's choice.
This is done via integrating web speech recognition and speech synthesis api
Note: This application does not support voice calls. Voice communication is only carried by speech recognition and synthesis.

There are two apps within this project:

1. users
    This app is in charge of handling all the user accounts as well the interaction between their profiles
    There are nine routes in this app. One for Home page, three for authentication, one for looking up a user with their username in the database, one for a list of the users you are connected on the site as friends, one for a list of the users who has requested to chat with you, one for viewing the profile of a user and the last route checks if there is any new chat request or chat message in the db.
    Views of this app controls the requests as per the route. Utils of the app contains additional functions to support the views carry out their tasks, like getting the valid button that is to be displayed on a user's profile, handling the request when the button is posted and saving the form to the database when a user updates their own profile.
    All the models are registered in the admin.py.
2. chat
    This app is in charge of handling real time communication via utilizing web sockets.
    There are two routes. One for viewing the chats of a user, where all the threads are displayed as per the previous chats. And another route to carry out a certain chat.
    Views of this app controls the requests as per the route.
    All the models are registered in the admin.py.
    Django Channels is used to handle long-running connections of websockets. ASGI server is used in this project, which is the asynchronous server specification that Channels is built on.
    To handle websocket requests, django consumer, basic unit of Channels code, is used here. On the other hand the http requests are still handled by the the django views.
    There is one consumer in consumers.py which handles the websocket requests in order to maintain the two-way interactive communication session between the user's browser and the server.
    Redis server is used in the project to store the messages temporarily in order to save them to the database in the near future.

The primary feature of this project is that it utilizes the webkit speech recognition and synthesis in order to carry out voice communication under circumstances when voice calls are not an option. Such circumstances include if one user can only talk while the other user can only text.

The client sided code contains functionality dedicated to handle such situations, btwMode or (too) busy to write Mode. Once initiated the speech recognition is activated, to record user's message. And on speech ending the message is automatically sent to the server, not requiring the user to send it. Upon recieving messages, speech synthesis is activated to read out the whole message of the other user. Once the whole message is read, speech recognition is activated to record the user's reply. This synthesis can be interrupted by pressing the third button under the textarea of the message form. This will stop the synthesis and start recognition. If a second message is recieved while recognition is activated, recognition will stop and the program will synthesize the recently recieved message. Speech is only synthesized if the message is not of the user.

There are two voice commands. Namely:

1. 'switch to text' which will end the btwMode
2. 'stop recognition' which will mark as the end of speech and therefore anything said after will not be included in the message

Note: Speech recognition is ran one last time after it closes to ensure there are no more speech to be recorded. It will keep run repeatedly as long as it recieves speech in its last run.
