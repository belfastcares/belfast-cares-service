#/bin/sh
set -e

# Prerequisites:

export DATABASE_URL='postgres://admin:bcadminpass123@localhost:5432/belfastcares'

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

if which python3 &>/dev/null; then
    print " - python3 already installed"
else
    print " - installing python3"
    brew install python3
fi

if which virtualenv &>/dev/null; then
    print " - virtualenv already installed"
else
    print " - installing virtualenv"
    pip install virtualenv
fi

if which postgres &>/dev/null; then
    print " - postgres already installed"
else
    print " - installing postgres"
    brew install postgres
fi

print " - removing virtual environment - belfastcares-env"
rm -rf belfastcares-env

# setting up django environment
print " - creating new virtual enviroment - belfastcares-env"
virtualenv -p python3 belfastcares-env
source belfastcares-env/bin/activate

print " - installing project deps"
pip install -r requirements.txt

# creating database
if psql -l | grep belfastcares | wc -l; then
    print " - dropping existing belfast cares database"
    dropdb belfastcares
fi

print " - creating belfast cares database"
createdb belfastcares

USER=$(psql postgres -tAc "SELECT 1 from pg_roles where rolname='admin'")

# creating postgres user
if [ "$USER" == "1" ]; then
    print " - admin already exists"
else
    print " - creating admin postgres user "
    psql -d belfastcares -c "CREATE USER admin WITH PASSWORD 'bcadminpass123'"
fi

print "Adding Database Schema"
python manage.py migrate

print "Populating Database Schema with initial data"
python manage.py loaddata web_app/fixtures/initial_data.json

print "Running server"
python manage.py runserver


