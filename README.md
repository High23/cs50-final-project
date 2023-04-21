# Welcome to Info/Music finder for spotify!
### Video Demo:  https://youtu.be/ny6k7k7mnwQ
### Description:
This was made as my CS50 Final project. This project is web based and contains information regarding your spotify profile such as recently played, followed artists, liked songs, and your top artist/tracks given a certain time range. If you do decide to check this project out then you will need to go [here](https://developer.spotify.com/) and log in with your spotify account and create an app. Once an app is created then you will need to get the client id, client secret, and redirect url but make sure that you have a ".env" file to store the client id, secret and redirect url as variables. After you've set them as variables you would want to store those variables in spoti.py and app.py where there should be "os.getenv("your spotify client id")", you then store your variables in the proper "your spotify client id" place. 
#### spoti.py
This file is where the spotify api calls are made to get information, there are only two function which are user_auth and search_func. user_auth uses spotify's Authorization Code Flow to get information about the current user using the web app, the scopes passed through are playlist-read-private, user-library-read, user-modify-playback-state, user-read-email,
user-read-playback-state, user-read-private, user-read-recently-played, user-follow-read, and user-top-read. These scopes are necessary because they give access to all of the user's information that will displayed all around the webpages. Here is a list of [all possible scopes](https://developer.spotify.com/documentation/web-api/concepts/scopes). Now the search_func, the search_func does not need user authorization since the information being search is public BUT it does use a different method called Client credentials flow, this flow allows the web app to call upon the spotify api without the need of showing the user a popup for authorization.
#### app.py
This file is where most of the work is done getting specific information about a user and passing that information to html pages. Certain app routes require login which is handled by a global variable "authorization" that has either True or False, that global variable only changes when a user logs in or logs out. In app.py there is a variable in the index app route that calls upon user_auth, the reason for this is so that the results variable can store the object that return when the user_auth is done. That object gives us access to all the methods that the scopes returned such as .current_user() or .current_user_save_albums().
#### HTML files
These files just allow us to show all the data that we got through app.py. The data deponds on jinja syntax to be shown, there is also some javascript mainly in search.html which handles preview volume and index.html which changes the data shown if the user clicks on the three available options(ie. recently played).
#### CSS file
Makes the website look pretty.
#### Libraries used
os
spotipy
flask
flask_session 
dotenv 
# 
# 
#
