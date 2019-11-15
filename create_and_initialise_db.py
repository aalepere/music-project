"""
    This script creates the music database with the following tables:
    - USERS
    - STREAMS
    - SONGS
    - ALBUMS
    - ARTISTS

    It then generate data to populate it.

    Use: python3 create_and_initialise_db.py
"""

import sqlite3
from datetime import datetime
from random import randint

# Create database
con = sqlite3.connect("music.db")
print(datetime.today(), "music.db has been created")

# Cursor for excuting SQLs
cur = con.cursor()

# Create tables and populate tables

## USERS
### Create table
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

### Populate table
insert_users_sql = """
INSERT INTO USERS (User_id, Email, Birthday, Country, Gender, Inscription_date) VALUES (?, ?, ?, ?,
?,?)
"""

country = {1: "FR", 2: "GB", 3: "DE", 4: "BR"}
gender = {1: "M", 2: "F"}


for i in range(1000):
    cur.execute(
        insert_users_sql,
        (
            i + 1,
            "email%s@gmail.com" % str(i + 1),
            "%s-01-01" % str(randint(1975, 2000)),
            country[randint(1, 4)],
            gender[randint(1, 2)],
            "%s-01-01" % str(randint(2010, 2019)),
        ),
    )

print(datetime.today(), "1000 users have been created")

## STREAMS

## SONGS

## ALBUMS

## ARTISTS
