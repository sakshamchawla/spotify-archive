import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

config_file = 'config'
client_id=''
client_secret=''
redirect_uri=''
username=''
scope=''

def setUp():
    with open(config_file, 'r') as config:
        configVals = [line.rstrip('\n') for line in config]
        global client_id, client_secret, redirect_uri, username, scope
        client_id = configVals[0]
        client_secret = configVals[1]
        redirect_uri = configVals[2]
        scope = configVals[3]
        username = configVals[4]

def show_tracks(results):
    for item in results['items']:
        track = item['track']
        print("%32.32s %32.32s %32s" % (track['artists'][0]['name'], track['name'], item['added_at']))

def getSavedSongs():
    token = util.prompt_for_user_token(username=username,scope=scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_uri)

    if token:
        sp = spotipy.Spotify(auth=token)
        results = sp.current_user_saved_tracks()
        show_tracks(results)
        while results['next']:
            results = sp.next(results)
            show_tracks(results)
    else:
        print("Can't get token for", username)

setUp()
getSavedSongs()
