import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from datetime import date


config_file = 'config'
client_id = ''
client_secret = ''
redirect_uri = ''
username = ''
scope = ''
sp = ''

date_before = '2019-09-11T00:00:00Z'


def setUp():
    with open(config_file, 'r') as config:
        configVals = [line.rstrip('\n') for line in config]
        global client_id, client_secret, redirect_uri, username, scope
        client_id = configVals[0]
        client_secret = configVals[1]
        redirect_uri = configVals[2]
        scope = configVals[3]
        username = configVals[4]
    token = util.prompt_for_user_token(
        username=username, scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)
    global sp
    sp = spotipy.Spotify(auth=token)


def show_tracks(results, tracks_to_move):

    for item in results['items']:
        track = item['track']
    #    print("%32.32s %32.32s %32s %s" % (
    #        track['artists'][0]['name'], track['name'], item['added_at'], date_before >= item['added_at']))
        if date_before >= item['added_at']:
            tracks_to_move.append(track['id'])
    return tracks_to_move


def create_playlist():
    today = date.today().strftime('%b %Y')
    # print(today)
    if sp:
        results = sp.user_playlist_create(
            username, 'Archive ' + str(today), public=True, description='Created by spotify-archive')
        return results['id']
    else:
        return None


def getSavedSongs():
    if sp:
        results = sp.current_user_saved_tracks()
        tracks_to_move = []
        tracks_to_move = show_tracks(results, tracks_to_move)
        while results['next']:
            results = sp.next(results)
            tracks_to_move = show_tracks(results, tracks_to_move)
        return tracks_to_move
    else:
        print("Can't get token for", username)


def add_to_playlist(new_playlist_id, tracks_to_move):
    if sp:
        results = sp.user_playlist_add_tracks(
            username, new_playlist_id, tracks_to_move)
        # print(results)
    else:
        print('''couldn't do it ''')

def delete_from_saved(tracks_to_move):
    if sp:
        sp.trace = False
        results = sp.current_user_saved_tracks_delete(tracks=tracks_to_move)
        print(results)
    else:
        print('Token error')

setUp()
tracks_to_move = getSavedSongs()
print(tracks_to_move)
new_playlist_id = create_playlist()
add_to_playlist(new_playlist_id, tracks_to_move)
delete_from_saved(tracks_to_move)
