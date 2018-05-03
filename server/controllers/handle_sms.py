# coding: utf-8
from __future__ import absolute_import

import logging
from datetime import date

from flask import current_app, request, Response

from . import app

from twilio import twiml
from firebase import Firebase
from firebase_token_generator import create_token

WEATHER = {
    'sunny': 'clear-day',
    'clear-night': 'clear-night',
    'cloudy': 'cloudy-weather',
    'hazy': 'haze-weather', # brouillard
    'most-cloudy-day': 'most-cloudy',
    'most-cloudy-night': 'most-cloudy-night',
    'rain-snow': 'rain-snow',
    'rainy': 'rainy-weather',
    'showcase': 'showcase',
    'snowy': 'snow-weather',
    'storm': 'storm-weather',
    'thunder': 'thunder-weather',
    'unknown': 'unknown',
    'windy': 'windy-weather',
}

BREAK = ['eat', 'camp', 'break', 'finish', 'start']

# for firebase
logging.debug(app.config)
ROOT_OBJECT = app.config['ROOT_OBJECT']
FIREBASE_PROJECT = app.config['FIREBASE_PROJECT']
FIREBASE_SECRET = app.config['FIREBASE_SECRET']
AUTH_PAYLOAD = app.config['AUTH_PAYLOAD']

def get_content(message, next_id):
    """
    Parse the SMS content and format to be save in Firebase
    body example : 48.87695,2.32943 - sunny - break - pozey oklm

    Args:
        message : str sms content
        next_id : int id in Firebase
    """
    content = message.split(' - ')

    weather = WEATHER[content[1].lower()]

    if content[2].lower() not in BREAK:
        raise Exception('Not in break type')

    return {
        'id': next_id,
        'date': date.today().strftime("%d/%m/%Y"),
        'latitude': float(content[0].split(',')[0]),
        'longitude': float(content[0].split(',')[1]),
        'weather': weather,
        'break': content[2].lower(),
        'message': content[3]
    }

def get_next_id(firebase):
    """
        Determine the next id in Firebase.
        Args:
            firebase: Firebase instance connexion
        Return: int next id
    """
    result = firebase.get()
    return 1 if result is None else len(result) + 1

@app.route('/sms-reciever', methods=['GET', 'POST'])
def smsReciever():
    """
        Handle the SMS when is coming and save it in Firebase
    """
    r = twiml.Response()

    # Limit the request to my phone number
    if not request.form.has_key('From') \
    and request.form['Body'] != current_app.config['MY_PHONE_NUMBER']:
        r.message('Not allowed to send a message !')
        return Response(response=str(r),
                        status=401,
                        mimetype="text/plain")

    # initiate the connexion to Firebase
    token = create_token(FIREBASE_SECRET, AUTH_PAYLOAD)

    firebase_project = FIREBASE_PROJECT + '/' + ROOT_OBJECT + '.json'
    firebase = Firebase(firebase_project, token)

    # Get the message
    if request.form.has_key('Body'):
        body = request.form['Body']

        # Get the next firebase Id and parse the content to firebase
        next_id = get_next_id(firebase)

        content = get_content(body, next_id)

        # saved the content in firebase
        if content is not None:
            try:
                firebase.post(content)
                r.message("Record saved ! id = {}".format(next_id))
            except Exception:
                r.message("Can't save the record in firebase")
        else:
            r.message("Bad body format")
    else:
        r.message("Can't get the body message")

    return str(r)
