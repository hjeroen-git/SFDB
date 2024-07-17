from spotify_database import SQLite3Column,SpotifyDatabase


ADD_SAMPLE_DATA = False

sp_db = SpotifyDatabase()
    

artists_schema = [
        SQLite3Column('id','TEXT',['PRIMARY KEY','NOT NULL']),
        SQLite3Column('name','TEXT',['NOT NULL','UNIQUE'])]
sp_db.create_table('artists',artists_schema)


artists_details_schema = [
        SQLite3Column('id','TEXT',['PRIMARY KEY','NOT NULL']),
        SQLite3Column('name','TEXT',['NOT NULL','UNIQUE']),
        SQLite3Column('followers','INTEGER',[]),
        SQLite3Column('popularity','INTEGER',[]),
        SQLite3Column('image_url','TEXT',[])]
sp_db.create_table('artists_details',artists_details_schema)



albums_schema = [
        SQLite3Column('id','TEXT',['PRIMARY KEY','NOT NULL']),
        SQLite3Column('title','TEXT',['NOT NULL','UNIQUE']),
        SQLite3Column('album_type','TEXT',[]),
        SQLite3Column('total_tracks','INTEGER',[]),
        SQLite3Column('image_url','TEXT',[]),
        SQLite3Column('release_date','TEXT',[]),
        SQLite3Column('release_date_precision','TEXT',[])]
sp_db.create_table('albums',albums_schema)



tracks_schema = [
        SQLite3Column('id','TEXT',['PRIMARY KEY','NOT NULL']),
        SQLite3Column('title','TEXT',['NOT NULL']),
        SQLite3Column('duration_ms','INTEGER',[]),
        SQLite3Column('popularity','INTEGER',[]),
        SQLite3Column('disc_number','INTEGER',[]),
        SQLite3Column('track_number','INTEGER',[])]
sp_db.create_table('tracks',tracks_schema)



tracks_audio_features_schema = [
        SQLite3Column('id','TEXT',['PRIMARY KEY','NOT NULL']),
        SQLite3Column('acousticness','TEXT',['NOT NULL']),
        SQLite3Column('danceability','REAL',[]),
        SQLite3Column('energy','REAL',[]),
        SQLite3Column('instrumentalness','REAL',[]),
        SQLite3Column('liveness','REAL',[]),
        SQLite3Column('loudness','REAL',[]),
        SQLite3Column('speechiness','REAL',[]),
        SQLite3Column('valence','REAL',[]),
        SQLite3Column('key','INTEGER',[]),
        SQLite3Column('mode','INTEGER',[]),
        SQLite3Column('tempo','REAL',[]),
        SQLite3Column('time_signature','INTEGER',[])]
sp_db.create_table('tracks_audio_features',tracks_audio_features_schema)



artists_albums_junction_schema = [
    SQLite3Column('artist_id','TEXT',[]),
    SQLite3Column('album_id','TEXT',[])
]
sp_db.create_junctiontable(
    'artists_albums',
    artists_albums_junction_schema,
    'artists',
    'id',
    'albums',
    'id')


albums_tracks_junction_schema = [
    SQLite3Column('album_id','TEXT',[]),
    SQLite3Column('track_id','TEXT',[])
]
sp_db.create_junctiontable(
    'albums_tracks',
    albums_tracks_junction_schema,
    'albums',
    'id',
    'tracks',
    'id')


tracks_artists_junction_schema = [
    SQLite3Column('track_id','TEXT',[]),
    SQLite3Column('artist_id','TEXT',[])
]
sp_db.create_junctiontable(
    'tracks_artists',
    tracks_artists_junction_schema,
    'tracks',
    'id',
    'artists',
    'id')


playlists_schema = [
    SQLite3Column('id','TEXT',['PRIMARY KEY']),
    SQLite3Column('description','TEXT',[]),
    SQLite3Column('followers','INTEGER',[]),
    SQLite3Column('image_url','TEXT',[]),
    SQLite3Column('name','TEXT',[]),
    SQLite3Column('owner','TEXT',[])
]
sp_db.create_table('playlists',playlists_schema)



playlists_tracks_junction_schema = [
    SQLite3Column('playlist_id','TEXT',[]),
    SQLite3Column('track_id','TEXT',[])
]
sp_db.create_junctiontable(
    'playlists_tracks',
    playlists_tracks_junction_schema,
    'playlists',
    'id',
    'tracks',
    'id')



if ADD_SAMPLE_DATA:
    artists_data = [
        {
            'id':'0',
            'name':'artist A',
            'followers':5,
            'popularity':6,
            'image_url':'google'
        },
        {
            'id':'1',
            'name':'artist B',
            'followers':54,
            'popularity':67,
            'image_url':'google'
        }
    ]

    albums_data = [
        {
            'id':'0',
            'title':'album alpha',
            'album_type':'album',
            'total_tracks':5,
            'image_url':'fzefze',
            'release_date':'2024',
            'release_date_precision':'year'
        },
        {
            'id':'1',
            'title':'album beta',
            'album_type':'album',
            'total_tracks':15,
            'image_url':'gfzefze',
            'release_date':'2023',
            'release_date_precision':'year'
        }
    ]
    artists_albums_data = [
        {
            'artist_id':'0',
            'album_id':'0'
        },
        {
            'artist_id':'1',
            'album_id':'0'
        }
    ]


    sp_db.insert_rows('artists',artists_data)
    sp_db.insert_rows('albums',albums_data)
    sp_db.insert_rows('artists_albums',artists_albums_data)
    
    sp_db.conn.commit()

    sp_db.cursor.execute('''
        SELECT albums.title
        FROM albums
        JOIN artists_albums ON albums.id = artists_albums.album_id
        JOIN artists ON artists_albums.artist_id = artists.id
        WHERE artists.name = 'artist A';
        ''')
    
    tracks = sp_db.cursor.fetchall()
    print(tracks)
    sp_db.conn.close()