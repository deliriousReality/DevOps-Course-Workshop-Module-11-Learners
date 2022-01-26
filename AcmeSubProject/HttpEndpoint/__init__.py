import logging, time, uuid, json

import azure.functions as func


def main(request: func.HttpRequest, translationtable: func.Out[str], translationqueue: func.Out[str]) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    start = time.time()

    # parse json
    req_body = request.get_json()
    subtitle = req_body.get("subtitle")
    languages = req_body.get("languages")

    # write into DB
    rowKey = str(uuid.uuid4())
    row = {
        "Name": subtitle,
        "PartitionKey": "translation",
        "RowKey": rowKey
    }
    translationtable.set(json.dumps(row))

    # write 1 message per language into queue
    messages = []
    for language in languages:
        message = {
            "rowKey": rowKey,
            "languageCode": language
        }
        messages.append(message)
    translationqueue.set(json.dumps(messages))

    # time.sleep(5) # Simulating 5 seconds of cpu-intensive processing
    end = time.time()
    processingTime = end - start

    return func.HttpResponse(
        f"Processing took {str(processingTime)} seconds. Translation stored in rowKey: {rowKey}",
        status_code=200
    )