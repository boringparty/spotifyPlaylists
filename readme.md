I was thinking that I need a way to quickly build spotify playlists. I asked chatGPT 4.x for some help. 

- I provide `tracks.txt` -- the first line is the name of the playlist and the rest is `artist - title`
- based on the playlist name, it'll either create a playlist or update an existing one
- Its using the API with spotipy which has oAuth.
- it doesn't add duplicates
- It shows the progress. Not the prettiest thing, but it serves its purpose.

```
Summary Report:
Total tracks processed: 61
Tracks added: 49
Tracks skipped (already in playlist): 5
Tracks not found: 7
Tracks not found:
  - Les Baxter - Quiet Village Bossa Nova
  - Monster Rally - Coral
  - Lee Fields & The Expressions - Money Is King
Playlist 'Dinner Jazz by chatGPT' updated with 49 new tracks.
```
So that all works  like a charm. I can do about 75 - 100 tracks without any issue. For the tracks themselves, I'm also asking chatGPT

>Can you do the same for various genres of jazz including lounge, exotica, space-age pop, etc. Include artists like Martin Denny, Les Baxter, but also new bands like Khruangbin and Monster Rally. You can also include soul from Colemine Records like Aaron Frazer, Lee Fields, Durand Jones.

In this case it spits out the bands I referenced, so I ask it to branch out. The selection is pretty great. 

It isn't perfect with apostrophes all the time, but for the most part its great. 

Ultimately, I found over the last year or so that Spotify's recommendations are a bit of an echo chamber and I've been trying to pump new music into the algo... with little success. This has a lot of the stuff I already listen to, but I think attacking it via genre instead of specific artists will yield fresh music. 

# Usage

1. update `tracks.txt` with the playlist name in the first row then the `artist - title`
2. run `python playlist.py`

If you want a list of tracks,

1. get the id for the playlist
2. run `python getList.py 1234567890abcdef`
