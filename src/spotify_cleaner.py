

class SpotifyCleaner():
    def __init__(self):
        ...

    def get_track(self,track):
        cleaned_dict = {}
        cleaned_dict['id'] = track['id']
        cleaned_dict['title'] = track['name']
        cleaned_dict['duration_ms'] = track['duration_ms']
        cleaned_dict['popularity'] = track['popularity']
        cleaned_dict['disc_number'] = track['disc_number']
        cleaned_dict['track_number'] = track['track_number']
        return [cleaned_dict]

    def get_playlist(self,playlist):
        cleaned_dict = {}
        cleaned_dict['id'] = playlist['id']
        if 'description' in playlist:
            cleaned_dict['description'] = playlist['description']
        else:
            cleaned_dict['description'] = None
        if 'followers' in playlist:
            cleaned_dict['followers'] = playlist['followers']
        else:
            cleaned_dict['followers'] = None
        if playlist['images'] and len(playlist['images']) > 0:
            cleaned_dict['image_url'] = playlist['images'][0]['url']
        else:
            cleaned_dict['image_url'] = None
        if 'name' in playlist:
            cleaned_dict['name'] = playlist['name']
        else:
            cleaned_dict['name'] = None
        if 'owner' in playlist:
            cleaned_dict['owner'] = playlist['owner']['id']
        else:
            cleaned_dict['owner'] = None
        return [cleaned_dict]
    
    def get_playlists_tracks(self,playlist_id,tracks):
        cleaned_dicts = []
        for track in tracks:
            cleaned_dict = {
                'playlist_id':playlist_id,
                'track_id':track['track']['id']
            }
            cleaned_dicts.append(cleaned_dict)
        return cleaned_dicts


    def get_album(self,album):
        cleaned_dict = {}
        cleaned_dict['id'] = album['id']
        cleaned_dict['title'] = album['name']
        cleaned_dict['album_type'] = album['album_type']
        cleaned_dict['total_tracks'] = album['total_tracks']
        if album['images'] and len(album['images']) > 0:
            cleaned_dict['image_url'] = album['images'][0]['url']
        cleaned_dict['release_date'] = album['release_date']
        cleaned_dict['release_date_precision'] = album['release_date_precision']
        return [cleaned_dict]
    
    def get_artists_from_track(self,track):
        cleaned_dicts = []
        for artist in track['artists']:
            cleaned_dict = {}
            cleaned_dict['id'] = artist['id']
            cleaned_dict['name'] = artist['name']
            cleaned_dicts.append(cleaned_dict)
        return cleaned_dicts
    
    def get_album_from_track(self,track):
        return self.get_album(track['album'])
    
    def get_artists_from_album_from_track(self,track):
        return self.get_artists_from_album(track['album'])

    def get_artists_from_album(self,album):
        cleaned_dicts = []
        for artist in album['artists']:
            cleaned_dict = {
                'id':artist['id'],
                'name':artist['name']
            }
            cleaned_dicts.append(cleaned_dict)
        return cleaned_dicts

    def get_artists_albums_from_album(self,artist_id,album):
        cleaned_dict = {
            'artist_id':artist_id,
            'album_id':album['id']
        }
        return [cleaned_dict]
    
    def get_artists_albums_from_track(self,track):
        return self.get_artists_albums_from_album(track['album'])

    def get_albums_tracks_from_track(self,track):
        cleaned_dict = {
            'album_id':track['album']['id'],
            'track_id':track['id']
        }
        return [cleaned_dict]

    def get_tracks_artists_from_track(self,track):
        cleaned_dicts = []
        for artist in track['artists']:
            cleaned_dict = {
                'track_id':track['id'],
                'artist_id':artist['id']
            }
            cleaned_dicts.append(cleaned_dict)
        return cleaned_dicts