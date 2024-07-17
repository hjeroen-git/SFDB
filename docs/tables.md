# Database Schema for MyProject

This document describes the database schema for MyProject. The database is implemented using SQLite and contains the following tables:
- `artists`
- `albums`
- `tracks`
- `tracks_audio_features`
- `playlists`
- `image_url`

And the following junctiontables:
- `artists_albums`
- `albums_tracks`
- `tracks_artists`
- `playlists_tracks`
- `artists_genres`
- `albums_genres`
- `images`
- `related_artists`

## Table: artists

The `artists` table stores information about the users of the application.

| Column Name   | Data Type | Constraints          | Description                       |
| ------------- | --------- | -------------------- | --------------------------------- |
| `id`          | TEXT      | PRIMARY KEY          | Unique identifier for each artist |
| `name`        | TEXT      | NOT NULL, UNIQUE     | The name of the artist            |
| `followers`   | INTEGER   |                      | The number of followers           |
| `popularity`  | INTEGER   |                      |                                   |
| `image_url`   | TEXT      |                      | Largest size image of the artist  |


## Table: albums

The `albums` table stores information about the users of the application.

| Column Name               | Data Type | Constraints          | Description                       |
| ------------------------- | --------- | -------------------- | --------------------------------- |
| `id`                      | TEXT      | PRIMARY KEY          | Unique identifier for each album  |
| `title`                   | TEXT      | NOT NULL, UNIQUE     | The name of the album             |
| `album_type`              | TEXT      |                      | The name of the album             |
| `total_tracks`            | INTEGER   |                      |                                   |
| `image_url`               | TEXT      |                      |                                   |
| `release_date`            | TEXT      |                      |                                   |
| `release_date_precision`  | TEXT      |                      |                                   |


## Table: tracks

The `tracks` table stores information about the users of the application.

| Column Name   | Data Type | Constraints          | Description                       |
| ------------- | --------- | -------------------- | --------------------------------- |
| `id`          | TEXT      | PRIMARY KEY          | Unique identifier for each track  |
| `title`       | TEXT      | NOT NULL             | The name of the track             |
| `duration_ms` | INTEGER   |                      | The duration of the track         |
| `popularity`  | INTEGER   |                      | The name of the track             |
| `disc_number` | INTEGER   |                      | The disc number (usually 1)       |
| `track_number`| INTEGER   |                      | The track number on the disc      |


## Table: tracks_audio_features

The `tracks_audio_features` table stores information about the users of the application.

| Column Name       | Data Type | Constraints          | Description                       |
| -------------     | --------- | -------------------- | --------------------------------- |
| `id`              | TEXT      | PRIMARY KEY          | Unique identifier for each track  |
| `acousticness`    | TEXT      |                      |                                   |
| `danceability`    | REAL      |                      |                                   |
| `energy`          | REAL      |                      |                                   |
| `instrumentalness`| REAL      |                      |                                   |
| `key`             | INTEGER   |                      |                                   |
| `liveness`        | REAL      |                      |                                   |
| `loudness`        | REAL      |                      |                                   |
| `mode`            | INTEGER   |                      |                                   |
| `speechiness`     | REAL      |                      |                                   |
| `tempo`           | REAL      |                      |                                   |
| `time_signature`  | INTEGER   |                      |                                   |
| `valence`         | REAL      |                      |                                   |


## Table: playlists

The `playlists` table stores information about the users of the application.

| Column Name       | Data Type | Constraints          | Description                       |
| -------------     | --------- | -------------------- | --------------------------------- |
| `id`              | TEXT      | PRIMARY KEY          | Unique identifier for each track  |
| `description`     | TEXT      |                      |                                   |
| `followers`       | INTEGER   |                      |                                   |
| `image_url`       | TEXT      |                      |                                   |
| `name`            | TEXT      |                      |                                   |
| `owner`           | TEXT      |                      |                                   |

## Junction Table: playlists_tracks
