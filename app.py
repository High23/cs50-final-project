import os
import spotipy

from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from dotenv import load_dotenv

from spoti import user_auth, login_required, search_func

load_dotenv()
client_id = os.getenv("your spotify client id") # Where you would place your spotify client id
client_secret = os.getenv("your spotify client secret") # Where you would place your spotify client secret
redirect_uri = os.getenv("your spotify redirect uri") # Where you would place your redirect uri
authorization = None

app = Flask(__name__)
app.secret_key = 'Your super secret key'

# Lines 21-32 are credited to and can be found from CS50 2022 week 9 finance, lines 17-20 and 30-36
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/",  methods=["GET", "POST"])
@login_required
def index():
    # Try blocks are used so that when the program know what to do after the user clicks an option on the authorization page(ie. "authorize", "cancel")
    try:
        # If the user clicks "authorize" then the program will proceed to grab the user's recently played, profile information, followed artists, and liked songs.
        # The authorization is a one time event, check the spoti.py file on lines 17-18 for more information
        results = user_auth()
        recently_played = results.current_user_recently_played(limit=20)
        _current_user = results.current_user()
        following = results.current_user_followed_artists(limit=20)
        liked_songs = results.current_user_saved_albums(limit=20)
    except (spotipy.oauth2.SpotifyOauthError, spotipy.exceptions.SpotifyException):
        # if the user were to click "cancel" then a message will flash that the authorization failed and the user will be redirected to the login page
        flash("Authorization Failed!")
        return redirect("/login")
    # Render the index.html file using the authorized information
    return render_template("index.html", authorization=authorization, recently_played=recently_played, 
                            current_user=_current_user, following=following, liked_songs=liked_songs)

@app.route("/login", methods=["GET", "POST"])
def login():
    global authorization
    if request.method == "POST": # If the user clicks the login button
        authorization = True # Set the global variable to True
        return redirect("/") # Redirect to the index page
    else: # No button was clicked because the user only requested the login page
        authorization = False # Set the global variable to False
        return render_template("login.html") # Render the login page

@app.route("/logout")  
def logout():
    # Set the global variable to false and clear the session cache handler to that the user will have to reauthorize afterwards redirect the user to the login page
    global authorization
    authorization = False
    session.clear()
    return redirect("/login")

@app.route("/playlist")
@login_required
def playlist():
    # Grab the current user's playlist and return the data into the playlists template
    results = user_auth()
    playlists = results.current_user_playlists(limit=50) # type: ignore
    return render_template("playlists.html", authorization=authorization, playlists=playlists)

@app.route("/search", methods=["GET", "POST"])
def search():
    if request.method == "POST": # If the user sent a post request when searching for an artist
        search_data = request.form.get("data") # Grab the data which would be the text typed by the user
        search_type = request.form.get("type") # Grab the type of data the user selected
        if search_data == "" or search_type == None: # Check that the variable are not empty
            flash("One or more parameters are missing!") # if one of the variables are then flash a message
        else:
            try:
                # Pass the information into the search function which is located in the spoti.py file
                results = search_func(search_data, search_type)
                # Store the search function results into a variable that is then passed into the search template to be used
                return render_template("search.html", authorization=authorization, results=results)
            except (spotipy.exceptions.SpotifyException, ValueError): # Incase of the user changing the value from the inspect element tab
                flash("One or more invalid values passed!") # Flash the message "One or more invalid values passed!"
        return redirect("/search") # Redirect to the search page which will then redirect to the index page
    else:
        return redirect("/")
    
@app.route("/top",  methods=["GET", "POST"])
@login_required
def top():
    # Grab the user's top artists and tracks with the time range set at the default value "short term"
    results = user_auth()
    _current_user = results.current_user()
    top_artists = results.current_user_top_artists(limit=30, time_range='short_term')
    top_tracks = results.current_user_top_tracks(limit=20, time_range='short_term')
    if request.method == "POST": # If the user adjusts the time range 
        range = request.form.get("range") # Set a variable to that time range
        try: 
            # Try grabbing the user's top tracks/artists
            top_artists = results.current_user_top_artists(limit=20, time_range=f"{ range }")
            top_tracks = results.current_user_top_tracks(limit=20, time_range=f'{ range }')
        except spotipy.exceptions.SpotifyException: # If an invalid value is passed flash the message "Invalid value"
            flash("Invalid value")
        # if a valid value was passed then render the template with user's top tracks/artists given the time range.
        # Otherwise short range is passed in by default
        return render_template("top.html", authorization=authorization, top_artists=top_artists, top_tracks=top_tracks, current_user=_current_user)
    else:
        return render_template("top.html", authorization=authorization, top_artists=top_artists, top_tracks=top_tracks, current_user=_current_user)