from spotipywrapper import SpotiWrapper
from spotify_database import SpotifyDatabase
from spotify_cleaner import SpotifyCleaner

spotify_database = SpotifyDatabase()
spotify_wrapper = SpotiWrapper(spotify_database)

#spotify_wrapper.get_current_user_playlists()
playlist_id = spotify_database.get_playlist_id_from_playlist_name('master')
playlist_tracks = spotify_wrapper.get_playlist_tracks(playlist_id)

#spotify_wrapper.get_artist_albums('0KDuKk6YdEu3hR56HtXmxt')

METAL_ARTISTS = spotify_database.get_playlist_artists('METAL GYM',get_id=True)
albums = []
for artist_id in METAL_ARTISTS:
    print(f'loading albums for {artist_id}')
    albums += spotify_wrapper.get_artist_albums(artist_id)
playlist_id = spotify_database.get_playlist_id_from_playlist_name('METAL GYM')
playlist_tracks = spotify_wrapper.get_playlist_tracks(playlist_id)

artist_id = spotify_database.get_artist_id_from_artist_name('Riley Green')

albums = spotify_database.get_artist_albums('Riley Green',True)
print('hh')