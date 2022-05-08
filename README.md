# Welcome to the Black Cat Market ![kitty cat](static/loading-cat.png)

This is a black market web application for the cats in the film Cats (2019).
In this applications Cats can operate within the black cat market, dealing catnip to other black cats, or simply checking up on their stockpiles.

## Installation

1. Download the repository and Enter the folder `Black-Cat-Market`
2. Create your virtual environment using
    ``` python3 -m venv env```
3. Activate your local environment using 

    ``` . env/bin/activate```
4. Install the following libraries
    ``` pip install Flask Flask-WTF PyJWT passlib waiting```
5. Create and initialize you database
    ``` python3 bin/createdb.py ```
    ``` python3 bin/makeaccounts.py```
   Feel free to run `sqlite3 black_cat_market.db` to explore what data is stored there

   If you don't like manual exploration here are the two tables, and the default contents of the database. Feel free to change this as you see fit, but please make the users Cats (2019) related!

| Tables      |
| ----------- |
| account     |
| user        |

### account
| id      | owner              | balance |
| ------- | ------------------ | ------- |
| 100     | Harvester          | 7500    |
| 939     | Harvester          | 500     |
| 850     | ThePhilosopher     | 200     |
| 666     | Krazy4KatNip       | 1000    |
| 969     | MrSniffsAlot       | 1000    |

### user
| codename       | name                      | password                     |
| -------------- | ------------------------- | ---------------------------- |
| Harvester      | Demeter                   | pbkdf2_sha256.hash("123456") |
| ThePhilosopher | Plato                     | pbkdf2_sha256.hash("123456") |
| MrSniffsAlot   | Rum Tum Tugger            | pbkdf2_sha256.hash("123456") |
| Krazy4KatNip   | Macavity                  | pbkdf2_sha256.hash("123456") |

## Usage

```
flask run
```