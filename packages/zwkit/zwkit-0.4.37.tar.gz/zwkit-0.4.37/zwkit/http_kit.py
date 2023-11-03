import requests
import json


def http_get(url):
    headers = {'Content-Type': 'application/json'}
    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    else:
        return json.loads(r.text)


def http_post(url, model=None):
    headers = {'Content-Type': 'application/json'}
    if model is None:
        r = requests.post(url, headers=headers)
    else:
        r = requests.post(url, data=model.to_json(), headers=headers)
    if r.status_code != 200:
        raise Exception(r.text)
    else:
        return json.loads(r.text)