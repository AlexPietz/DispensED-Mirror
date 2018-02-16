# Dispensed Website


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Installing
```
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

## Deployment
Run `./avenv.sh` in a console. Then visit `http://127.0.0.1:5000/`

### Adding additional packages from pip
You may have to install additional packages, make sure you are in the virtual environment and in the "dispensed-web" directory, then
```
$ pip install <package>
$ pip freeze > requirements.txt
$ git add requirements.txt
```

## DB Migration
First, Update app/models.py
Then:
```
$ flask db migrate -m "<quick explaination>"
$ flask db upgrade
```

