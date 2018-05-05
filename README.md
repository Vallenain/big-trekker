# sms-hiking-traker

This application is based on :
  - Google App Engine (python Framework and Flask)
  - Firebase (Real-time database)
  - Twilio (SMS server)
  - Angular JS and lumX

To run this project with your own data, you must :
  - Create a Google Cloud Platform project
  - Create a Twilio Account and buy a Phone Number with text message
  - Create a Firebase project (it can be the same as GCP project)

In Twilio configuration you have to configure a Webhook who call the Google App Engine application on /sms-reciever

Requirements:
  - gcloud cli tool
  - gcloud google app engine python
  - virtualenv
  - npm
  - bower
  - python2.7


## Installation

```bash
# For development
$ ./bin/dev-install.sh

# For refreshing webpack bundle
$ npm run build:dev

# Start the server
$ dev_appserver.py app.yaml # start the server on port 8080
# Go to http://localhost:8080

```

Set in Firebase your database rules to be read by anyone :

```json
{
  "rules": {
    ".read": "true",
    ".write": "auth != null"
  }
}
```

## Prepare for production

```bash
# To package the app for production
$ ./bin/prod-install.sh

# To upload your app
$ gcloud auth login your_mail@gmail.com
$ gcloud config set project gcp_project_id
$ gcloud app deploy app.yaml --version=1

# When app uploaded
$ gcloud app browse
```

## Config

Add folder config in server. I removed the folder from the repos to protect my secrets data :)

- server/config
  - \_\_init\_\_.py
  - dev.py
  - prod.py

```python
# dev.py

from __future__ import absolute_import
from .prod import *

# Add below your dev variable config
```

```python
# prod.py

# Firebase
FIREBASE_PROJECT = 'https://YOUR_FIREBASE_ID.firebaseio.com/'
FIREBASE_SECRET = 'YOUR_FIREBASE_SECRET'
AUTH_PAYLOAD  = 'YOUR_AUTH_PAYLOAD'
# For example {"uid": "1", "auth_data": "foo", "other_auth_data": "bar"}
ROOT_OBJECT = 'YOUR_ROOT_OBJECT'

# Twilio
ACCOUNT_SID = "YOUR_TWILIO_SID"
AUTH_TOKEN = "YOUR_TWILIO_TOKEN"
MY_PHONE_NUMBER = 'YOUR_PHONE_NUMBER' # Example : +33611223344

```

## On front side
There is `client/js/private.js` file to add with this content

``` javascript
module.exports = {
    GoogleMapsApiKey: YOURS,
    FirebaseConfig: {
        apiKey: "YOURS",
        authDomain: "PROJECT_ID.firebaseapp.com",
        databaseURL: "https://PROJECT_ID.firebaseio.com",
        projectId: "PROJECT_ID",
        storageBucket: "YOUR_BUCKET.appspot.com", // you can use the default free one of App Engine
        messagingSenderId: "YOURS" // settings > cloud messaging
    }
};
```

## Format of the SMS
Each piece of information is separated with ` - `. Make sure there is none in the `message` part.
The parts are (order matters):
1. latitude
2. longitude
3. weather (see possible values below)
4. break (see possible values below)
5. message

### Weather values
- sunny
- clear-night'
- cloudy
- hazy
- most-cloudy-day
- most-cloudy-night
- rain-snow
- rainy
- showcase
- snowy
- storm
- thunder
- unknown
- windy

### Break values
- eat
- camp
- break
- finish
- start

## Licence

This project is released under the [GPL version 3][1] license.

  [1]: https://www.gnu.org/licenses/gpl.txt
