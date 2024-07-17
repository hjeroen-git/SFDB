import sqlite3
import constants

class SQLite3Column:
    def __init__(self,name:str,type:str,constraints:list[str]):
        self.name = name
        self.type = type
        self.constraints = constraints
    def to_str(self):
        constraints_str = ' '.join(self.constraints).upper()
        return f"{self.name} {self.type} {constraints_str}"


class SpotifyDatabase:
    def __init__(self):
        self.conn = sqlite3.connect(r'database\music_app.db')
        self.cursor = self.conn.cursor()


    def create_table(self,table_name,columns:list[SQLite3Column]):
        query = f'CREATE TABLE IF NOT EXISTS {table_name} ({",".join(col.to_str() for col in columns)});'
        self.cursor.execute(query)
        self.conn.commit()

    def create_junctiontable(
            self,
            table_name,
            columns,
            reference_table_1,
            reference_column_1,
            reference_table_2,
            reference_column_2):
        column_query = ",\n".join([col.to_str() for col in columns])
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {column_query},
            PRIMARY KEY ({columns[0].name}, {columns[1].name}),
            FOREIGN KEY ({columns[0].name}) REFERENCES {reference_table_1}({reference_column_1}),
            FOREIGN KEY ({columns[1].name}) REFERENCES {reference_table_2}({reference_column_2})
        );
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def print_table_structure(self,table_name):

        # Query to get table structure using PRAGMA table_info
        self.cursor.execute(f"PRAGMA table_info({table_name});")
        columns = self.cursor.fetchall()

        # Print table structure
        print(f"Table Structure for '{table_name}':")
        for column in columns:
            col_name = column[1]
            col_type = column[2]
            notnull = 'NOT NULLABLE' if column[3] else 'NULLABLE'
            is_pk = 'PRIMARY KEY' if column[5] else ''
            print(f"{col_name}: {col_type} ({notnull}, {is_pk})")

    def insert_rows(self,table_name,rows):
        if type(rows) != list:
            rows = [rows]
        row_data = []
        for row in rows:
            self.assert_row(table_name,row)

            row_data.append(tuple(row.values()))

        # Remove duplicates
        row_data = list(set(row_data))
        column_names = constants.COLUMNS_IN_TABLE[table_name]
        question_marks = ', '.join('?'*len(column_names))
        query = f'''
            INSERT OR IGNORE INTO {table_name} ({','.join(column_names)}) VALUES ({question_marks})
            '''
        self.cursor.executemany(query, row_data)
        self.conn.commit()
        

    def assert_row(self,rowtype,row):
        if list(row.keys()) != constants.COLUMNS_IN_TABLE[rowtype]:
            raise AssertionError(f"Mismatch between given and expected columns. Expected {constants.COLUMNS_IN_TABLE[rowtype]}, but got {row.columns}")
        

    def get_artist_id_from_artist_name(self,artist_name):
        self.cursor.execute(f'''
            SELECT artists.id
            FROM artists
            WHERE artists.name = '{artist_name}';
            ''')
        artist_id = self.cursor.fetchone()
        return artist_id[0]
    
    def get_playlist_id_from_playlist_name(self,playlist_name):
        self.cursor.execute(f'''
            SELECT playlists.id
            FROM playlists
            WHERE playlists.name = '{playlist_name}';
            ''')
        playlist_id = self.cursor.fetchone()
        return playlist_id[0]
    
    def get_artist_albums(self,artist_name,albums_only=False):
        if albums_only:
            self.cursor.execute(f'''
                SELECT albums.title
                FROM albums
                JOIN artists_albums ON albums.id = artists_albums.album_id
                JOIN artists ON artists_albums.artist_id = artists.id
                WHERE artists.name = '{artist_name}' AND albums.album_type = 'album';''')
        else:
            self.cursor.execute(f'''
                SELECT albums.title
                FROM albums
                JOIN artists_albums ON albums.id = artists_albums.album_id
                JOIN artists ON artists_albums.artist_id = artists.id
                WHERE artists.name = '{artist_name}';''')
        albums = self.cursor.fetchall()
        return [album[0] for album in albums]
    
    def get_playlist_artists(self,playlist_name,get_id=False):
        if get_id:
            artist_column = 'id'
        else:
            artist_column = 'name' 
        self.cursor.execute(f'''
            SELECT artists.{artist_column}
            FROM artists
            JOIN tracks_artists ON artists.id = tracks_artists.artist_id
            JOIN playlists_tracks ON tracks_artists.track_id = playlists_tracks.track_id
            JOIN playlists ON playlists_tracks.playlist_id = playlists.id
            WHERE playlists.name = '{playlist_name}';''')
        artists = self.cursor.fetchall()
        return [artist[0] for artist in artists]