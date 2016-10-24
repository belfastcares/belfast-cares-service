# belfast-cares-service

The belfast cares api service built using Django utilizing postgres & bootstrap, which can easily be deployed to Heroku.

### Prerequisites
- python3
- pip
- postgres
- virtualenv

Initial setup via : https://github.com/belfastcares/belfast-cares-service/wiki/Setup-Guide---threats-api-service

You can run the following steps manually or use ./setup.sh within the repository. Be sure to chmod 777 setup.sh before use.

### Redeployment script
```
rm -rf belfastcares-env

virtualenv -p python3 belfastcares-env
source belfastcares-env/bin/activate
pip install -r requirements.txt

dropdb hackathon
createdb hackathon
python manage.py migrate
python manage.py loaddata web_app/fixtures/initial_data.json
python manage.py runserver
```

*** Note : You may need to replace belfastcares-env with hackathon-env.
