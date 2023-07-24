import requests
import json
import os

headers = {
    "Authorization": os.getenv("AUTHORIZATION_TOKEN"),
    "accept"       : "application/json"
}

def get_imdb_data(url):
    response = requests.request(method="GET", url= url,
                    headers=headers)
    response_dict = json.loads(response.content)
    return response_dict
