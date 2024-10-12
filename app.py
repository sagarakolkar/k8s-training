# -*- coding: utf-8 -*-

from __future__ import print_function, unicode_literals
import regex

from pprint import pprint
from PyInquirer import style_from_dict, Token, prompt, Separator
from PyInquirer import Validator, ValidationError

from pyfiglet import Figlet
f = Figlet(font='slant')
print(f.renderText('SignalFX Observability'))

style = style_from_dict({
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',
})


class PhoneNumberValidator(Validator):
    def validate(self, document):
        ok = regex.match('^([01]{1})?[-.\s]?\(?(\d{3})\)?[-.\s]?(\d{3})[-.\s]?(\d{4})\s?((?:#|ext\.?\s?|x\.?\s?){1}(?:\d+)?)?$', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid phone number',
                cursor_position=len(document.text))  # Move cursor to end

class CMDBIDValidator(Validator):
    def validate(self, document):
        ok = regex.match('[a-z]{3}[1-9]{2}', document.text)
        if not ok:
            raise ValidationError(
                message='Please enter a valid Application Prefix / CMDB ID ',
                cursor_position=len(document.text))  # Move cursor to end

class ServiceNameValidator(Validator):
    def validate(self, document):
        ok = regex.match('^[a-z1-9]{5}', document.text)
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
                'name': 'US-East-1'
            },
            {
                'name': 'US-West-2'
            },
            {
                'name': 'AP-South-1'
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
print('Synthetic Test Configuration:')
pprint(answers)
