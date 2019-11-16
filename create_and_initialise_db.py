"""
    This script creates the music database with the following tables:
    - USERS
    - STREAMS
    - SONGS
    - ALBUMS
    - ARTISTS

    It then generate data or retrieves it through the deezer API to populate it.

    Use: python3 create_and_initialise_db.py
"""

import sqlite3
from datetime import datetime
from random import randint

import requests
from requests.exceptions import HTTPError


# Utils functions
# TODO This function should be updated to cover the case when the search doesn't find any match
def get_artist(artist_name):
    """ Search for the artist and retrieves both id and name
        >>> get_artist("metronomy")
        >>> ('13570','Metronomy')
    """
    url = "https://api.deezer.com/search/artist?q=%s" % artist_name
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    else:
        json = response.json()
        artist_id = json["data"][0]["id"]
        artist_name = json["data"][0]["name"]
    return artist_id, artist_name


def get_list_of_albums(artist_id):
    """ Retrieves all the albums for a given artists. This function takes an artist_id as input, if
    an artist name was to be used then use get_artist first.
    """
    url = "https://api.deezer.com/artist/%s/albums" % str(artist_id)
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    else:
        json = response.json()
    return json


def get_list_of_songs(album_id):
    """Retrieves the list of songs on an album"""
    url = "https://api.deezer.com/album/%s/tracks" % str(album_id)
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
    except HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")  # Python 3.6
    except Exception as err:
        print(f"Other error occurred: {err}")  # Python 3.6
    else:
        json = response.json()
    return json


# Create database
con = sqlite3.connect("music.db")
print(datetime.today(), "music.db has been created")

# Cursor for excuting SQLs
cur = con.cursor()

# Create tables and populate tables

# USERS
# Create table
create_users_tbl_sql = """
CREATE TABLE USERS(
    User_id integer PRIMARY KEY,
    Email VARCHAR(50) NOT NULL,
    Birthday DATE NOT NULL,
    Country CHAR(2) NOT NULL,
    Gender CHAR(1) NOT NULL,
    Inscription_date DATE NOT NULL)"""

cur.execute(create_users_tbl_sql)
print(datetime.today(), "USERS table created")

# Populate table
insert_users_sql = """
INSERT INTO USERS (User_id, Email, Birthday, Country, Gender, Inscription_date) VALUES (?, ?, ?, ?,
?,?)
"""

# List of possible values for country and gender
country = ["FR", "GB", "DE", "BR"]
gender = ["M", "F"]

# Insert 1000 random users
for i in range(1000):
    cur.execute(
        insert_users_sql,
        (
            i + 1,
            "email%s@gmail.com" % str(i + 1),
            "%s-01-01" % str(randint(1975, 2000)),
            country[randint(0, 3)],
            gender[randint(0, 1)],
            "%s-01-01" % str(randint(2010, 2019)),
        ),
    )

print(datetime.today(), "1000 users have been created")

# ARTISTS, ALBUMS & SONGS
# Create tables
create_artists_tbl_sql = """
CREATE TABLE ARTISTS(
    Artist_id integer PRIMARY KEY,
    Artist_name VARCHAR(150) NOT NULL)"""

cur.execute(create_artists_tbl_sql)
print(datetime.today(), "ARTISTS table created")

create_albums_tbl_sql = """
CREATE TABLE ALBUMS(
    Album_id integer PRIMARY KEY,
    Album_title VARCHAR(150) NOT NULL,
    Creation_date DATE NOT NULL)"""

cur.execute(create_albums_tbl_sql)
print(datetime.today(), "ALBUMS table created")

create_songs_tbl_sql = """
CREATE TABLE SONGS(
    Sng_id integer PRIMARY KEY,
    Sng_title VARCHAR(150) NOT NULL,
    Album_id integer NOT NULL,
    Artist_id integer NOT NULL,
    Creation_date DATE NOT NULL,
    FOREIGN KEY(Album_id) REFERENCES ALBUMS(Album_id),
    FOREIGN KEY(Artist_id) REFERENCES ARTISTS(Artist_id))"""

cur.execute(create_songs_tbl_sql)
print(datetime.today(), "SONGS table created")

# Populate tables

artist_list = ["Metronomy", "smiths", "velvet_underground", "led_zeppelin"]
insert_artist_sql = """
INSERT INTO ARTISTS (Artist_id, Artist_name) VALUES (?, ?)
"""
insert_albums_sql = """
INSERT INTO ALBUMS (Album_id, Album_title, Creation_date) VALUES (?, ?, ?)
"""
insert_songs_sql = """
INSERT INTO SONGS (Sng_id, Sng_title, Album_id, Artist_id, Creation_date) VALUES (?, ?, ?, ?, ?)
"""

for artist in artist_list:
    # Retrieve and insert artists
    artist_id, artist_name = get_artist(artist)
    cur.execute(insert_artist_sql, (artist_id, artist_name))
    print(datetime.today(), "Artist %s created" % artist_name)

    # Retrieve albums for the given artist and insert
    album_dict = get_list_of_albums(artist_id)
    for album in album_dict["data"]:
        album_id = album["id"]
        album_title = album["title"]
        creation_date = album["release_date"]
        cur.execute(insert_albums_sql, (album_id, album_title, creation_date))
        print(datetime.today(), "Album %s created" % album_title)

        # Retrieve songs on a given album
        songs_dict = get_list_of_songs(album_id)
        for song in songs_dict["data"]:
            sng_id = song["id"]
            sng_title = song["title"]
            cur.execute(insert_songs_sql, (sng_id, sng_title, album_id, artist_id, creation_date))
            print(datetime.today(), "Song %s created" % sng_title)
