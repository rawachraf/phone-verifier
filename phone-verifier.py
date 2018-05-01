#!/usr/bin/python
# -*- coding: utf-8 -*-
import phonenumbers
from phonenumbers import carrier
from phonenumbers import timezone
from phonenumbers import geocoder
from twilio.rest import Client
import requests
import time

params = (('Type', 'caller-name'), )

account_sid = 'Your twilio sid goes here'
auth_token = 'Your twilio auth token goes here'
client = Client(account_sid, auth_token)

with open('verified_phone_numbers.txt', 'r') as myfile:
    text = myfile.read().replace('\n', ' ')

for match in phonenumbers.PhoneNumberMatcher(text, 'US'):
    z = phonenumbers.format_number(match.number,
                                   phonenumbers.PhoneNumberFormat.E164)
    x = phonenumbers.parse(z, 'US')
    if phonenumbers.is_valid_number(x) == True:
        try:
            number = \
                client.lookups.phone_numbers(z).fetch(type='carrier')
            urlstring = 'https://lookups.twilio.com/v1/PhoneNumbers/' \
                + str(z) + '/'
            response = requests.get(urlstring, params=params,
                                    auth=('ACb9e7926bb2510333af3d9f0a119d1dc6'
                                    , '6ce0f5941065bb301a9af14a9bdddb89'
                                    ))
            print z + '  ' + str(timezone.time_zones_for_number(x)) \
                + '  ' + repr(geocoder.description_for_number(x, 'en')) \
                + '   ' + number.carrier['type'] + '   ' \
                + number.carrier['name'] + '   ' \
                + 'Additional info:            ' + response.text
            time.sleep(1)
        except TwilioRestException, error:

            if error.status == 404:
                print z + '  ' + str(timezone.time_zones_for_number(x)) \
                    + '  ' + repr(geocoder.description_for_number(x,
                                  'en')) + '   ' \
                    + 'No carrier information'
            else:
                raise error
