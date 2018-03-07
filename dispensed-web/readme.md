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

### Project Structure
```
app
|-- forms.py      # Form settings
|-- __init__.py   # Init module vars
|-- models.py     # Database interface
|-- routes.py     # What URL triggers what function
|-- static
|   `-- <images and other static content>
`-- templates
    `-- <.html templates>

```

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

## API
### Assigning a drug to patient
Drugs from a predefined list can be assigned to each patient. Quantity of the drug and time are also required when adding a drug to a specific patient. 

### Reading the list of assigned drugs
It is assumed that the robot will distribute drugs every 15 minutes. The reading of the list of drugs to be distributed at a spedific time is done by making a request to:  

```
http://localhost:5000/dbread
```

As a result of the request, a JSON file is returned containing a list of patients and the corresponding drugs in the period of +/- 15 minutes from the time of the request. 

For example, if a drug is to be dispensed at 10:00, it will be included in the list returned by a request made in the period from 09:45 until 10:15. 

This way the robot will have this information in the case that it finished earlier or later than supposed to with the current distribution.

### Confirmation for dispensed drugs
In the database in the patient_drug table a new field is added - a flag for dispensed drug.

The procedure for dispensing drugs is as follows:

1) The robot acquires the list of drugs to be distributed by a request to:

```
http://localhost:5000/dbread
```

2) At that point the flags for the drugs that appear in the JSON file are set to false.
This shows that these drugs are still to be dispensed.

3) After the robot dispenses a particular drug, it returns a confirmation through a PUT request to  /dispensed page, including the patient, the drug and the time in JSON format. An example request executed from the Python shell is:

```
from requests import put
```
```
put('http://localhost:5000/dispensed', json={'patient_id': '2', 'drug_id': '3', 'time': '15:35'})
```

At that point the corresponding flag for the dispensed drug becomes true.

All the dispensed drug flags are reset to false at midnight.

### Notifications

If the confirmation for a particular drug has not been received by 15 minutes after the supposed time, a notification (e-mail) is sent to the nurse.
This e-mail contains information about the patient, time and the drug that has not been dispensed.

The email server that will be used to send the emails, along with any required authentication and recipient, is defined in module config.py:

    # Mail server settings
    MAIL_SERVER = 'localhost'
    MAIL_PORT = 25
    MAIL_USE_TLS = False
    MAIL_USE_SSL = False
    MAIL_USERNAME = None
    MAIL_PASSWORD = None
    # Default mail sender
    MAIL_DEFAULT_SENDER = 'team@dispensed.ed'
    # Default mail recipient
    MAIL_DEFAULT_RECIPIENT = 'yourmail@example.com'

The above configuration is only for testing and uses Python's local SMTP debugging server.
The SMTP debugging server can be started from the console window:

    python -m smtpd -n -c DebuggingServer localhost:25

When the SMTP debugging server is running, the emails sent by the application will be received and displayed in the console window.

Note that for the demo we should use an actial mail server and an actual email account.

