#!/bin/bash

# Remove all migrations and load database with music data from the csv file

rm -f db.sqlite3 recommender/migrations/0*.py recommender/migrations/__pycache__/0*.pyc
python manage.py makemigrations && python manage.py migrate
python manage.py makemigrations recommender && python manage.py migrate recommender
# python manage.py migrate recommender zero && python manage.py makemigrations && python manage.py migrate


# Now load music data from the csv file into Django's database

# WINDOWS: remove the # at the beginning of the line below
./sqlite3 db.sqlite3 -cmd ".mode csv" ".import data.csv recommender_musicdata"

# MAC:remove the # at the beginning of the line below
#sqlite3 db.sqlite3 -cmd ".mode csv" ".import data.csv recommender_musicdata"

echo "*********************************************"
echo "If needed, now create super user and insert data into database"

# Windows: Remove the # at the beginning of the line below
#$SHELL
