import requests
import datetime


def http_request(sla_name, url: str, method, headers=None, auth=None):
    if headers is None:
        headers = {}

    headers['content-type'] = 'application/json'

    start = datetime.datetime.now()
    session = requests.session()
    session.auth = auth
    response = None
    # match method:
    #     case 'get':
    #         response = session.get(url, headers=headers)
    #     case 'post':
    #         response = session.post(url, headers=headers)
    #     case 'put':
    #         response = session.put(url, headers=headers)
    #     case 'delete':
    #         response = session.delete(url, headers=headers)

    end = datetime.datetime.now()
    sla = int((end - start).total_seconds() * 1000)

    requests.session().close()
    return response