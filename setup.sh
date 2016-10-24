#/bin/sh
set -e

# Prerequisites:

#PYTHON_VERSION=

#bold=$(tput bold)
#red=$(tput setaf 1)
#normal=$(tput sgr0)

#print(){
# echo 
#}

print " Removing virtual environment - belfastcares-env"
rm -rf belfastcares-env

print " Creating new virtual enviroment - belfastcares-env"
virtualenv -p python3 belfastcares-env
source belfastcares-env/bin/activate

print " Installing project deps"
pip install -r requirements.txt

print " Dropping existing belfast cares database"
dropdb hackathon

print " Creating belfast cares database"
createdb hackathon

print "Adding Database Schema"
python manage.py migrate

print "Populating Database Schema with initial data"
python manage.py loaddata web_app/fixtures/initial_data.json

print "Running server"
python manage.py runserver

