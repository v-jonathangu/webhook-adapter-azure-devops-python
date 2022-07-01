import logging
from datetime import datetime
import os
import json
# also use dotenv to load the environment variables
import requests

import azure.functions as func

# get it from the environment variable, configure it to your taste
forward_url = os.environ.get('DISCORD_WEBHOOK_URL')

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    result = webhook(req.get_json())

    if result:
        return func.HttpResponse(f"Webhook sent successfully", status_code=200)
    else:
        return func.HttpResponse(f"Webhook failed to send", status_code=500)



def webhook(json_content):
    print(json_content)
    # here we take the parameters that we need from the json_data
    # on this example we will take the following parameters:
    # - project  [resource->definition->name]
    # - title of the build [message->text]
    # - markdown of the build [message->markdown]
    # create the new json data
    json_data = {
        "project": json_content['resource']['definition']['name'],
        "title": json_content['message']['text'],
        "markdown": json_content['message']['markdown']
    }
    
    if forward_url is None:
        return False
    return send_to_discord(json_data, forward_url)


def send_to_discord(json, url_webhook) -> bool:
    # do a post with json content to the discord webhook
    # this will send the data to the discord channel
    json_playload = {
        "embeds": [{
            "description": json['markdown'],
            "title": json['title'] + " - " + json['project'],
        }]
    }
    headers = {'Content-Type': 'application/json'}
    result = requests.post(url_webhook, json=json_playload, headers=headers)
    # return the result (int this example discord returns a no content)
    return result.status_code == 204


