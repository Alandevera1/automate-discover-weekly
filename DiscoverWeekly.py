from dotenv import load_dotenv
import os
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from datetime import datetime

### TODO ###
# add exception handling
# AUTOMATE
# QOL changes
### TODO ###

load_dotenv()

# creates client to Spotify 
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv('CLIENT_SECRET'),
                                               redirect_uri=os.getenv('REDIRECT_URI'),
                                               scope='playlist-modify-private'))


BASE_URL = 'https://api.spotify.com/v1/'
AUTH_URL = 'https://accounts.spotify.com/api/token'

# POST to get Spotify access token 
auth_response = requests.post(AUTH_URL, {
    'grant_type': 'client_credentials',
    'client_id': os.getenv('CLIENT_ID'), # Spotify integration ID
    'client_secret': os.getenv('CLIENT_SECRET'), # Spotify integration secret
    "expires_in": 3600
})

# convert the response to JSON
auth_response_data = auth_response.json()

# save the access token
access_token = auth_response_data['access_token']

# headers to request anything in the Spotify API 
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

def get_playlist_tracks(playlist_url):
    # Indices of the URI in the playlist link
    playlist_id = playlist_url[len(
        'https://open.spotify.com/playlist/'):len('https://open.spotify.com/playlist/') + 22]

    ''' getting track uris '''
    playlist = requests.request('GET', BASE_URL + 'playlists/' + playlist_id +
                            '/tracks', headers=headers)  # Gets the url and requests data
    playlist = playlist.json()
    # Takes in only the tracks of a playlist
    playlist_tracks = playlist.get('items')

    playlist_track_uri = [track.get('track').get(
        'uri')[14:] for track in playlist_tracks]  # List of uris
    
    return playlist_track_uri

def create_playlist_image(img):
    pass


def run():
    name = f'Discover Weekly [{datetime.today().strftime("%#m/%#d/%Y")}]'
    playlist_id = sp.user_playlist_create(user='alandevera2', name=name, public=False).get('id')
    sp.playlist_add_items(playlist_id=playlist_id, items=get_playlist_tracks(os.getenv('DISCWEEKLY_URL')))
    return 'OK'
    
''' Main method to run the program '''
if __name__ == "__main__":
    run()