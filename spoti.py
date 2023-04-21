import os
import spotipy
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth, SpotifyClientCredentials
from functools import wraps
from flask import redirect, url_for, session, flash

load_dotenv()
client_id = os.getenv("your spotify client id")
client_secret = os.getenv("your spotify client secret")
redirect_uri = os.getenv("your spotify redirect uri")


def user_auth():
    # Grab the scopes that will be used throughout the program
    scope = "playlist-read-private user-library-read user-modify-playback-state user-read-email user-read-playback-state user-read-private user-read-recently-played user-follow-read user-top-read"
    # The custom cache handler provided by the spotipy library allows us to store the access token that spotify gives when the user grants authorization,
    # the token is then stored in the session variable from the flask library(line 6), this custom cache handler allows the program to only ask once for user authentication.
    # When the function is recalled, the function will return the same sp variable with the current user's info because the cache handler is storing the access toke seperately for the
    # current user
    cache_handler = spotipy.cache_handler.FlaskSessionCacheHandler(session)
    # Oauth is used because the program is using user information or according to spotify, authorization code flow.
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id, client_secret=client_secret, 
                                                   redirect_uri=redirect_uri, scope=scope, cache_handler=cache_handler, 
                                                   show_dialog=True))
    return sp

def search_func(search_data, search_type):
    # The search function does not need user authetication since the information being searched for is public not private or user information
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
    results = sp.search(q=f"{ search_data }", type=f"{ search_type }", limit=50) # The information passed by the search bar is place into the search function dynamically with a limit of 50(the cap).
    returned_data = [] # Make an empty list so that the information returned by sp.search will be stored properly since sp.search returns info in dicts.
    # This if and elif statements will check if the search type was one of three available options, The for loops will store proper data according to the search type
    if search_type == "artist": 
        for  item in results["artists"]["items"]: #type: ignore
            returned_data.append(item) 
    elif search_type == "album": 
        for  item in results['albums']["items"]: #type: ignore
            returned_data.append(item)
    elif search_type == 'track':
        for  item in results['tracks']["items"]: #type: ignore
            returned_data.append(item)
    if bool(returned_data) == False: # placed incase of user adjusting the value of the options in the inspect elements tab
        raise ValueError
    return returned_data 
    

def login_required(f):
    # Copied from flask's webpage which is linked below, modified a bit so that authorization is used as the "checker"
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/2.2.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from app import authorization
        if authorization is None or authorization is False:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


