#/bin/sh
set -e

export DATABASE_URL='postgres://admin:bcadminpass123@localhost:5432/belfastcares'

# logging colour functions
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
    print " - installing brew"
    /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
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

#TODO - Check if virtual environement exists before removal
print " - removing virtual environment - belfastcares-env"
rm -rf belfastcares-env

# setting up django environment
print " - creating new virtual enviroment - belfastcares-env"
virtualenv -p python3 belfastcares-env
source belfastcares-env/bin/activate

print " - installing project deps via pip"
pip install -r requirements.txt

# creating database
# ensure postgres has started
brew services start postgres
if psql -l | grep belfastcares ; then
    print " - dropping existing belfast cares database"
    dropdb belfastcares
fi

print " - creating belfast cares database"
createdb belfastcares

USER=$(psql postgres -tAc "SELECT 1 from pg_roles where rolname='admin'")

# creating postgres user
if [ "$USER" == "1" ]; then
    print " - postgres admin user already exists"
else
    print " - creating postgres admin user "
    psql -d belfastcares -c "CREATE USER admin WITH PASSWORD 'bcadminpass123'"
fi

print " - applying database migrations"
python manage.py migrate

print " - populating schema with initial data"
python manage.py loaddata web_app/fixtures/initial_data.json

print " - running web server"
python manage.py runserver

