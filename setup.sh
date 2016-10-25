#/bin/sh
set -e

# Prerequisites:

export DATABASE_URL='postgres://djangodbuser:hellokittyislandadventure69@localhost:5432/belfastcares'

bold=$(tput bold)
red=$(tput setaf 1)
normal=$(tput sgr0)

print(){
    echo "${bold}$*${normal}"
}

error(){
    echo "${red}ERROR${normal}: $*" >&2
    exit 1
}

if which brew &>/dev/null; then
    print " - brew already installed "
else
    print " - please install brew"
fi

if which postgres &>/dev/null; then
    print " - postgres already installed"
else
    print " - install postgres"
    brew install postgres
fi


print " Removing virtual environment - belfastcares-env"
rm -rf belfastcares-env

# setting up django environment
print " Creating new virtual enviroment - belfastcares-env"
virtualenv -p python3 belfastcares-env
source belfastcares-env/bin/activate

print " Installing project deps"
pip install -r requirements.txt

# creating database
if psql -l | grep belfastcares | wc -l; then
    print " Dropping existing belfast cares database"
    dropdb belfastcares
fi

print " Creating belfast cares database"
createdb belfastcares

# creating postgres user
if psql postgres -tAc "SELECT 1 FROM pg_roles WHERE rolname='djangodbuser'"; then
    print " - djangodbuser already exists"
else
    print " - creating django db user "
    psql -d belfastcares -c "CREATE USER djangodbuser WITH PASSWORD 'hellokittyislandadventure69'"
fi

print "Adding Database Schema"
python manage.py migrate

print "Populating Database Schema with initial data"
python manage.py loaddata web_app/fixtures/initial_data.json

print "Running server"
python manage.py runserver


