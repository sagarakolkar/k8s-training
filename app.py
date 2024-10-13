# -*- coding: utf-8 -*-
#from collections.abc import Mapping
from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError
from pyfiglet import Figlet
import json
import requests

f = Figlet(font='slant')
print(f.renderText('SignalFX Observability'))

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})

def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text

class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end

class CMDBIDValidator(Validator):
    def validate(self, document):
        ok = regex.match('[A-Za-z]{3}[0-9]{2}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid Application Prefix / CMDB ID ',
                cursor_position=len(document.text))  # Move cursor to end

class ServiceNameValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[A-Za-z0-9]{5}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid Service Name ',
                cursor_position=len(document.text))  # Move cursor to end

class ServiceURLValidator(Validator):
    def validate(self, document):
        ok = regex.match('^https://[a-z1-9].*.\.com', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid Service Name ',
                cursor_position=len(document.text))  # Move cursor to end
                
class NumberValidator(Validator):
    def validate(self, document):
        try:
            int(document.text)
        except ValueError:
            raise ValidationError(
                message='Please enter a number',
                cursor_position=len(document.text))  # Move cursor to end


print('Hi, Welcome to SignalFX onboarding tool')

questions = [
    {
        'type': 'list',
        'name': 'APM_OPERATION',
        'message': 'Please select SignalFX Observability operation you want to configure for your application ?',
        'choices': ['Create-Detector', 'Create-Synthetic-Test',"Create-SLO",'Create-Dashboard'],
        'filter': lambda val: val.lower()
    }
]

answers = prompt(questions, style=style)

if answers["APM_OPERATION"] == "create-synthetic-test":
    questions = [
        {
            'type': 'input',
            'name': 'CMDB_ID',
            'message': 'What\'s the CMDB ID of your application ?',
            'validate': CMDBIDValidator
        },
        {
            'type': 'input',
            'name': 'Service_Name',
            'message': 'What\'s your service name ?',
            'validate': ServiceNameValidator
        },
            {
            'type': 'input',
            'name': 'Service_URL',
            'message': 'What\'s your service HTTP URL ?',
            'validate': ServiceURLValidator
        },
        {
            'type': 'list',
            'name': 'Environment_Name',
            'message': 'What\'s the environment name?',
            'choices': ['DEV', 'SIT', 'UAT'],
            'filter': lambda val: val.lower()
        },
            {
            'type': 'list',
            'name': 'Synthetic_TEST_Type',
            'message': 'Which Synthetic test type you would like to create',
            'choices': ['UPTIME-HTTP','UPTIME-PORT','API'],
            'filter': lambda val: val.lower()
        },
          {
            'type': 'checkbox',
            'message': 'Select synthetic test location',
            'name': 'Test_Locaiton',
            'choices': [
                Separator('= The location ='),
                {
                    'name': 'aws-us-east-1'
                },
                {
                    'name': 'aws-us-west-2'
                }
            ],
            'validate': lambda answer: 'You must choose at least one location.' \
                if len(answer) == 0 else True
        },
        {
            'type': 'input',
            'name': 'Threshold',
            'message': 'What\'s the synthetic test error threshold?',
            'validate': NumberValidator,
            'filter': lambda val: int(val)
        },
        {
            'type': 'confirm',
            'name': 'Test-Creation-Confirmation',
            'message': 'Are you sure you want to proceed with Synthetic Test Creation?',
            'default': False
        }
    ]
    
    answers = prompt(questions, style=style)
    #data = json.loads(answers)
    print('Synthetic Test Location:', answers["Test_Locaiton"])
    
    syntheticDict = { "${ENV_NAME}": answers["Environment_Name"], "${CMDB_ID}": answers["CMDB_ID"], "${TEST_LOCATION}": answers["Test_Locaiton"], "${SERVICE_NAME}": answers["Service_Name"]}
    
    with open('synthetic-http.json', 'r') as f:
        data = json.load(f)
    
    data["test"]["locationIds"] =  answers["Test_Locaiton"]
    data["test"]["url"] =  answers["Service_URL"]
    data["test"]["name"] =  answers["CMDB_ID"] + "-" + answers["Service_Name"] +"-" + answers["Environment_Name"]
    data["test"]["body"] = "{'alert_name':'the service is down','url':" + answers["Service_URL"] + "}'",
    
    #replace_all(data, syntheticDict)
    #print(data)
    
    
    url = f'https://api.us1.signalfx.com/v2/synthetics/tests/http'
    
    headers = {
        'Content-Type': 'application/json',
        'X-SF-TOKEN': 'yYr3yqwnaoYXPKE5FscSLQ'
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    
    if response.status_code == 201:
        print("############# Successfully created Synthetic Test ################# ")
        print(response.json())
    else:
        print(f"############ Failed to update hostname. Status Code: {response.status_code} #################")
        print(response.text)
else:
     print(f"############ These operations are not live yet, Work is in progress #################")
     
