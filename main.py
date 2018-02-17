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
    description = """Hello! Welcome to Auto Bartender. I'm your personal drink maker. To get started,
    you can say something like Alexa, ask Auto Bartender to make a vodka with coke.
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


def process_order(first_drink, first_percent, second_drink, second_percent):
    try:
        if first_drink and second_drink and second_drink and second_percent:
            return make_response("Your mixed drink order {} percent {} with {} percent {} is currently being processed.".format(first_percent,first_drink, second_percent, second_drink))
        elif first_drink:
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
            first_percent = intent.get('slots', {}).get(
                'first_percent', {}).get('value', None)
            second_percent = intent.get('slots', {}).get(
                'second_percent', {}).get('value', None)
            if not (first_drink and second_drink and first_percent and second_percent):
                return ask_for_more_response()
        return process_order(first_drink, first_percent, second_drink, second_percent)
    elif req.get('type', '') == 'LaunchRequest':
        return app_description()
    elif req.get('type', '') == 'SessionEndedRequest':
        return make_response("No worries. Let me know if you need another drink. Good bye.")
    return make_response("Unrecognized request")


@app.route('/')
def index():
    return "Hello world"


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=11111)
