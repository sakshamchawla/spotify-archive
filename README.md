# spotify-archive
Move your saved songs to playlists
## Why
If you have a long list of songs in your "Liked Songs" or Saved Songs, which you don't listen to anymore but don't want to lose them either, you can move them to a playlist.

## Requirements
Requires [spotipy](https://spotipy.readthedocs.io/en/2.9.0/)

Requires [Spotify Desktop](https://www.spotify.com/us/download) (explained in Notes).

`python3 -m pip install spotipy`

### Files
#### config
Required for initial configuration. Create file `config` -
```
[client_id]
[client_secret]
[callback_url] (you can use http://localhost)
user-library-read playlist-modify-public user-library-modify
[username]
```
Obtain client_id, client_secret from [developer.spotify.com](developer.spotify.com). Set callback_url as http://localhost.
Do not modify 4th line of config. They are the scopes of authorization that the program Requires. Last line is the username, you can get it from Account Settings in your Spotify account.
#### ids
Required only if you are using ids offset for copying tracks.
Format:
```
start_id_offset
end_id_offset
id_exception1
id_exception2
id_exception3
...
```
id exceptions are those tracks which in the offset range but will be ignored while moving. Can be 0.

## Usage
Several "modes"
- date - use this mode if you want to use date offset
- id - use this mode if you want to use ids offset
- idse - use this mode if you want to set ids range offset


`python3 archiver.py [mode=date|id|idse] [arg=date|id|filename]`

Examples:

`python3 archiver.py date 2019-10-19` will move all songs before `2019-10-19` to a new playlist

`python3 archiver.py id 4RzpCjByV1NWUGKVQGuej6` will move all songs added before this track (inclusive).

`python3 arhiver.py idse list_of_ids.txt` will move all songs listed in range but exceptions in `list_of_ids.txt`

### Notes
- This application will create a new playlist called `Archive - [DATE (MM/YYYY)]` and move your songs.
- You will have an option to **not** delete songs from *Saved Songs*.
- For authentication, it will request the authorization in your default browser. After the authorization is successful, copy the link in the terminal.
- To get track ids, you will need Spotify Desktop application. You can get the track ids by clicking on *Share* > *Copy Spotify URI*. It will look something like this `spotify:track:59PYPDxTbqJpiGfyogPb5h`. The track id is `59PYPDxTbqJpiGfyogPb5h`
