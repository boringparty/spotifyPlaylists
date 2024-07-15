import sys
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

def fetch_playlist_info(playlist_id):
    # Set your credentials here
    client_id = 'your_client_id'
    client_secret = 'your_client_secret'

    # Initialize client credentials manager
    client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Fetch playlist tracks with pagination
    results = sp.playlist_tracks(playlist_id)
    tracks = results['items']

    while results['next']:
        results = sp.next(results)
        tracks.extend(results['items'])

    # Print header
    print("Artist|Title|Energy|Key")

    # Iterate through tracks and fetch features
    for track in tracks:
        track_name = track['track']['name']
        artist_name = track['track']['artists'][0]['name']  # Assuming one artist per track
        track_id = track['track']['id']

        # Fetch track features
        features = sp.audio_features([track_id])[0]  # Fetching features for one track

        # Extract desired features
        energy = features['energy']
        key = features['key']
        # Additional features like genre may not be directly available in Spotify API

        # Print formatted output
        print(f"{artist_name}|{track_name}|{energy}|{key}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        playlist_id = sys.argv[1]
        fetch_playlist_info(playlist_id)
    else:
        print("Please provide a Spotify playlist ID.")
