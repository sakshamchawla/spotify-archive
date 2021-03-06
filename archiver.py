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
id_offset_found = False
start_id_offset_found = False
end_id_offset_found = False


"""
Initial set up config files
Initializes Spotify and does authorization
"""


def setUp():
    print('Setting up')
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

# prints out tracks in results


def show_tracks(results):
    for item in results['items']:
        track = item['track']
        print("%32.32s %32.32s %32s %s" % (
            track['artists'][0]['name'], track['name'], item['added_at'], date_before >= item['added_at']))


"""
Creates a new playlist
Names it as "Archive Month-Year"
"""


def create_playlist():
    print('Creating playlist')
    today = date.today().strftime('%b %Y')
    # print(today)
    if sp:
        results = sp.user_playlist_create(
            username, 'Archive ' + str(today), public=True, description='Created by spotify-archive')
        return results['id']
    else:
        return None


"""
Adds all the songs to a playlist
"""


def add_to_playlist(new_playlist_id, tracks_to_move):
    print('Adding ' + str(len(tracks_to_move)) + ' songs to playlist')
    if sp:
        if len(tracks_to_move) > 100:
            for i in range(0, len(tracks_to_move), 100):
                results = sp.user_playlist_add_tracks(
                    username, new_playlist_id, tracks_to_move[i:i + 100])
        else:
            results = sp.user_playlist_add_tracks(
                username, new_playlist_id, tracks_to_move)
        # print(results)
    else:
        print('''couldn't do it ''')


"""
Deletes songs from Saved List
"""


def delete_from_saved(tracks_to_move, new_playlist_id):
    if sp:
        text = input(
            'Playlist has been created.\nAre you sure you to delete from Saved Songs? (Yes or No) ')
        if text.lower() == 'yes':
            sp.trace = False
            if len(tracks_to_move) > 50:
                for i in range(0, len(tracks_to_move), 50):
                    results = sp.current_user_saved_tracks_delete(
                        tracks=tracks_to_move[i:i+50])
            else:
                results = sp.current_user_saved_tracks_delete(
                    tracks=tracks_to_move)
        else:
            print('Aborted. Delete Playlist manually')
    else:
        print('Token error')


"""
Gets the tracks in a "subset" of tracks stored in "results"
"""


def get_tracks_by_date_offset(results, tracks_to_move, date_before):
    for item in results['items']:
        track = item['track']
        if date_before >= item['added_at']:
            tracks_to_move.append(track['id'])
    return tracks_to_move


"""
Gets all the tracks by calling get_tracks_by_date_offset()
"""


def get_all_tracks_by_date_offset(date_before):
    if sp:
        print('Getting songs')
        results = get_first_saved_songs()
        # show_tracks(results)
        tracks_to_move = []
        tracks_to_move = get_tracks_by_date_offset(
            results, tracks_to_move, date_before)
        while results['next']:
            results = sp.next(results)
            tracks_to_move = get_tracks_by_date_offset(
                results, tracks_to_move, date_before)
        return tracks_to_move
    else:
        print("Can't get token for", username)


"""
Returns the first set of saved songs
"""


def get_first_saved_songs():
    if sp:
        results = sp.current_user_saved_tracks()
        return results
    else:
        print("Can't get token for", username)


"""
Gets tracks starting from id [id:] in subset
"""


def get_tracks_by_id_offset(results, tracks_to_move, id_offset):
    for item in results['items']:
        track = item['track']
        global id_offset_found
        if not id_offset_found:
            if id_offset == track['id']:
                tracks_to_move.append(track['id'])
                id_offset_found = True
            else:
                continue
        else:
            tracks_to_move.append(track['id'])
    return tracks_to_move


"""
Gets tracks starting from id [id:] by get_tracks_by_id_offset
"""


def get_all_tracks_by_id_offset(id_offset):
    if sp:
        print('Getting songs')
        results = get_first_saved_songs()
        tracks_to_move = []
        tracks_to_move = get_tracks_by_id_offset(
            results, tracks_to_move, id_offset)
        while results['next']:
            results = sp.next(results)
            tracks_to_move = get_tracks_by_id_offset(
                results, tracks_to_move, id_offset)
        return tracks_to_move
    else:
        print("Can't get token for", username)


"""
Gets tracks starting from id and ending by id in subset
"""


def get_tracks_by_se_id_offset(results, tracks_to_move, start_id_offset, end_id_offset, ids_exceptions):
    if start_id_offset == end_id_offset:
        return tracks_to_move.append(start_id_offset)
    for item in results['items']:
        track = item['track']
        global start_id_offset_found, end_id_offset_found
        if not start_id_offset_found:
            if start_id_offset == track['id']:
                tracks_to_move.append(track['id'])
                start_id_offset_found = True
            else:
                continue
        elif not end_id_offset_found:
            if end_id_offset == track['id']:
                tracks_to_move.append(track['id'])
                end_id_offset_found = True
            elif not end_id_offset_found:
                tracks_to_move.append(track['id'])
    [tracks_to_move.remove(id)
     for id in ids_exceptions if id in tracks_to_move]
    return tracks_to_move


"""
Gets all tracks starting from id and ending by id
ids_exceptions - list of ids in the range which should be exempted
"""


def get_all_tracks_by_se_id_offset(start_id_offset, end_id_offset, ids_exceptions):
    if sp:
        print('Getting songs')
        results = get_first_saved_songs()
        tracks_to_move = []
        tracks_to_move = get_tracks_by_se_id_offset(
            results, tracks_to_move, start_id_offset, end_id_offset, ids_exceptions)
        while results['next']:
            if not end_id_offset_found:
                results = sp.next(results)
                tracks_to_move = get_tracks_by_se_id_offset(
                    results, tracks_to_move, start_id_offset, end_id_offset, ids_exceptions)
        return tracks_to_move
    else:
        print("Can't get token for ", username)


if __name__ == "__main__":
    if len(sys.argv) > 2:
        setUp()
        mode = sys.argv[1]
        if mode == 'date':
            if sys.argv[2]:
                date_before = sys.argv[2] + 'T00:00:00Z'
                tracks_to_move = get_all_tracks_by_date_offset(date_before)
            else:
                raise ValueError('Error: Missing date')
        if mode == 'id':
            if sys.argv[2]:
                tracks_to_move = get_all_tracks_by_id_offset(sys.argv[2])
            else:
                raise ValueError('Missing id')
        if mode == 'idse':
            if sys.argv[2]:
                with open(sys.argv[2], 'r') as ids_file:
                    ids = [line.rstrip('\n') for line in ids_file]
                    start_id_offset = ids[0]
                    end_id_offset = ids[1]
                    ids_exceptions = ids[2:]
                tracks_to_move = get_all_tracks_by_se_id_offset(
                    start_id_offset, end_id_offset, ids_exceptions)
            else:
                raise ValueError('Missing Filename')
        new_playlist_id = create_playlist()
        add_to_playlist(new_playlist_id, tracks_to_move)
        delete_from_saved(tracks_to_move, new_playlist_id)
    else:
        raise ValueError('Error Missing arg - mode args')
