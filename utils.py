import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "client.json"

import dialogflow_v2 as dialogflow

dialogflow_session_client = dialogflow.SessionsClient()
project_id = "news-bot-rfojse"

def detect_intent_from_text(text,session_id,language_code='len'):
    session = dialogflow_session_client.session_path(project_id,session_id)
    text_input = dialogflow.types.TextInput(text=text,language_code=language_code)
    query_input = dialogflow.types.QueryInput(text=text_input)
    response = dialogflow_session_client.detect_intent(session=session,query_input=query_input)
    return response.query_result

def get_reply(query,chat_id):
    response = detect_intent_from_text(query,chat_id)
    if response.intent.display_name == 'get_news':
        return "get_news",dict(response.parameters)
    if response.intent.display_name == 'Corona':
        return "Corona",dict(response.parameters)
    else:
        return "small_talk",response.fulfillment_text


from gnewsclient import gnewsclient


def fetch_news(parameters):
    print(parameters)
    client = gnewsclient.NewsClient()
    country = parameters.get('geo-country')
    if country == '':
        country="India"
        
    client.language = parameters.get('language')
    client.location = country
    client.topic = parameters.get('news')
    return client.get_news()[:5]

topics_Keyboard = [
                    ['Top Stories','World','Nation'],
                    ['Business','Technology','Entertainment'],
                    ['Sports','Science','Health']
                    ]

Corona_topic = [['India Corona Cases'],
                ['Delhi Corona Cases'],
                ['Maharashtra Corona Cases']
                 ]