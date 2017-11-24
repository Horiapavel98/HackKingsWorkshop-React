"""
This sample demonstrates a simple skill built with the Amazon Alexa Skills Kit.
The Intent Schema, Custom Slots, and Sample Utterances for this skill, as well
as testing instructions are located at http://amzn.to/1LzFrj6

For additional samples, visit the Alexa Skills Kit Getting Started guide at
http://amzn.to/1LGWsLG
"""

from __future__ import print_function
import httplib, urllib, json




# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to the Alexa Skills Kit sample. " \
                    "Why don't you ask me what your bank balance is. " 
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Please ask me your bank balance, " 

    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying the Alexa Skills Kit sample. " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))



def set_url(bank_function, account):
    #Place IDs here
    applicationId = "?key="
    if bank_function is "getaccount":
        url = "/accounts/%s" % account 
        url = url + applicationId
    elif bank_function is "transfer":
        url = "/accounts/%s/transfers" % account
        url = url + applicationId
    return url


def http_request(http_type, url):
    conn = httplib.HTTPConnection("api.reimaginebanking.com")

    if http_type is "GET":
        conn.request(http_type, url)
    elif http_type is "POST":
        params = {
            "medium": "balance",
            "payee_id": "",
            "transaction_date": "2017-11-19",
            "status": "pending",
            "description": "transfer",
            "amount": 25
        }
        params = json.dumps(params)
        headers = {"Content-type": "application/json",
            "Accept": "application/json"}
        conn.request(http_type, url, params, headers)

    resp = conn.getresponse()
    print(resp.status)
    print(resp.reason)
    response = resp.read()
    print(response)
    jsonresponse = json.loads(response)


    if http_type is "GET":
        return jsonresponse['balance']
    elif http_type is "POST":
        return jsonresponse['message']



def get_bank_balance(intent, session):
    session_attributes = {}
    reprompt_text = None
    bank_balance = ""

    #Place IDs here
    account = ""
    bank_function = "getaccount"
    http_type = "GET"


    print("INCOMING URL SETTING......")
    print(set_url(bank_function,account))

    bank_balance = http_request(http_type, set_url(bank_function, account))

    print("BANK BALANCE RECEIVED.....")
    print(type(bank_balance))

    speech_output = "Current bank balance on the account is " + str(bank_balance) + " pounds"
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))


def transfer_money_to(intent, session):
    session_attributes = {}
    reprompt_text = None
    message = ""

    #Place IDs here
    account = ""
    bank_function = "transfer"
    http_type = "POST"

    print("INCOMING URL SETTING......")
    print(set_url(bank_function,account))

    message = http_request(http_type, set_url(bank_function, account))

    speech_output = message
    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        intent['name'], speech_output, reprompt_text, should_end_session))





# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "ShowBankBalanceIntent":
        return get_bank_balance(intent, session)
    elif intent_name == "TransferMoneyIntent":
        return transfer_money_to(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
