import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time
import sys

# Spotify API credentials
client_id = 'xxx'
client_secret = 'xxx'
redirect_uri = 'http://localhost:8888/callback'

# Authenticate with Spotify
scope = 'playlist-modify-public'
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=client_id,
                                               client_secret=client_secret,
                                               redirect_uri=redirect_uri,
                                               scope=scope))

# Read tracks from the file
with open('tracks.txt', 'r') as f:
    lines = f.readlines()
    playlist_name = lines[0].strip()
    tracks = [line.strip() for line in lines[1:]]

# Function to search for a track and return its URI
def search_track(sp, artist, title):
    query = f'artist:{artist} track:{title}'
    results = sp.search(q=query, type='track', limit=1)
    tracks = results['tracks']['items']
    if tracks:
        return tracks[0]['uri']
    else:
        return None

# Check if the playlist already exists
user_id = sp.current_user()['id']
playlists = sp.current_user_playlists(limit=50)['items']
existing_playlist = None

for playlist in playlists:
    if playlist['name'] == playlist_name:
        existing_playlist = playlist
        break

# Use the existing playlist or create a new one
if existing_playlist:
    playlist_id = existing_playlist['id']
    print(f"Updating existing playlist: '{playlist_name}'")
    # Get the existing track URIs in the playlist
    existing_tracks = sp.playlist_tracks(playlist_id, fields='items(track(uri))')['items']
    existing_track_uris = {item['track']['uri'] for item in existing_tracks}
else:
    playlist = sp.user_playlist_create(user=user_id, name=playlist_name, description="")
    playlist_id = playlist['id']
    print(f"Creating new playlist: '{playlist_name}'")
    existing_track_uris = set()

# Add tracks to the playlist with rate limiting and progress display
track_uris_to_add = []
skipped_tracks = 0
not_found_tracks = []

for i, track in enumerate(tracks):
    try:
        artist, title = track.split(' - ')
        uri = search_track(sp, artist, title)
        if uri:
            if uri not in existing_track_uris:
                track_uris_to_add.append(uri)
            else:
                skipped_tracks += 1
                print(f"Track already in playlist: {artist} - {title}")
        else:
            not_found_tracks.append(track)
    except ValueError:
        print(f"Skipping malformed track entry: {track}")
        not_found_tracks.append(track)

    time.sleep(1)  # Rate limit to avoid hitting Spotify's API rate limits
    sys.stdout.write(f'\rProgress: {i+1}/{len(tracks)} tracks processed')
    sys.stdout.flush()

if track_uris_to_add:
    sp.playlist_add_items(playlist_id=playlist_id, items=track_uris_to_add)
    print('\nAll new tracks added to the playlist.')
else:
    print('\nNo new tracks were added to the playlist.')

# Summary report
print(f"\nSummary Report:")
print(f"Total tracks processed: {len(tracks)}")
print(f"Tracks added: {len(track_uris_to_add)}")
print(f"Tracks skipped (already in playlist): {skipped_tracks}")
print(f"Tracks not found: {len(not_found_tracks)}")
if not_found_tracks:
    print("Tracks not found:")
    for track in not_found_tracks:
        print(f"  - {track}")

print(f"Playlist '{playlist_name}' updated with {len(track_uris_to_add)} new tracks.")
