from flask import Flask, jsonify, request, render_template
import json
app = Flask(__name__)


def make_response(msg):
    assert(isinstance(msg, str))
    response = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': msg
            },
            'shouldEndSession': True
        }
    }
    return json.dumps(response)


def app_description():
    description = """Many howdies! Welcome to Auto Bartender. I'm your personal drink maker. To get started,
    you can say something like make me a mixed drink.
    """
    response = {
        'version': '1.0',
        'sessionAttributes': {},
        'response': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': description
            },
            'shouldEndSession': False,
            "reprompt": {
                "outputSpeech": {
                    "type": "PlainText",
                    "text": "What can I do for you?"
                }
            }
        }
    }
    return json.dumps(response)


class DispenseAdpater(object):
    drink_table = {
        "green": 1,
        "sprite": 1,
        "yellow": 2,
        "vodka": 2,
        "blue": 3,
        "rum": 3,
        "red": 4,
        "coke": 4
    }

    def __init__(self):
        pass

    @staticmethod
    def disp(arg1, arg2=None):
        if arg2 is None:
            DispenseAdpater.disp_single(arg1)
            return
        first_drink, first_percent = arg1
        second_drink, second_percent = arg2
        if first_drink.lower() not in DispenseAdpater.drink_table or second_drink.lower() not in DispenseAdpater.drink_table:
            raise Exception("Your drink choice of {} and {} is curently not supported. You should have known that. Go home. You are drunk.".format(
                first_drink, second_drink))
        else:
            first_percent /= 100.0
            first_drink_index = DispenseAdpater.drink_table[first_drink.lower()]
            second_percent /= 100.0
            second_drink_index = DispenseAdpater.drink_table[second_drink.lower()]
            print "{},{},{},{}".format(first_drink_index, first_percent, second_drink_index, second_percent)

    @staticmethod
    def disp_single(arg1):
        first_drink, first_percent = arg1
        if first_drink.lower() not in DispenseAdpater.drink_table:
            raise Exception(
                "Your drink choice of {} is curently not supported. You should have known that. Go home. You are drunk.".format(first_drink))
        else:
            first_percent /= 100.0
            first_drink_index = DispenseAdpater.drink_table[first_drink.lower()]
            print "{}, {}".format(first_drink_index, first_percent)


def process_order(first_drink, first_percent, second_drink, second_percent):
    try:
        if first_drink and first_percent and second_drink and second_percent:
            if (not(0 <= first_percent <= 100 and 0 <= second_percent <= 100)):
                raise Exception("Percentage error. Go home. You are drunk.")
            DispenseAdpater.disp((first_drink, first_percent),
                                 (second_drink, second_percent))
            return make_response("Your mixed drink order {} percent {} with {} percent {} is currently being processed.".format(first_percent, first_drink, second_percent, second_drink))
        elif first_drink:
            DispenseAdpater.disp((first_drink, 100))
            return make_response("Your drink order {} is currently being processed.".format(first_drink))
        else:
            return make_response("Sorry I don't understand your order yet.")
    except Exception as e:
        return make_response(e.message)


def ask_for_more_response():
    response = {
        "version": "1.0",
        "response": {
            "shouldEndSession": False,
            "directives": [
                {
                    "type": "Dialog.Delegate"
                }
            ]
        },
        "sessionAttributes": {}
    }
    return json.dumps(response)


@app.route('/order', methods=['POST', 'GET'])
def order():
    try:
        print request.json
        req = request.json
        first_drink = None
        first_percent = 100
        second_drink = None
        second_percent = 0
        if req.get('type', '') == 'IntentRequest':
            intent = req.get('intent', {})
            if intent.get('name', '') == 'SingleOrder':
                first_drink = intent.get('slots', {}).get(
                    'single_drink', {}).get('value', None)
                if first_drink is None:
                    return ask_for_more_response()
            elif intent.get('name', '') == 'DoubleOrder':
                first_drink = intent.get('slots', {}).get(
                    'first_drink', {}).get('value', None)
                second_drink = intent.get('slots', {}).get(
                    'second_drink', {}).get('value', None)
                first_percent = int(intent.get('slots', {}).get(
                    'first_percent', {}).get('value', 0))
                second_percent = 100 - first_percent
                if not (first_drink and second_drink and first_percent and second_percent):
                    return ask_for_more_response()
            return process_order(first_drink, first_percent, second_drink, second_percent)
        elif req.get('type', '') == 'LaunchRequest':
            return app_description()
        elif req.get('type', '') == 'SessionEndedRequest':
            return make_response("No worries. Let me know if you need another drink. Good bye.")
        return make_response("Unrecognized request")
    except Exception as e:
        return make_response(e.message)


@app.route('/')
def index():
    return "Hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=11111)
