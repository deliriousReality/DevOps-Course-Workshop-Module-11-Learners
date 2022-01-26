import logging, json, uuid, requests

import azure.functions as func


def main(queuein: func.QueueMessage, messageJSON, translationout: func.Out[str]) -> None:
    # logging.info('Python queue trigger function processed a queue item: %s',
    #              queuein.get_body().decode('utf-8'))
    language = json.loads(queuein.get_body().decode('utf-8'))['languageCode']
    translation = json.loads(messageJSON)['Name']
    
    # do translation
    # Add your subscription key and endpoint
    subscription_key = "23410eea111242fa9969e4ec61ef7482"
    endpoint = "https://api.cognitive.microsofttranslator.com"
    # Add your location, also known as region. The default is global.
    # This is required if using a Cognitive Services resource.
    location = "global"
    path = '/translate'
    constructed_url = endpoint + path
    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': language
    }
    constructed_url = endpoint + path

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    # You can pass more than one object in body.
    body = [{
        'text': translation
    }]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    translated = response[0]['translations'][0]['text']

    # write into DB
    rowKey = str(uuid.uuid4())
    row = {
        "Translation": translated,
        "LanguageCode": language,
        "RowKey": rowKey
    }
    translationout.set(json.dumps(row))