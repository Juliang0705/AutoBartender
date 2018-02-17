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

def process_order(first_drink, second_drink):
    if first_drink and second_drink:
        return make_response("Your drink order {} with {} is currently being processed.".format(first_drink, second_drink))
    elif first_drink or second_drink:
        drink = first_drink or second_drink
        return make_response("Your drink order {} is currently being processed.".format(drink))
    else:
        return make_response("I'm having a hard time processing your drink right now")

@app.route('/order', methods = ['POST', 'GET'])
def order():
    print request.json
    req = request.json
    first_drink = None
    second_drink = None
    if req.get('type', '') == 'IntentRequest':
        intent = req.get('intent', {})
        if intent.get('name', '') == 'SingleOrder':
            first_drink = intent.get('slots', {}).get('single_drink',{}).get('value', {})
        elif intent.get('name', '') == 'DoubleOrder':
            first_drink = intent.get('slots', {}).get('first_drink', {}).get('value', {})
            second_drink = intent.get('slots', {}).get('second_drink', {}).get('value', {})
        return process_order(first_drink, second_drink)
    elif req.get('type', '') == 'LaunchRequest':
        return app_description()
    return make_response("Unrecognized request")

@app.route('/')
def index():
    return "Hello world"
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=11111)