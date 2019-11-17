# Introduction
This repo creates a music database, then populates it through the Deezer REST API as well as randomly generated records.

# Database
The database is a Sqlite database and host the 5 following tables:
* **USERS**: All users using the Deezer streaming services.
```sql
CREATE TABLE USERS(
    User_id integer PRIMARY KEY,
    Email VARCHAR(50) NOT NULL,
    Birthday DATE NOT NULL,
    Country CHAR(2) NOT NULL,
    Gender CHAR(1) NOT NULL,
    Inscription_date DATE NOT NULL)
```
* **ARTISTS**: All artists; currently the creation script only covers `Metronomy` and `Joy Division`
```sql
CREATE TABLE ARTISTS(
    Artist_id integer PRIMARY KEY,
    Artist_name VARCHAR(150) NOT NULL)
 ```
* **ALBUMS**: All albums recorded by a given artist
```sql
CREATE TABLE ALBUMS(
    Album_id integer PRIMARY KEY,
    Album_title VARCHAR(150) NOT NULL,
    Creation_date DATE NOT NULL)
```
* **SONGS**: All songs present on a given album
```sql
CREATE TABLE SONGS(
    Sng_id integer PRIMARY KEY,
    Sng_title VARCHAR(150) NOT NULL,
    Album_id integer NOT NULL,
    Artist_id integer NOT NULL,
    Creation_date DATE NOT NULL,
    FOREIGN KEY(Album_id) REFERENCES ALBUMS(Album_id),
    FOREIGN KEY(Artist_id) REFERENCES ARTISTS(Artist_id))
 ```
* **STREAMS**: List of songs listened to by a give user
```sql
CREATE TABLE STREAMS(
    Sng_id integer NOT NULL,
    User_id integer NOT NULL,
    Offer_id integer NOT NULL,
    Offer_TnB BOOLEAN NOT NULL,
    Country CHAR(2) NOT NULL,
    Context_of_the_stream VARCHAR(50) NOT NULL,
    Streams_duration integer NOT NULL,
    Stream_date DATE NOT NULL,
    FOREIGN KEY(Sng_id) REFERENCES SONGS(Sng_id),
    FOREIGN KEY(User_id) REFERENCES USERS(User_id))
```

# Install & Setup
First create a virtual environment with `virtualenv`:
```shell
virtual -v env
```
Activate the virtual environment:
```shell
source env/bin/activate
```
Install all Python packages required for this repo:
```shell
pip install - r requirements.txt
```
If you wish to recreate the database, please run the following script:
```shell
python create_and_initialise_db.py

2019-11-17 18:52:04.672021 music.db has been created
2019-11-17 18:52:04.675190 USERS table created
2019-11-17 18:52:04.676792 100 users have been created
2019-11-17 18:52:04.679364 ARTISTS table created
2019-11-17 18:52:04.680899 ALBUMS table created
2019-11-17 18:52:04.682566 SONGS table created
2019-11-17 18:52:04.792614 Artist Metronomy created
2019-11-17 18:52:04.967678 Album Metronomy Forever created
2019-11-17 18:52:05.098154 Song Wedding created
2019-11-17 18:52:05.100162 Song Whitsand Bay created
2019-11-17 18:52:05.101401 Song Insecurity created
2019-11-17 18:52:05.102962 Song Salted Caramel Ice Cream created
2019-11-17 18:52:05.104311 Song Driving created
2019-11-17 18:52:05.105130 Song Lately created
2019-11-17 18:52:05.106328 Song Lying Low created
2019-11-17 18:52:05.107312 Song Forever Is A Long Time created
2019-11-17 18:52:05.109255 Song The Light created
2019-11-17 18:52:05.110716 Song Sex Emoji created
2019-11-17 18:52:05.111505 Song Walking In The Dark created
2019-11-17 18:52:05.112172 Song Insecure created
2019-11-17 18:52:05.114637 Song Miracle Rooftop created
2019-11-17 18:52:05.115828 Song Upset My Girlfriend created
2019-11-17 18:52:05.116552 Song Wedding Bells created
2019-11-17 18:52:05.117322 Song Lately (Going Spare) created
2019-11-17 18:52:05.118145 Song Ur Mixtape created
[...]
```
# SQL statements
All the SQL statements can be visualised in the Jupyter notebook `SQL_queries_PART1_DATA.ipynb`
## Monthly Active Users (MAU) per day per offer and per country
```sql
SELECT ST1.Stream_date,
       ST1.Offer_id,
       ST1.Country,
       SUM(ST1.count) AS MAU
FROM
  (SELECT ST.Stream_date,
          Offer_id,
          U.Country,
          count(DISTINCT ST.User_id) AS COUNT
   FROM STREAMS ST
   INNER JOIN USERS U ON U.User_id = ST.User_id
   WHERE Streams_duration >=30
   GROUP BY Stream_date,
            Offer_id,
            U.Country
   ORDER BY Stream_date,
            Offer_id) ST1
JOIN
  (SELECT Stream_date,
          Offer_id,
          U.Country,
          count(DISTINCT ST.User_id) AS COUNT
   FROM STREAMS ST
   INNER JOIN USERS U ON U.User_id = ST.User_id
   WHERE Streams_duration >=30
   GROUP BY Stream_date,
            Offer_id,
            U.Country
   ORDER BY Stream_date,
            Offer_id) ST2 ON julianDay(ST1.Stream_date) - julianDay(ST2.Stream_date) < 30
AND julianDay(ST1.Stream_date) - julianDay(ST2.Stream_date) >= 0
AND ST1.Offer_id = ST2.Offer_id
AND ST1.Country = ST2.Country
GROUP BY ST1.Stream_date,
         ST1.Offer_id,
         ST1.Country
```
## 10 best streamers of Metronomy in 2016 in France (streamed on French territory)
```sql
SELECT U.User_id,
       U.Email,
       U.Country,
       U.Gender,
       SUM(Streams_duration) AS Total_listen
FROM STREAMS AS ST
INNER JOIN SONGS AS SG ON SG.Sng_id = ST.Sng_id
INNER JOIN ARTISTS AS A ON A.Artist_id = SG.Artist_id
INNER JOIN USERS AS U ON U.User_id = ST.User_id
WHERE A.Artist_name = 'Metronomy'
  AND ST.Country = 'FR'
  AND strftime('%Y', ST.Stream_date)= '2016'
GROUP BY U.User_id,
         U.Email,
         U.Country,
         U.Gender
ORDER BY Total_listen DESC
LIMIT 10
```
## Number of days between the inscription and the 100th stream of all the Brazilian users registered in January 2018
```sql
SELECT U.User_id,
       R.Stream_date,
       U.Inscription_date,
       julianDay(R.Stream_date),
       julianDay(U.Inscription_date)
FROM
  (SELECT User_id,
          Stream_date,
          RANK() OVER(PARTITION BY User_id
                      ORDER BY Stream_date ASC) RANK
   FROM STREAMS) R
INNER JOIN USERS U ON R.User_ID = U.User_id
WHERE R.RANK = 100
  AND U.country ='BR'
  AND strftime('%Y-%m', U.Inscription_date) = '2018-01'
```
# TODOS
* [ ] Add a diagram of the data model
* [ ] Implement unit tests
* [ ] Put CI/CD pipeline in place
* [ ] A couple of updates are required in `create_and_initialise_db.py`; see source code
