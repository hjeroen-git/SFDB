import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotify_database import SpotifyDatabase
from spotify_cleaner import SpotifyCleaner
import spotify_login_credentials as spotify_creds
import time
import os
import json

API_WAITTIME = 5

class SpotiWrapper():
    def __init__(self,spotify_database:SpotifyDatabase):
        self.spotify_database = spotify_database
        self.spotify_cleaner = SpotifyCleaner()
        ccm = SpotifyOAuth(
            client_id=spotify_creds.client_id,
            client_secret=spotify_creds.client_secret,
            redirect_uri="https://localhost:8888/callback",
            scope='user-read-recently-played,playlist-read-private')
        self.spotify = spotipy.Spotify(client_credentials_manager=ccm)

    def batchloader(self,function,offset_incr,**kwargs):
        print(f"starting batchloader for {function}")
        offset = 0
        items = []
        kwargs['limit'] = offset_incr
        while True:

            print(f"[Spotify API] batchloader with {function}. offset = {offset}")
            response = function(offset=offset,**kwargs)
            time.sleep(API_WAITTIME)
            if offset + offset_incr > response['total'] or len(response['items']) == 0:
                items += response['items']
                break
            items += response['items']
            offset += offset_incr
        return items
    
    def get_current_user_playlists(self,to_cache=True):
        playlists = self.batchloader(self.spotify.current_user_playlists,20)
        cleaned_playlist_dicts = []
        for playlist in playlists:
            cleaned_dict = self.spotify_cleaner.get_playlist(playlist)
            cleaned_playlist_dicts += cleaned_dict
        if to_cache:
            self.spotify_database.insert_rows('playlists',cleaned_playlist_dicts)
        return cleaned_playlist_dicts

    def get_playlist_tracks(self,playlist_id,to_cache=True):
        tracks = self.batchloader(self.spotify.playlist_tracks,100,playlist_id=playlist_id)
        if to_cache:
            tracks_data = []
            albums_data = []
            artists_data = []
            tracks_artists_data = []

            playlists_tracks_data = self.spotify_cleaner.get_playlists_tracks(playlist_id,tracks)
            for track_i in tracks:
                track = track_i['track']
                tracks_data += self.spotify_cleaner.get_track(track)
                albums_data += self.spotify_cleaner.get_album_from_track(track)
                artists_data += self.spotify_cleaner.get_artists_from_track(track)
                artists_data += self.spotify_cleaner.get_artists_from_album_from_track(track)
                tracks_artists_data += self.spotify_cleaner.get_tracks_artists_from_track(track)

            self.spotify_database.insert_rows('playlists_tracks',playlists_tracks_data)
            self.spotify_database.insert_rows('tracks',tracks_data)
            self.spotify_database.insert_rows('albums',albums_data)
            self.spotify_database.insert_rows('artists',artists_data) 
            self.spotify_database.insert_rows('tracks_artists',tracks_artists_data)
        return tracks


    def get_artist_albums(self,artist_id,to_cache=True):
        albums_from_artist = self.batchloader(self.spotify.artist_albums,20,artist_id=artist_id,include_groups='album,single')
        if to_cache:
            albums_data = []
            artists_data = []
            artists_albums_data = []
            for album in albums_from_artist:
                albums_data += self.spotify_cleaner.get_album(album)
                artists_data += self.spotify_cleaner.get_artists_from_album(album)
                artists_albums_data += self.spotify_cleaner.get_artists_albums_from_album(artist_id,album)
            self.spotify_database.insert_rows('albums',albums_data)
            self.spotify_database.insert_rows('artists',artists_data)
            self.spotify_database.insert_rows('artists_albums',artists_albums_data)
        return albums_from_artist
    

    def get_album_tracks(self,album_id,to_cache=True):
        tracks_from_album = self.batchloader(self.spotify.album_tracks,50,album_id=album_id)
        if to_cache:
            pass
        return tracks_from_album
    

    def get_tracks_audio_features(self,track_ids,to_cache=True):
        tracks_with_audio_features = []
        offset = 0
        while offset < len(track_ids):
            tracks_with_audio_features += self.spotify.audio_features(tracks=track_ids[offset:offset+100])
            offset+=100
            print('Waittime...')
            time.sleep(API_WAITTIME)
        if to_cache:
            tracks_audio_features = []
            for track in tracks_with_audio_features:
                if track:
                    tracks_audio_features += self.spotify_cleaner.get_track_audio_features(track)
            self.spotify_database.insert_rows('tracks_audio_features',tracks_audio_features)
        return tracks_audio_features