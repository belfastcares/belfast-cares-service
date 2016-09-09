# django-heroku-getting-started

A barebones Django app utilizing postgres & bootstrap, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Local Setup

### Setup Python IDE
Download the pycharm ide - community edition from
```sh 
https://www.jetbrains.com/pycharm/download/download-thanks.html?platform=windows&code=PCC
```

### Ensure you have python installed and then install pip
```sh
wget https://bootstrap.pypa.io/get-pip.py
pip install -upgrade pip
pip install virtualenv
```

### Checkout source code using Git
```sh
git clone https://github.com/apoclyps/django-heroku-seed.git
```

### Mac Setup
```sh
brew install heroku
brew install postgresql
brew services start postgresql
```

### for Linux Distros
```sh
wget -O- https://toolbelt.heroku.com/install-ubuntu.sh | sh
sudo apt-get install sudo apt-get install python-dev libpq-dev python-dev
```

### Create Virtual Enviroment & Install Deps
```sh
virtualenv hackathon-env
source hackathon-env/bin/activate

pip install -r requirements.txt
```

### Create local database
```sh
psql hackathon
CREATE USER user WITH PASSWORD 'password';
```

### Add to ~/.bash_profile
```sh
export DATABASE_URL='postgres:/user:password@localhost:5431/django-heroku-seed'
```

### Setup local server
```sh
createdb django-heroku-seed
```

### create local admin user
```sh
python manage.py createsuperuser
```

### Run local server
```sh
python manage.py migrate
python manage.py collectstatic
python manage.py runserver
```

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com/apoclyps/django-heroku-seed.git
$ cd django-heroku-seed

$ pip install -r requirements.txt

$ createdb django-heroku-seed

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)
-
