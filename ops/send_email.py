# google cloud function

import os
# import datetime
import requests
from flask import redirect
# from google.cloud import datastore

""" ENV VARS
{
    'MAILGUN_API_KEY': '',
    'MAILGUN_DOMAIN_NAME': 'mg.mywellnessplatform',
    'REDIRECT_SUCCESS_URL: 'https://mywellnessplatform.com',
    'REDIRECT_FAILURE_URL: 'https://mywellnessplatform.com',
    'TO_ADDRESS: '',
    'PROJECT_ID: '',
    'CONFIRMATION_EMAIL_BODY: 'Thanks for contacting us!',
    'CONFIRMATION_EMAIL_FROM_NAME: 'myWellnessPlatform',
}

"""


def start(request):
    success_url = os.environ.get('REDIRECT_SUCCESS_URL', None)
    fail_url = os.environ.get('REDIRECT_FAILURE_URL', None)
    to_address = str(os.environ.get('TO_ADDRESS', None))
    from_email = request.form['email']
    from_name = request.form['from_name']
    body = request.form['body']
    # hidden spam field
    s_body = request.form['s_body']
    subject = request.form['subject']
    if s_body == '' or s_body is None:
        try:
            response = send_email(
                from_email,
                from_name,
                subject,
                body,
                to_address,
            )

            if response == 200:
                return redirect(success_url, code=302)
        except:
            pass
    return redirect(fail_url, code=302)


def send_email(from_email, from_name, subject, body, to_address):
    """
    Send an email using MailGUN API Client
    """

    # Initializing important data from environment
    mg_domain = os.environ.get('MAILGUN_DOMAIN_NAME', None)
    mg_key = os.environ.get('MAILGUN_API_KEY', None)

    # Preparing the data to be sent as email
    url = 'https://api.mailgun.net/v3/{}/messages'.format(mg_domain)
    auth = ('api', mg_key)
    data = {
        'from': '{} <{}>'.format(from_name, from_email),
        'to': to_address,
        'subject': subject,
        'text': body,
    }

    # Sending the email
    response = requests.post(url, auth=auth, data=data)
    return response.status_code


"""
def save_user_data(FROM_NAME, FROM_EMAIL, body):

    # Save the data in our DB as user has not got the email

    # Initializing the data where PROJECT_ID = GCP Project ID
    PROJECT_ID = os.environ.get('PROJECT_ID', None)
    client = datastore.Client(PROJECT_ID)

    key = client.key('Task')

    # Create a new entity
    task = datastore.Entity(key, exclude_from_indexes=['message'])
    task.update({
        'created': datetime.datetime.now(),
        'name': FROM_NAME,
        'email': FROM_EMAIL,
        'message': body
    })

    # Upload the data
    client.put(task)

    return client.key



def send_confirmation_email(FROM_EMAIL, TO_ADDRESS):
    # Send a confirmation email to the user saying we're received their email.
    CONFIRMATION_EMAIL_TO_ADDRESS = FROM_EMAIL
    CONFIRMATION_EMAIL_FROM_ADDRESS = TO_ADDRESS
    CONFIRMATION_SUBJECT = 'Thank you for contacting us!'
    CONFIRMATION_EMAIL_BODY = os.environ.get('CONFIRMATION_EMAIL_BODY', None)
    CONFIRMATION_EMAIL_FROM_NAME = os.environ.get(
        'CONFIRMATION_EMAIL_FROM_NAME', None)

    send_email(CONFIRMATION_EMAIL_FROM_ADDRESS, CONFIRMATION_EMAIL_FROM_NAME,
               CONFIRMATION_SUBJECT, CONFIRMATION_EMAIL_BODY, CONFIRMATION_EMAIL_TO_ADDRESS)
"""